# -*- coding: utf-8 -*-
"""
초기 5건 원문 패키지(BRxxxx_saved_results) → inputs/derived/{toc_all,sections_findings,subheads_agg}.json 재생성.

세션 scratchpad 에만 있던 extract_toc.py / node_spans.py / sections_and_findings.py / subheads.py 를
경로 독립적으로 합친 것이다. 저장소에 커밋된 파생 파일과 같은 결과를 낸다(검증: --check).

원문 패키지 위치는 환경변수 BR_PACKAGES 또는 --packages 로 준다. 그 아래에 5개 패키지 폴더가 있어야 한다.
  <BR_PACKAGES>/<임의접두>-BR0001_saved_results/{html/*.html, evidence/BR0001/wrapper.html, results/BR0001/r0001/*.jsonl}
  (폴더명은 'BR0001_saved_results' 로 끝나기만 하면 된다)

사용
  BR_PACKAGES=~/br_packages python3 build/derive_initial_five.py            # inputs/derived/ 갱신
  BR_PACKAGES=~/br_packages python3 build/derive_initial_five.py --check    # 커밋본과 비교만(파일 갱신 없음)
"""
import os, re, sys, json, glob, html, bisect, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "inputs", "derived")
REPORTS = {"BR0001": ("삼성전자", 2024), "BR0044": ("DB손해보험", 2023), "BR0053": ("셀트리온", 2023), "BR0016": ("선바이오", 2021), "BR0020": ("NH프라임리츠", 2021)}
HEAD_PAT = re.compile(r'^(?:\(?\d{1,2}\)|\d{1,2}\)|[가-힣]\.|\d{1,2}-\d{1,2}\.|\[[^\]]{2,60}\]|[①-⑳]|\(\d{1,2}-\d{1,2}\))')

def norm(t): return re.sub(r'[\s【】\[\]()（）]', '', t)
def strip(h): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html.unescape(h)).replace('\xa0', ' ')).strip()
def read(p): return open(p, encoding="utf-8", errors="replace", newline="").read()   # \r\n 보존: nodes.jsonl 오프셋 기준

def package_dir(base, br):
    c = [d for d in glob.glob(os.path.join(base, f"*{br}_saved_results")) if os.path.isdir(d)]
    if not c: sys.exit(f"패키지 없음: {base}/*{br}_saved_results")
    return c[0]

def toc_of(wrapper, body):
    toc = []
    for m in re.finditer(r"var (node(\d))\s*=\s*\{\};(.*?)(?=var node\d\s*=\s*\{\};|function |$)", wrapper, flags=re.S):
        lvl = int(m.group(2)); b = m.group(3)
        g = lambda k: re.search(r"\['%s'\]\s*=\s*\"([^\"]*)\"" % k, b)
        t, eid, off, ln, tocno, nid = (g(k) for k in ("text", "eleId", "offset", "length", "tocNo", "id"))
        if not t: continue
        toc.append({"level": lvl, "text": html.unescape(t.group(1)).strip(), "id": nid.group(1) if nid else None, "eleId": eid.group(1) if eid else None,
                    "offset": int(off.group(1)) if off else None, "length": int(ln.group(1)) if ln else None, "tocNo": tocno.group(1) if tocno else None})
    anchors = {m.group(1): {"pos": m.start(), "text": re.sub(r'<[^>]+>', '', html.unescape(m.group(2))).strip()} for m in re.finditer(r"<A name='toc(\d+)'>(.*?)</A>", body, flags=re.S | re.I)}
    for t in toc:
        a = anchors.get(t["id"]); t["html_pos"] = a["pos"] if a else None; t["anchor_text"] = a["text"] if a else None
    order = sorted([t for t in toc if t["html_pos"] is not None], key=lambda x: x["html_pos"])
    for i, t in enumerate(order): t["html_end"] = order[i + 1]["html_pos"] if i + 1 < len(order) else len(body)
    return toc, len(anchors)

def node_spans(pkg, br):
    spans, types = {}, {}
    for fn in sorted(glob.glob(os.path.join(pkg, "results", br, "r0001", "nodes*.jsonl"))):
        for l in open(fn, encoding="utf-8"):
            if not l.strip(): continue
            r = json.loads(l); nid = r["id"].split("/")[-1]
            for x in r.get("source_refs") or []:
                if x.get("locator_type") == "text_span" and x.get("locator"): spans[nid] = (x["locator"]["start"], x["locator"]["end"]); break
            types[nid] = r.get("node_type")
    return spans, types

def sections_findings(pkg, br, s, toc, spans, types):
    anchors = [(m.start(), strip(m.group(2))) for m in re.finditer(r"<A name='toc(\d+)'>(.*?)</A>", s, flags=re.S | re.I)]
    xbrl = [(m.start(), strip(m.group(1))) for m in re.finditer(r"<P class='table-group-xbrl'>(.*?)</P>", s, flags=re.S)]
    secs = []; ai = 0
    for t in toc:                                   # wrapper 목차 ↔ 본문 앵커: 텍스트 순서 two-pointer 정렬
        pos = None
        for j in range(ai, min(ai + 4, len(anchors))):
            if norm(anchors[j][1]) == norm(t["text"]): pos = anchors[j][0]; ai = j + 1; break
        secs.append({"level": t["level"], "text": t["text"], "pos": pos, "src": "anchor" if pos is not None else None})
    for i, sec in enumerate(secs):                  # 미정렬 항목: 부모 범위 안의 xbrl 제목 → 본문 검색
        if sec["pos"] is not None: continue
        par = next((j for j in range(i - 1, -1, -1) if secs[j]["level"] < sec["level"]), None)
        if par is None or secs[par]["pos"] is None: continue
        pstart = secs[par]["pos"]; pend = len(s)
        for j in range(par + 1, len(secs)):
            if secs[j]["level"] <= secs[par]["level"] and secs[j]["pos"] is not None: pend = secs[j]["pos"]; break
        cands = [(p, tx) for p, tx in xbrl if pstart <= p < pend and norm(tx) == norm(sec["text"])]
        if cands: sec["pos"] = cands[0][0]; sec["src"] = "xbrl_heading"
        else:
            pat = (re.escape(sec["text"].split(".")[0] + ".") + r"\s*" + re.escape(sec["text"].split(".", 1)[1].strip()[:12])) if "." in sec["text"] else re.escape(sec["text"][:10])
            m = re.search(pat, s[pstart:pend])
            if m: sec["pos"] = pstart + m.start(); sec["src"] = "text_search"
    withpos = [(i, x) for i, x in enumerate(secs) if x["pos"] is not None]
    for k, (i, x) in enumerate(withpos):
        x["end"] = next((x2["pos"] for _, x2 in withpos[k + 1:] if x2["level"] <= x["level"]), len(s))
    starts = sorted((a, nid, types[nid]) for nid, (a, b) in spans.items()); keys = [a for a, _, _ in starts]
    def count_in(a, b):
        c = collections.Counter(t for _, _, t in starts[bisect.bisect_left(keys, a):bisect.bisect_left(keys, b)]); return {k: c[k] for k in ("table", "cell", "paragraph", "image")}
    for x in secs:
        if x["pos"] is None: x["counts"] = None; x["subheads"] = []; continue
        x["counts"] = count_in(x["pos"], x["end"])
        subs = []
        for m in re.finditer(r'<P[^>]*>(.*?)</P>', s[x["pos"]:x["end"]], flags=re.S | re.I):
            t = strip(m.group(1))
            if 2 < len(t) < 70 and HEAD_PAT.match(t) and not t.startswith("(단위") and not t.startswith("(기준일"): subs.append(t)
        x["subheads"] = subs
    finds = []
    for fn in sorted(glob.glob(os.path.join(pkg, "results", br, "r0001", "findings*.jsonl"))):
        for l in open(fn, encoding="utf-8"):
            if not l.strip(): continue
            r = json.loads(l)
            ev = [e["id"].split("/")[-1] for e in (r.get("evidence_refs") or []) if isinstance(e, dict) and "id" in e and "/node/" in e["id"]] or \
                 [e["id"].split("/")[-1] for e in (r.get("target_refs") or []) if isinstance(e, dict) and "id" in e and "/node/" in e["id"]]
            pos = next((spans[e][0] for e in ev if e in spans), None)
            if pos is None:
                pos = next((x["locator"]["start"] for x in (r.get("source_refs") or []) if x.get("locator_type") == "text_span"), None)
            path = [i for i, x in enumerate(secs) if pos is not None and x["pos"] is not None and x["pos"] <= pos < x["end"]]
            prop = r.get("proposal")
            finds.append({"id": r["id"].split("/")[-1], "record_type": r.get("record_type"), "summary": r.get("summary"), "state": r.get("state"), "evidence": ev[:5], "pos": pos,
                          "section_path": [secs[i]["text"] for i in path], "section_idx": path[-1] if path else None,
                          "proposal": (prop if isinstance(prop, str) else json.dumps(prop, ensure_ascii=False)[:300]) if prop else None})
    return secs, finds

def clean_sub(h):
    hn = re.sub(r'\s+', ' ', h)
    hn = re.sub(r'^\(?\d{1,2}\)|^\d{1,2}\)|^[가-힣]\.|^\d{1,2}-\d{1,2}\.|^[①-⑳]|^\(\d{1,2}-\d{1,2}\)', '', hn).strip()
    hn = hn.strip("[]").strip(); return re.sub(r'\s*\(.*?\)\s*$', '', hn) if len(hn) > 25 else hn

def subheads_agg(R):
    agg = collections.defaultdict(lambda: collections.defaultdict(set))
    for br, r in R.items():
        cur1 = None
        for x in r["sections"]:
            if x["level"] == 1: cur1 = x["text"]
            if x["pos"] is None: continue
            if x["level"] == 2 or (x["level"] == 1 and x["text"].split(".")[0] in ("IV", "VII", "IX", "X")):
                key = f"{cur1} > {x['text']}" if x["level"] == 2 else x["text"]
                for h in x["subheads"]:
                    hn = clean_sub(h)
                    if len(hn) >= 2: agg[key][hn].add(br)
    return {key: [(h, sorted(b)) for h, b in sorted(agg[key].items(), key=lambda kv: (-len(kv[1]), kv[0]))] for key in agg}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--packages", default=os.environ.get("BR_PACKAGES")); ap.add_argument("--check", action="store_true"); a = ap.parse_args()
    if not a.packages: sys.exit("원문 패키지 위치를 BR_PACKAGES 환경변수 또는 --packages 로 지정한다.")
    toc_all, R = {}, {}
    for br, (name, yr) in REPORTS.items():
        pkg = package_dir(a.packages, br)
        w = read(os.path.join(pkg, "evidence", br, "wrapper.html")); s = read(glob.glob(os.path.join(pkg, "html", "*.html"))[0])
        toc, na = toc_of(w, s)
        toc_all[br] = {"company": name, "year": yr, "html_len": len(s), "toc": toc, "anchors_found": na}
        spans, types = node_spans(pkg, br)
        secs, finds = sections_findings(pkg, br, s, toc, spans, types)
        R[br] = {"company": name, "year": yr, "html_len": len(s), "sections": secs, "findings": finds}
        print(f"{br} {name} {yr}: toc {len(toc)} anchors {na} | sections {len(secs)} with pos {sum(1 for x in secs if x['pos'] is not None)} | nodes {len(types)} | findings {len(finds)} located {sum(1 for f in finds if f['section_idx'] is not None)}")
    outputs = {"toc_all.json": toc_all, "sections_findings.json": R, "subheads_agg.json": subheads_agg(R)}
    if a.check:
        ok = True
        for fn, obj in outputs.items():
            cur = json.load(open(os.path.join(OUT, fn), encoding="utf-8"))
            same = json.loads(json.dumps(obj, ensure_ascii=False)) == cur; ok &= same
            print(f"  {fn}: {'일치' if same else '불일치'}")
        sys.exit(0 if ok else 1)
    os.makedirs(OUT, exist_ok=True)
    for fn, obj in outputs.items():
        json.dump(obj, open(os.path.join(OUT, fn), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"→ {OUT}/{{{','.join(outputs)}}}  (report_status.json 은 각 패키지 manifest.json 에서 손으로 옮긴 요약이라 재생성하지 않는다)")

if __name__ == "__main__":
    main()
