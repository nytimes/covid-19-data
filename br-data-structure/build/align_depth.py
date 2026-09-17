# -*- coding: utf-8 -*-
"""
여러 보고서의 절 트리를 Depth 별로 나래비 세워 공통 체계와 변형을 뽑는다.

입력: inputs/reports/*/structure.json  (survey_structure.py 산출)
출력: inputs/derived/depth_alignment.json
      - depth 별로 (템플릿 노드 기준) 각 보고서의 제목·순서·표/셀 수
      - 전건 공통 / 일부 / 단독 출현 분류, 제목 표기 변형(별칭 후보), 순서 불일치

왜 노드 기준인가
  원문 XML/HTML 의 요소 깊이는 표현 구조이지 의미 계층이 아니다. 의미 축은 절 제목이므로
  제목을 템플릿 노드로 정규화한 뒤 그 노드를 키로 정렬한다. 정규화에 실패한 제목은 unmatched 로 남겨
  골격 개정 후보가 된다.

사용: python3 build/align_depth.py [--reports-dir inputs/reports]
"""
import os, re, json, glob, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

def norm(t): return re.sub(r'[\s·ㆍ,.()（）\[\]【】]', '', (t or "")).lower()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports-dir", default=os.path.join(ROOT, "inputs", "reports"))
    ap.add_argument("--out", default=os.path.join(ROOT, "inputs", "derived", "depth_alignment.json"))
    a = ap.parse_args()
    tree = json.load(open(os.path.join(ROOT, "skeleton", "data_tree_template.json"), encoding="utf-8"))
    tnodes, torder = {}, []
    def walk(n):
        tnodes[n["id"]] = n; torder.append(n["id"])
        for c in n.get("children") or []: walk(c)
    walk(tree["root"])

    reports, per = [], collections.defaultdict(dict)
    unmatched = collections.defaultdict(list)
    for p in sorted(glob.glob(os.path.join(a.reports_dir, "BR*", "structure.json"))):
        s = json.load(open(p, encoding="utf-8")); ident = s["identity"]; br = ident["sample_id"]
        reports.append({"id": br, "company": ident.get("company"), "fiscal_year": ident.get("fiscal_year"), "sector": ident.get("sector")})
        seq = collections.Counter()
        for i, sec in enumerate(s["sections"]):
            nid = sec.get("node")
            if not nid:
                unmatched[br].append({"level": sec["level"], "text": sec["text"]}); continue
            seq[nid] += 1
            c = sec.get("counts") or {}
            prev = per[nid].get(br)
            rec = {"title": sec["text"], "order": i, "level": sec["level"],
                   "tables": c.get("table", 0), "cells": c.get("cell", 0), "paragraphs": c.get("paragraph", 0),
                   "subheads": len(sec.get("subheads") or []), "occurrences": seq[nid]}
            if prev:  # 같은 노드에 여러 절이 매칭되면 합산하고 첫 순서를 유지
                for k in ("tables", "cells", "paragraphs", "subheads"): rec[k] += prev[k]
                rec["order"] = prev["order"]
            per[nid][br] = rec
    ids = [r["id"] for r in reports]
    rows = []
    for nid in torder:
        if nid == "DT.A001": continue          # 루트(문서 자체)는 정렬 대상이 아니다
        got = per.get(nid)
        if not got and tnodes[nid].get("level", 9) > 2: continue
        n = tnodes[nid]
        titles = collections.Counter(v["title"] for v in (got or {}).values())
        present = [b for b in ids if b in (got or {})]
        rows.append({
            "node": nid, "level": n.get("level"), "title": n["title"], "scope": n.get("scope"),
            "present": present, "absent": [b for b in ids if b not in (got or {})],
            "coverage": f"{len(present)}/{len(ids)}",
            "class": "공통" if len(present) == len(ids) else ("일부" if len(present) > 1 else ("단독" if present else "미관찰")),
            "title_variants": [{"text": t, "n": c} for t, c in titles.most_common()],
            "per_report": {b: got[b] for b in present} if got else {},
            "order_consistent": len({tuple(sorted((b, per[x][b]["order"]) for b in present)) for x in [nid]}) == 1,
        })
    # 같은 depth 안에서 보고서별 출현 순서가 서로 같은지
    for lvl in (1, 2):
        seqs = {}
        for b in ids:
            seqs[b] = [r["node"] for r in sorted([x for x in rows if x["level"] == lvl and b in x["present"]],
                                                 key=lambda x: x["per_report"][b]["order"])]
        base = seqs[ids[0]]
        for r in rows:
            if r["level"] != lvl: continue
            bad = []
            for b in r["present"]:
                sub = [n for n in seqs[b] if n in base]
                if [n for n in base if n in seqs[b]] != sub: bad.append(b)
            r["order_conflict"] = bad
    out = {"reports": reports, "levels": {}, "rows": rows,
           "unmatched": {k: v for k, v in unmatched.items()},
           "summary": {}}
    for lvl in (1, 2, 3):
        sel = [r for r in rows if r["level"] == lvl]
        out["summary"][f"L{lvl}"] = {k: sum(1 for r in sel if r["class"] == k) for k in ("공통", "일부", "단독", "미관찰")}
        out["summary"][f"L{lvl}"]["총"] = len(sel)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"보고서 {len(reports)}건: " + ", ".join(f"{r['id']} {r['company']} {r['fiscal_year']}" for r in reports))
    for lvl in (1, 2, 3):
        s = out["summary"][f"L{lvl}"]
        print(f"  L{lvl}: 총 {s['총']} | 전건 공통 {s['공통']} · 일부 {s['일부']} · 단독 {s['단독']} · 미관찰 {s['미관찰']}")
    conf = [r for r in rows if r.get("order_conflict")]
    print(f"  순서 불일치 노드: {len(conf)}" + (" → " + ", ".join(f"{r['node']}({'/'.join(r['order_conflict'])})" for r in conf[:6]) if conf else ""))
    un = {k: len(v) for k, v in unmatched.items() if v}
    print(f"  템플릿 미대응 제목: {un or '없음'}")
    print("→", a.out)

if __name__ == "__main__":
    main()
