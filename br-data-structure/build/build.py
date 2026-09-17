# -*- coding: utf-8 -*-
"""
골격(skeleton/*.json)에 보고서 근거를 결합해 dist/skeleton.json 을 만든다.

입력
- inputs/reports/BRxxxx/structure.json  구조 조사 결과(build/survey_structure.py). 있으면 '조사됨'.
- inputs/reports/BRxxxx/identity.json   미취득 보고서 슬롯(식별·예상 변형·필요 자료).
- inputs/derived/sections_findings.json 초기 5건의 셀 단위 의미조사 발견(findings)과 절 귀속.
- inputs/derived/report_status.json     초기 5건 조사 상태와 문맥 유형 빈도.
- inputs/aggregate_a0002/, a0001/       통합판 유형·규칙 후보.

결합 규칙
- 각 보고서 목차 항목은 structure.json 의 node(템플릿 id)로 노드에 붙는다. 하위가 존재하면 상위도 존재로 집계한다.
- 발견은 sections_findings 의 절 인덱스(같은 wrapper 목차 순서)를 structure.json 의 node 로 바꿔 매단다.
- 표 카탈로그는 (노드, 정규화 캡션)으로 묶어 '관찰된 표 유형'을 만들고, L3 제목과 겹치지 않는 공통 유형을 개정 후보로 낸다.
"""
import json, os, re, collections, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SK = os.path.join(ROOT, "skeleton")
IN = os.path.join(ROOT, "inputs")
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def load_jsonl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]

template = load(os.path.join(SK, "data_tree_template.json"))
info = load(os.path.join(SK, "info_tree.json"))
mapping = load(os.path.join(SK, "mapping.json"))
obs = load(os.path.join(SK, "observation_schema.json"))
docmap = load(os.path.join(SK, "dart_document_map.json"))
observations = load(os.path.join(SK, "observations.json")) if os.path.exists(os.path.join(SK, "observations.json")) else {"items": {}, "meta": {}, "vocab": {}}
sections_findings = load(os.path.join(IN, "derived", "sections_findings.json"))
status = load(os.path.join(IN, "derived", "report_status.json"))
types_a = load_jsonl(os.path.join(IN, "aggregate_a0002", "type_catalog.jsonl"))
rules_a = load_jsonl(os.path.join(IN, "aggregate_a0002", "rule_candidates.jsonl"))
types_a0001 = {t["id"].split("/")[-1]: t for t in load_jsonl(os.path.join(IN, "aggregate_a0001", "type_catalog.jsonl"))}

# ---------------------------------------------------------------- reports roster
reports = {}
for d in sorted(glob.glob(os.path.join(IN, "reports", "BR*"))):
    br = os.path.basename(d)
    sp = os.path.join(d, "structure.json"); ip = os.path.join(d, "identity.json")
    if os.path.exists(sp):
        st = load(sp)
        ident = st["identity"]
        reports[br] = {"id": br, "company": ident.get("company"), "fiscal_year": ident.get("fiscal_year"), "receipt_id": ident.get("receipt_id"),
                       "sector": ident.get("sector"), "period": ident.get("period"), "surveyed": True, "structure": st,
                       "survey_depth": st.get("survey", {}).get("depth"), "html_sha256": ident.get("html_sha256")}
    elif os.path.exists(ip):
        ident = load(ip)
        reports[br] = dict(ident, id=br, surveyed=False, structure=None)
# 초기 5건의 의미조사 상태 병합
for br, stt in status["reports"].items():
    if br in reports:
        reports[br].update({"semantic_survey": {"work_state": stt["work_state"], "coverage": stt["coverage"], "outputs": stt["outputs"], "resume": stt["resume"]}})
        reports[br].setdefault("sector", stt.get("sector")); reports[br].setdefault("period", stt.get("period"))
G01_ORDER = ["BR0001", "BR0044", "BR0020", "BR0016", "BR0053", "BR0043", "BR0021", "BR0100", "BR0002", "BR0022", "BR0042", "BR0062", "BR0081", "BR0003", "BR0023", "BR0045", "BR0063", "BR0082", "BR0004", "BR0024"]
ORDER = [b for b in G01_ORDER if b in reports] + [b for b in sorted(reports) if b not in G01_ORDER]
SURVEYED = [b for b in ORDER if reports[b]["surveyed"]]
PENDING = [b for b in ORDER if not reports[b]["surveyed"]]

# ---------------------------------------------------------------- index template
nodes = {}
def index(n, parent=None):
    n["parent"] = parent; nodes[n["id"]] = n
    n["instances"] = {}; n["findings"] = []; n["rules"] = []; n["table_types"] = []
    for c in n["children"]:
        index(c, n["id"])
index(template["root"])

# ---------------------------------------------------------------- instance overlay from structure.json
for br in SURVEYED:
    st = reports[br]["structure"]
    for x in st["sections"]:
        nid = x.get("node")
        if not nid or nid not in nodes:
            continue
        if x.get("pos") is None:
            nodes[nid]["instances"].setdefault(br, {"present": False, "sections": [x["text"]], "counts": None, "subheads": [], "own": True})
            continue
        inst = nodes[nid]["instances"].setdefault(br, {"present": True, "sections": [], "counts": {"table": 0, "cell": 0, "paragraph": 0, "image": 0}, "subheads": [], "own": True})
        inst["sections"].append(x["text"])
        for k in inst["counts"]:
            inst["counts"][k] += (x.get("counts") or {}).get(k, 0) or 0
        inst["subheads"].extend(x.get("subheads") or [])
    nodes["DT.A001"]["instances"][br] = {"present": True, "sections": ["(문서 전체)"], "counts": None, "subheads": [], "own": True}

# 빈 절 판정
for n in nodes.values():
    for br, inst in n["instances"].items():
        if inst["present"] is True and inst["counts"] and sum(inst["counts"].values()) == 0:
            inst["present"] = "empty"

# 하위가 존재하면 상위도 존재(집계). 예: 보험업 XII.4.02 가 L3에 직접 대응된 경우 XII.4 도 존재.
def rollup_presence(n):
    for c in n["children"]:
        rollup_presence(c)
    for br in SURVEYED:
        if br in n["instances"]:
            continue
        kids = [c["instances"][br] for c in n["children"] if br in c["instances"] and c["instances"][br]["present"] in (True, "empty")]
        if kids:
            cnt = {"table": 0, "cell": 0, "paragraph": 0, "image": 0}
            for k in kids:
                for kk in cnt:
                    cnt[kk] += (k["counts"] or {}).get(kk, 0)
            n["instances"][br] = {"present": True if sum(cnt.values()) else "empty", "sections": sum((k["sections"] for k in kids), []), "counts": cnt, "subheads": [], "own": False}
rollup_presence(template["root"])

# 목차에 대응 절이 없는 템플릿 노드는 상위가 존재하면 '상위 절에 포함'. 형제 중 직접 대응된 것이 있으면 나머지는 '없음'.
def inherit_presence(n):
    for br in SURVEYED:
        if n["instances"].get(br, {}).get("present") is not True:
            continue
        sibling_matched = any(c["instances"].get(br, {}).get("present") in (True, "empty") for c in n["children"])
        if sibling_matched:
            continue
        for c in n["children"]:
            if br not in c["instances"]:
                c["instances"][br] = {"present": "within_parent", "sections": [], "counts": None, "subheads": [], "own": False}
    for c in n["children"]:
        inherit_presence(c)
inherit_presence(template["root"])

# 소제목 관찰 휴리스틱 (L3 leaf)
def key_terms(title):
    parts = re.split(r"[·/()（）,\s]", title)
    return [p for p in parts if len(p) >= 3][:4]
for n in nodes.values():
    if n["level"] == 3 and not n["children"]:
        parent = nodes[n["parent"]]; seen = {}; terms = key_terms(n["title"])
        for br, inst in parent["instances"].items():
            hits = [h for h in inst.get("subheads", []) if any(t in h for t in terms)]
            if hits:
                seen[br] = hits[:4]
        n["subhead_evidence"] = seen

# ---------------------------------------------------------------- table catalog -> table types
def norm_caption(c):
    if not c:
        return None
    for _ in range(3):   # '4. 주식의 분포 현황 가. 주식 소유 현황' 처럼 접두 번호가 겹치는 경우
        c = re.sub(r"^\s*(?:\(?\d{1,2}\)|\d{1,2}\)|\d{1,2}\.|[가-힣]\.|\d{1,2}-\d{1,2}\.|[①-⑳]|□|-|ㅇ|○|◦|■|가\)|나\)|다\)|라\)|마\))\s*", "", c)
    c = re.sub(r"\(.*?\)", "", c)            # 괄호 안 회사명 등 제거
    c = re.sub(r"[\s·ㆍ:：\[\]【】]", "", c)
    c = re.sub(r"(당사|회사|의|등|현황)$", "", c)
    return c[:40] if c else None

def header_sig(t):
    h = t.get("header_rows") or []
    if not h:
        return None
    return "hdr:" + "|".join(re.sub(r"[\s·ㆍ]", "", x) for x in h[0] if x)[:60]

tt = collections.defaultdict(lambda: {"reports": collections.OrderedDict(), "captions": collections.Counter(), "headers": collections.Counter(), "units": collections.Counter(), "n": 0, "merged": 0})
for br in SURVEYED:
    for t in reports[br]["structure"]["tables"]:
        if t["kind"] != "data" or not t.get("node"):
            continue
        key = (t["node"], norm_caption(t.get("caption")) or header_sig(t) or "(캡션 없음)")
        rec = tt[key]
        rec["reports"].setdefault(br, 0); rec["reports"][br] += 1
        rec["captions"][t.get("caption") or ""] += 1
        if t.get("header_rows"):
            rec["headers"][" | ".join(h for h in t["header_rows"][0] if h)[:160]] += 1
        if t.get("unit"):
            rec["units"][t["unit"][:40]] += 1
        rec["n"] += 1; rec["merged"] += 1 if t.get("merged") else 0
table_types = []
for (nid, key), rec in tt.items():
    row = {"node": nid, "key": key, "caption": rec["captions"].most_common(1)[0][0], "reports": list(rec["reports"].keys()), "count": rec["n"],
           "header": rec["headers"].most_common(1)[0][0] if rec["headers"] else "", "unit": rec["units"].most_common(1)[0][0] if rec["units"] else None,
           "merged_ratio": round(rec["merged"] / rec["n"], 2)}
    table_types.append(row)
    nodes[nid]["table_types"].append(row)
for n in nodes.values():
    n["table_types"].sort(key=lambda r: (-len(r["reports"]), -r["count"]))
# L3 개정 후보: 2개 이상 보고서에서 관찰되고 어느 L3 제목의 핵심어와도 겹치지 않는 표 유형
revision_candidates = []
for row in table_types:
    if len(row["reports"]) < 2 or row["key"] == "(캡션 없음)" or row["key"].startswith("hdr:"):
        continue
    n = nodes[row["node"]]
    pool = n["children"] if n["children"] else [n]
    key = row["key"]
    hit = any(any(t and t in key for t in key_terms(c["title"])) or any(t and t in c["title"].replace(" ", "") for t in [key[:4]]) for c in pool)
    if not hit:
        revision_candidates.append(dict(row, parent_title=n["title"]))
revision_candidates.sort(key=lambda r: (-len(r["reports"]), r["node"]))

# ---------------------------------------------------------------- findings (초기 5건 의미조사)
findings_index = {}
for br, r in sections_findings.items():
    if br not in reports or not reports[br]["surveyed"]:
        continue
    st_secs = reports[br]["structure"]["sections"]
    secs = r["sections"]
    for f in r["findings"]:
        fid = f"{br}/{f['id']}"; nid = None
        si = f.get("section_idx")
        if si is not None and si < len(st_secs) and norm_caption(st_secs[si]["text"]) == norm_caption(secs[si]["text"]):
            nid = st_secs[si].get("node")
            if nid is None:   # 미대응 L3 -> 상위 절
                for j in range(si - 1, -1, -1):
                    if st_secs[j]["level"] < st_secs[si]["level"] and st_secs[j].get("node"):
                        nid = st_secs[j]["node"]; break
        rec = {"id": fid, "report": br, "company": r["company"], "local_id": f["id"], "record_type": f.get("record_type"), "summary": f.get("summary"),
               "evidence": f.get("evidence") or [], "section_path": f.get("section_path") or [], "node": nid, "proposal": f.get("proposal")}
        findings_index[fid] = rec
        if nid:
            nodes[nid]["findings"].append(fid)

# ---------------------------------------------------------------- rules
rules = []
type_by_id = {t["id"]: t for t in types_a}
A0001_LABELS = {"T0001": "같은 표 안의 대상·연결범위 예외", "T0002": "계획·잠정·기말·지급 사건의 시간 역할", "T0003": "분모·산식이 다른 비율", "T0004": "투자·지배·기초자산의 다단 관계", "T0005": "반복 발생과 기재 충돌", "T0006": "열별 기준 전환과 미적용 정책", "T0007": "대시·공란·명시0·해당없음의 의미 분리"}
for rl in rules_a:
    tid = rl.get("type_id"); t = type_by_id.get(tid, {}); inherited = rl.get("inherited_from")
    if inherited and not t:
        t = types_a0001.get(inherited.split("/")[-1].replace("R", "T"), {}); tid = t.get("id", tid)
    rec = {"id": rl["id"], "type_id": tid, "label": t.get("label") or A0001_LABELS.get((inherited or "").split("/")[-1].replace("R", "T")),
           "definition": t.get("definition_draft"), "state": rl.get("state"), "application": rl.get("application") or t.get("definition_draft"),
           "rejection": rl.get("rejection") or t.get("counterexample_guard"), "failure_handling": rl.get("failure_handling"),
           "required_context": rl.get("required_context") or t.get("required_context") or [], "counterexample_guard": t.get("counterexample_guard"),
           "supporting": rl.get("supporting_discoveries") or t.get("local_discoveries") or [], "inherited_from": inherited, "nodes": []}
    for d in rec["supporting"]:
        m = re.match(r"(BR\d{4})/r\d+/finding/(.+)", d)
        if m:
            fr = findings_index.get(f"{m.group(1)}/{m.group(2)}")
            if fr and fr["node"]:
                rec["nodes"].append(fr["node"]); nodes[fr["node"]]["rules"].append(rl["id"])
    rec["nodes"] = sorted(set(rec["nodes"])); rules.append(rec)
for n in nodes.values():
    n["rules"] = sorted(set(n["rules"]))

# ---------------------------------------------------------------- mapping
info_nodes = {}
def index_it(n, parent=None):
    n["parent"] = parent; info_nodes[n["id"]] = n; n["data_topic"] = []; n["data_item"] = []
    for c in n["children"]:
        index_it(c, n["id"])
index_it(info["root"])
for n in nodes.values():
    n["mapping"] = {"topic": [], "item": []}
missing = []
for e in mapping["edges"]:
    d = e["data"]
    if d not in nodes:
        missing.append(d); continue
    for i in e["info"]:
        if i not in info_nodes:
            missing.append(i); continue
        nodes[d]["mapping"][e["level"]].append(i)
        (info_nodes[i]["data_topic"] if e["level"] == "topic" else info_nodes[i]["data_item"]).append(d)
if missing:
    print("WARNING unmatched mapping ids:", sorted(set(missing)))

# ---------------------------------------------------------------- 관측 카탈로그 부착
obs_missing = []
for nid, it in observations["items"].items():
    if nid not in nodes: obs_missing.append(nid); continue
    nodes[nid]["subitems"] = [{"code": g["code"], "title": g["title"], "observations": g["observations"]} for g in it["groups"] if g["title"]]
    nodes[nid]["observations"] = [dict(o, subitem=g["title"]) for g in it["groups"] for o in g["observations"]]
    nodes[nid]["observation_evidence"] = {"reports": it["evidence_reports"], "level": it["evidence_level"]}
if obs_missing: print("WARNING 관측 카탈로그의 미대응 노드:", obs_missing[:8])

# ---------------------------------------------------------------- roll-ups
def rollup(n):
    tot = collections.Counter()
    for f in n["findings"]:
        tot[findings_index[f]["report"]] += 1
    for c in n["children"]:
        tot.update(rollup(c))
    n["stats"] = {"findings_total": sum(tot.values()), "findings_by_report": dict(tot), "findings_here": len(n["findings"]), "rules_here": len(n["rules"]),
                  "reports_present": [br for br in SURVEYED if n["instances"].get(br, {}).get("present") is True],
                  "reports_empty": [br for br in SURVEYED if n["instances"].get(br, {}).get("present") == "empty"],
                  "table_types": len(n["table_types"]), "table_types_shared": sum(1 for r in n["table_types"] if len(r["reports"]) >= 2),
                  "observations_here": len(n.get("observations") or []), "subitems_here": len(n.get("subitems") or []),
                  "observations_total": len(n.get("observations") or []) + sum(c["stats"]["observations_total"] for c in n["children"])}
    return tot
rollup(template["root"])

def it_stats(n):
    items = set(n["data_item"]); topics = set(n["data_topic"])
    for c in n["children"]:
        ci, ct = it_stats(c); items |= ci; topics |= ct
    n["stats"] = {"findings_via_items": sum(nodes[d]["stats"]["findings_here"] for d in items),
                  "findings_via_all": sum(nodes[d]["stats"]["findings_here"] for d in (items | topics)),
                  "data_nodes_item": len(items), "data_nodes_topic": len(topics), "rolled_up": bool(n["children"])}
    return items, topics
it_stats(info["root"])

# 문맥 유형 정규화 집계
canon = {s: c["canonical"] for c in obs["context_relation_types"] for s in c["observed_synonyms"]}
ctx_counts = collections.defaultdict(collections.Counter); uncanon = collections.Counter()
for br, cc in status["context_type_counts"].items():
    for k, v in cc.items():
        (ctx_counts[canon[k]].__setitem__(br, ctx_counts[canon[k]][br] + v) if k in canon else uncanon.__setitem__(k, uncanon[k] + v))
for c in obs["context_relation_types"]:
    c["observed_count"] = dict(ctx_counts.get(c["canonical"], {})); c["observed_total"] = sum(ctx_counts.get(c["canonical"], {}).values())
obs["uncanonical_observed"] = dict(uncanon)

# 구조 조사 요약 (보고서별)
survey_summary = []
for br in ORDER:
    r = reports[br]
    if r["surveyed"]:
        st = r["structure"]; s = st["stats"]
        survey_summary.append({"id": br, "company": r["company"], "fiscal_year": r["fiscal_year"], "sector": r.get("sector"), "period": r.get("period"),
                               "receipt_id": r.get("receipt_id"), "surveyed": True, "sections": s["sections"], "aligned": s["aligned"], "unmatched": st["unmatched"],
                               "tables_total": s["tables_total"], "tables_data": sum(1 for t in st["tables"] if t["kind"] == "data"), "html_chars": st["identity"]["html_chars"],
                               "semantic": r.get("semantic_survey"), "depth": r.get("survey_depth")})
    else:
        survey_summary.append({"id": br, "company": r["company"], "fiscal_year": r["fiscal_year"], "sector": r.get("sector"), "period": r.get("period"),
                               "receipt_id": r.get("receipt_id"), "surveyed": False, "acquisition": r.get("acquisition"), "expected_variants": r.get("expected_variants", []),
                               "sampling_reason": r.get("sampling_reason"), "planned_depth": r.get("planned_depth")})

# ---------------------------------------------------------------- write
def strip_parent(n):
    n.pop("parent", None)
    for c in n["children"]:
        strip_parent(c)
strip_parent(template["root"]); strip_parent(info["root"])
out = {
    "meta": {"generated_utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z", "title": "사업보고서 공통 데이터체계 골격 v0.2",
             "reports": [{k: v for k, v in reports[br].items() if k != "structure"} for br in ORDER],
             "surveyed": SURVEYED, "pending": PENDING, "batch": status["batch"],
             "counts": {"data_nodes": len(nodes), "info_nodes": len(info_nodes), "mapping_edges": len(mapping["edges"]), "findings": len(findings_index), "rules": len(rules),
                        "reports_surveyed": len(SURVEYED), "reports_pending": len(PENDING), "table_types": len(table_types), "revision_candidates": len(revision_candidates),
                        "observations": observations.get("meta", {}).get("observation_count", 0), "subitems": observations.get("meta", {}).get("subitem_count", 0)}},
    "document_map": docmap, "data_tree": template["root"], "structure_layers": template["structure_layers"], "note_topics": template["note_topics"],
    "info_tree": info["root"], "skills": info["skills"], "mapping": {"levels": mapping["levels"], "rules": mapping["rules"], "edge_count": len(mapping["edges"])},
    "observation_schema": obs, "observation_catalog_meta": observations.get("meta", {}), "observation_vocab": observations.get("vocab", {}), "rules": rules, "findings": findings_index, "table_types": table_types, "revision_candidates": revision_candidates,
    "survey_summary": survey_summary,
}
p = os.path.join(DIST, "skeleton.json")
with open(p, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("관측", observations.get("meta", {}).get("observation_count", 0), "· 세분화 항목", observations.get("meta", {}).get("subitem_count", 0))
print("data nodes", len(nodes), "| info nodes", len(info_nodes), "| findings", len(findings_index), "located", sum(1 for f in findings_index.values() if f["node"]),
      "| rules", len(rules), "| surveyed", len(SURVEYED), "pending", len(PENDING), "| table types", len(table_types), "| revision candidates", len(revision_candidates))
print("written", p, os.path.getsize(p), "bytes")
