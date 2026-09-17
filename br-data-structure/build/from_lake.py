# -*- coding: utf-8 -*-
"""
dart_bulk_download.py 로 만든 수집 폴더(lake)에서 pending 슬롯의 사업보고서를 찾아 골격 파이프라인에 넣는다.

lake 구조(dart_bulk_download.py v1.2.0):
  <lake>/manifest.sqlite3            filings(rcept_no, corp_code, corp_name, stock_code, report_nm, rcept_dt, status, zip_path, sha256 …)
  <lake>/raw/documents/YYYY/MM/DD/<rcept_no>.zip
  <lake>/extracted/YYYYMMDD/<rcept_no>/…   (extract 명령을 돌린 경우)

동작
  1) identity.json 의 stock_code(없으면 회사명)와 사업연도 종료월로 filings 에서 '사업보고서 (YYYY.MM)' 원공시를 찾는다.
     정정본([기재정정] 등)은 corrections 에 기록만 한다.
  2) status=downloaded 인 ZIP 을 열어 본문 XML 을 inputs/raw/BRxxxx/ 로 꺼낸다(gitignore).
  3) build/survey_structure.py --xml 로 구조 조사를 실행한다.
  4) lake 에 없으면 dart_bulk_download.py 실행 명령(회사별 좁은 창)을 출력한다.

사용
  python3 build/from_lake.py --lake /path/to/dart_annual_lake              # pending 전부
  python3 build/from_lake.py --lake /path/to/dart_annual_lake BR0043 BR0082
  python3 build/from_lake.py --plan                                        # lake 없이 실행 계획만 출력
"""
import os, sys, re, json, glob, sqlite3, zipfile, shutil, datetime, argparse, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

def load_slots(reports_dir, ids=None):
    out = []
    for d in sorted(glob.glob(os.path.join(reports_dir, "BR*"))):
        br = os.path.basename(d)
        if ids and br not in ids:
            continue
        ip = os.path.join(d, "identity.json")
        if os.path.exists(ip) and not os.path.exists(os.path.join(d, "structure.json")):
            out.append((br, ip, json.load(open(ip, encoding="utf-8"))))
    return out

def period_end(ident):
    return datetime.date.fromisoformat(ident["period"].split("~")[1].strip()[:10])

def bulk_command(ident, corp_code=None):
    pe = period_end(ident)
    start = pe.strftime("%Y%m%d"); end = (pe + datetime.timedelta(days=150)).strftime("%Y%m%d")
    cc = corp_code or "<8자리 회사 고유번호: corpCode.xml 또는 기존 lake manifest 의 corp_code>"
    return (f"python dart_bulk_download.py run --out ./lake_{ident['sample_id']} --corp-code {cc} "
            f"--start {start} --end {end} --export --wait-on-limit   # {ident['company']} {ident['fiscal_year']}")

def find_in_lake(db, ident):
    pe = period_end(ident)
    want = f"({pe.year}.{pe.month:02d})"
    sc = (ident.get("stock_code") or "").strip()
    rows = []
    if sc:
        rows = db.execute("SELECT * FROM filings WHERE stock_code=? AND report_nm LIKE '%사업보고서%' AND rcept_dt>=? ORDER BY rcept_dt", (sc, pe.strftime("%Y%m%d"))).fetchall()
    if not rows:
        rows = db.execute("SELECT * FROM filings WHERE corp_name LIKE ? AND report_nm LIKE '%사업보고서%' AND rcept_dt>=? ORDER BY rcept_dt", (f"%{ident['company']}%", pe.strftime("%Y%m%d"))).fetchall()
    hits = [r for r in rows if want in (r["report_nm"] or "")]
    originals = [r for r in hits if not (r["report_nm"] or "").strip().startswith("[")]
    chosen = (originals or hits or [None])[0]
    corrections = [r["rcept_no"] for r in hits if chosen is not None and r["rcept_no"] != chosen["rcept_no"]]
    return chosen, hits, corrections

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*"); ap.add_argument("--lake"); ap.add_argument("--plan", action="store_true")
    ap.add_argument("--reports-dir", default=os.path.join(ROOT, "inputs", "reports")); ap.add_argument("--raw-dir", default=os.path.join(ROOT, "inputs", "raw"))
    ap.add_argument("--no-survey", action="store_true")
    a = ap.parse_args(); ids = set(a.ids) or None
    slots = load_slots(a.reports_dir, ids)
    if a.plan or not a.lake:
        print("# lake 없이 실행 계획. 회사별로 좁은 접수일 창만 조회하므로 전체 수집보다 훨씬 빠르다.")
        for br, ip, ident in slots:
            print(bulk_command(dict(ident, sample_id=br), ident.get("corp_code")))
        print("# 받은 뒤: python3 build/from_lake.py --lake ./lake_BRxxxx BRxxxx  (또는 여러 lake 를 차례로)")
        return
    lake = os.path.abspath(a.lake)
    dbp = os.path.join(lake, "manifest.sqlite3")
    if not os.path.exists(dbp):
        sys.exit(f"manifest.sqlite3 가 없다: {lake}")
    db = sqlite3.connect(f"file:{dbp}?mode=ro", uri=True); db.row_factory = sqlite3.Row
    done = 0
    for br, ip, ident in slots:
        ident["sample_id"] = br
        chosen, hits, corrections = find_in_lake(db, ident)
        if chosen is None:
            print(f"{br} {ident['company']} {ident['fiscal_year']}: lake 에 없음 → {bulk_command(ident, ident.get('corp_code'))}")
            continue
        ident.update({"receipt_id": chosen["rcept_no"], "corp_code": chosen["corp_code"], "corp_name_dart": chosen["corp_name"], "stock_code": chosen["stock_code"] or ident.get("stock_code"),
                      "report_nm": chosen["report_nm"], "rcept_dt": chosen["rcept_dt"], "corrections": corrections,
                      "receipt_candidates": [{k: r[k] for k in ("rcept_no", "report_nm", "rcept_dt", "rm")} for r in hits]})
        if chosen["status"] != "downloaded" or not chosen["zip_path"]:
            ident["acquisition"] = {"state": "listed_not_downloaded", "lake": lake, "status": chosen["status"], "note": "dart_bulk_download.py run --mode download 로 원문을 받은 뒤 다시 실행"}
            json.dump(ident, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"{br} {ident['company']}: 목록에는 있으나 미다운로드(status={chosen['status']})"); continue
        zp = os.path.join(lake, chosen["zip_path"])
        if not os.path.exists(zp):
            print(f"{br}: ZIP 없음 {zp}"); continue
        sha = hashlib.sha256(open(zp, "rb").read()).hexdigest()
        if chosen["sha256"] and sha != chosen["sha256"]:
            print(f"{br}: ZIP SHA-256 불일치, lake verify 필요 {zp}"); continue
        d = os.path.join(a.raw_dir, br); os.makedirs(d, exist_ok=True)
        z = zipfile.ZipFile(zp); names = z.namelist()
        xmls = [n for n in names if n.lower().endswith(".xml")]
        main = next((n for n in xmls if chosen["rcept_no"] in n), None) or (max(xmls, key=lambda n: z.getinfo(n).file_size) if xmls else None)
        if main is None:
            print(f"{br}: ZIP 안에 XML 없음 {names}"); continue
        z.extractall(d)
        ident["acquisition"] = {"state": "acquired", "how": "dart_bulk_download.py lake", "lake": lake, "zip": zp, "zip_sha256": sha, "files": names,
                                "main_xml": os.path.relpath(os.path.join(d, main), ROOT), "acquired_at_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"}
        json.dump(ident, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{br} {ident['company']} {ident['fiscal_year']} ← {chosen['rcept_no']} {chosen['report_nm']} ({chosen['rcept_dt']}) main={main} 정정={corrections}")
        if not a.no_survey:
            cmd = [sys.executable, os.path.join(HERE, "survey_structure.py"), br, "--xml", os.path.join(d, main), "--company", ident["company"], "--year", str(ident["fiscal_year"]),
                   "--receipt", chosen["rcept_no"], "--sector", ident.get("sector") or "", "--period", ident.get("period") or "", "--out", os.path.join(a.reports_dir, br, "structure.json")]
            subprocess.run(cmd, check=True)
            ident["status"] = "surveyed"; json.dump(ident, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        done += 1
    print(f"완료 {done}/{len(slots)}. 다음: python3 build/build.py && python3 build/render_html.py")

if __name__ == "__main__":
    main()
