# -*- coding: utf-8 -*-
"""
OpenDART API 로 사업보고서 원문(공시서류 원본 XML)을 내려받아 구조 조사까지 이어 주는 도구.

API 키는 환경변수 OPENDART_API_KEY 로만 읽는다. 파일·로그·저장소에 키를 쓰지 않는다.

하위 명령
  corpcode              corpCode.xml(zip) 내려받아 inputs/raw/CORPCODE.xml 로 캐시
  resolve               pending 슬롯(identity.json)의 stock_code/company 로 corp_code 를 채움
  find [BRxxxx ...]     사업연도 종료일 이후 창(window)에서 A001 접수번호 후보를 찾아 identity.json 에 기록
  fetch [BRxxxx ...]    document.xml 로 원본 zip 내려받아 inputs/raw/BRxxxx/ 에 풀고 본문 XML 경로 기록
  survey [BRxxxx ...]   build/survey_structure.py 를 XML 모드로 실행해 structure.json 생성
  all [BRxxxx ...]      corpcode → resolve → find → fetch → survey

사용 예
  export OPENDART_API_KEY=...            # 키는 셸 환경변수로만
  python3 build/acquire_opendart.py all  # pending 15건 전부
  python3 build/build.py && python3 build/render_html.py

정정 공시 정책: 같은 사업연도의 사업보고서가 여럿이면 최초 제출본(정정 아님)을 표본으로 쓰고,
정정본 접수번호는 identity.json 의 corrections 에 기록만 한다(초기 5건과 같은 기준).
"""
import os, sys, json, re, io, zipfile, time, glob, subprocess, datetime, argparse
import urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IN = os.path.join(ROOT, "inputs")
RAW = os.path.join(IN, "raw")
BASE = "https://opendart.fss.or.kr/api/"
UA = "br-data-structure/0.2 (structural survey)"
PAUSE = 0.6   # 초당 호출 제한을 넉넉히 지킨다

def key():
    k = os.environ.get("OPENDART_API_KEY")
    if not k:
        sys.exit("OPENDART_API_KEY 환경변수가 없다. 키를 파일에 쓰지 말고 export 로 넘겨라.")
    return k

def get(path, params, binary=False):
    params = dict(params); params["crtfc_key"] = key()
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read(); ctype = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} {path}: {e.read()[:200]!r}")
    except urllib.error.URLError as e:
        raise SystemExit(f"접속 실패 {path}: {e.reason}. 이 환경에서 opendart.fss.or.kr 가 차단됐다면 다른 환경에서 실행한다.")
    time.sleep(PAUSE)
    if binary:
        # 오류는 zip 대신 JSON/XML 본문으로 온다
        if data[:2] != b"PK":
            raise SystemExit(f"{path}: zip 이 아님 -> {data[:300]!r}")
        return data
    j = json.loads(data.decode("utf-8"))
    if j.get("status") not in ("000", "013"):   # 013 = 조회 결과 없음
        raise SystemExit(f"{path}: status {j.get('status')} {j.get('message')}")
    return j

def slots(ids=None):
    out = []
    for d in sorted(glob.glob(os.path.join(IN, "reports", "BR*"))):
        br = os.path.basename(d)
        if ids and br not in ids:
            continue
        ip = os.path.join(d, "identity.json")
        if os.path.exists(ip) and not os.path.exists(os.path.join(d, "structure.json")):
            out.append((br, ip, json.load(open(ip, encoding="utf-8"))))
    return out

def save(ip, ident):
    json.dump(ident, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ corpcode
def cmd_corpcode(_):
    os.makedirs(RAW, exist_ok=True)
    p = os.path.join(RAW, "CORPCODE.xml")
    if os.path.exists(p) and time.time() - os.path.getmtime(p) < 7 * 86400:
        print("cached", p); return p
    z = zipfile.ZipFile(io.BytesIO(get("corpCode.xml", {}, binary=True)))
    name = [n for n in z.namelist() if n.lower().endswith(".xml")][0]
    open(p, "wb").write(z.read(name)); print("written", p); return p

def load_corpcode():
    p = os.path.join(RAW, "CORPCODE.xml")
    if not os.path.exists(p):
        cmd_corpcode(None)
    s = open(p, encoding="utf-8", errors="replace").read()
    rows = []
    for m in re.finditer(r"<list>(.*?)</list>", s, flags=re.S):
        b = m.group(1)
        g = lambda t: (re.search(rf"<{t}>(.*?)</{t}>", b, flags=re.S) or [None, ""])[1].strip()
        rows.append({"corp_code": g("corp_code"), "corp_name": g("corp_name"), "stock_code": g("stock_code"), "modify_date": g("modify_date")})
    return rows

# ------------------------------------------------------------------ resolve
def cmd_resolve(a):
    rows = load_corpcode(); by_stock = {r["stock_code"]: r for r in rows if r["stock_code"] and r["stock_code"].strip()}
    for br, ip, ident in slots(a.ids):
        if ident.get("corp_code"):
            print(br, "already", ident["corp_code"]); continue
        cand = None
        sc = (ident.get("stock_code") or "").strip()
        if sc and sc in by_stock:
            cand = by_stock[sc]; how = "stock_code"
        else:
            name = ident["company"]
            exact = [r for r in rows if r["corp_name"] == name and r["stock_code"].strip()]
            part = [r for r in rows if name in r["corp_name"] and r["stock_code"].strip()]
            cand = (exact or part or [None])[0]; how = "name_exact" if exact else ("name_partial" if part else None)
            if not exact and len(part) > 1:
                print(br, ident["company"], "후보 여러 개:", [(r["corp_name"], r["stock_code"], r["corp_code"]) for r in part[:8]])
        if cand:
            ident["corp_code"] = cand["corp_code"]; ident["corp_name_dart"] = cand["corp_name"]; ident["stock_code"] = cand["stock_code"]; ident["corp_code_how"] = how
            save(ip, ident); print(br, ident["company"], "->", cand["corp_code"], cand["corp_name"], cand["stock_code"], f"({how})")
        else:
            print(br, ident["company"], "-> corp_code 미해결. identity.json 에 stock_code 를 채우고 다시 실행")

# ------------------------------------------------------------------ find
def cmd_find(a):
    for br, ip, ident in slots(a.ids):
        if not ident.get("corp_code"):
            print(br, "corp_code 없음 -> resolve 먼저"); continue
        pe = ident["period"].split("~")[1].strip()[:10]           # 사업연도 종료일
        d0 = datetime.date.fromisoformat(pe)
        bgn = d0.strftime("%Y%m%d"); end = (d0 + datetime.timedelta(days=150)).strftime("%Y%m%d")
        j = get("list.json", {"corp_code": ident["corp_code"], "bgn_de": bgn, "end_de": end, "pblntf_ty": "A", "pblntf_detail_ty": "A001", "page_count": 100, "last_reprt_at": "N"})
        lst = j.get("list", []) or []
        want = f"({d0.year}.{d0.month:02d})"
        hits = [x for x in lst if "사업보고서" in x.get("report_nm", "") and want in x.get("report_nm", "")]
        if not hits:   # 사업연도 표기가 다른 경우 대비: 사업보고서면 모두 보여준다
            hits = [x for x in lst if "사업보고서" in x.get("report_nm", "")]
        originals = [x for x in hits if not x["report_nm"].strip().startswith("[")]
        chosen = (originals or hits or [None])[0]
        ident["receipt_candidates"] = [{k: x.get(k) for k in ("rcept_no", "report_nm", "rcept_dt", "rm", "flr_nm")} for x in hits]
        if chosen:
            ident["receipt_id"] = chosen["rcept_no"]; ident["report_nm"] = chosen["report_nm"]; ident["rcept_dt"] = chosen["rcept_dt"]
            ident["corrections"] = [x["rcept_no"] for x in hits if x is not chosen and x["report_nm"].strip().startswith("[")]
            print(br, ident["company"], "->", chosen["rcept_no"], chosen["report_nm"], chosen["rcept_dt"], "| 정정:", ident["corrections"])
        else:
            print(br, ident["company"], "-> 후보 없음 (창", bgn, end, ") 목록:", [(x.get("report_nm"), x.get("rcept_no")) for x in lst[:5]])
        save(ip, ident)

# ------------------------------------------------------------------ fetch
def pick_main_xml(names, rcept_no):
    xmls = [n for n in names if n.lower().endswith(".xml")]
    for n in xmls:
        if rcept_no in n:
            return n
    return xmls[0] if xmls else None

def cmd_fetch(a):
    for br, ip, ident in slots(a.ids):
        rc = ident.get("receipt_id")
        if not rc:
            print(br, "receipt_id 없음 -> find 먼저"); continue
        d = os.path.join(RAW, br); os.makedirs(d, exist_ok=True)
        zp = os.path.join(d, f"{rc}.zip")
        if not os.path.exists(zp):
            open(zp, "wb").write(get("document.xml", {"rcept_no": rc}, binary=True))
        z = zipfile.ZipFile(zp); names = z.namelist(); z.extractall(d)
        # zip 안 파일명이 EUC-KR 로 깨질 수 있어 크기순으로도 보관
        main = pick_main_xml(names, rc)
        if main is None:
            sizes = sorted(((z.getinfo(n).file_size, n) for n in names), reverse=True); main = sizes[0][1]
        ident["acquisition"] = {"state": "acquired", "how": "opendart document.xml", "zip": os.path.relpath(zp, ROOT), "files": names, "main_xml": os.path.relpath(os.path.join(d, main), ROOT),
                                "acquired_at_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"}
        save(ip, ident); print(br, ident["company"], "->", main, "files:", len(names))

# ------------------------------------------------------------------ survey
def cmd_survey(a):
    for br, ip, ident in slots(a.ids):
        mx = (ident.get("acquisition") or {}).get("main_xml")
        if not mx:
            print(br, "main_xml 없음 -> fetch 먼저"); continue
        cmd = [sys.executable, os.path.join(HERE, "survey_structure.py"), br, "--xml", os.path.join(ROOT, mx), "--company", ident["company"], "--year", str(ident["fiscal_year"]),
               "--receipt", ident.get("receipt_id") or "", "--sector", ident.get("sector") or "", "--period", ident.get("period") or ""]
        print(" ".join(cmd[1:])); subprocess.run(cmd, check=True)
        ident["status"] = "surveyed"; save(ip, ident)

def cmd_all(a):
    cmd_corpcode(a); cmd_resolve(a); cmd_find(a); cmd_fetch(a); cmd_survey(a)
    print("done. 다음: python3 build/build.py && python3 build/render_html.py")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["corpcode", "resolve", "find", "fetch", "survey", "all"]); ap.add_argument("ids", nargs="*")
    a = ap.parse_args(); a.ids = set(a.ids) or None
    {"corpcode": cmd_corpcode, "resolve": cmd_resolve, "find": cmd_find, "fetch": cmd_fetch, "survey": cmd_survey, "all": cmd_all}[a.cmd](a)
