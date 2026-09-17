# -*- coding: utf-8 -*-
"""dist/skeleton.json -> dist/index.html (단일 파일, 오프라인, 외부 스크립트 없음)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIST = os.path.join(ROOT, "dist")
data = open(os.path.join(DIST, "skeleton.json"), encoding="utf-8").read().replace("</", "<\\/")

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>사업보고서 데이터체계 골격</title>
<meta name="description" content="DART 사업보고서 공통 데이터 트리, 정보 트리, 매핑에 5개 보고서의 실제 발견과 규칙 후보를 매단 골격 시각화">
<style>
:root{
  color-scheme:light;
  --bg:#f6f6f4; --surface:#fcfcfb; --surface-2:#f0efec; --line:#dedcd6; --line-2:#cfccc4;
  --text:#0b0b0b; --text-2:#52514e; --text-3:#7a7873;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s7:#4a3aa7; --s8:#e34948;
  --seq1:#cde2fb; --seq2:#9ec5f4; --seq3:#5598e7; --seq4:#256abf; --seq5:#104281;
  --good:#008300; --warn:#eda100; --serious:#e34948;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    color-scheme:dark;
    --bg:#141413; --surface:#1a1a19; --surface-2:#232321; --line:#33332f; --line-2:#44443f;
    --text:#ffffff; --text-2:#c3c2b7; --text-3:#8f8e86;
    --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s7:#9085e9; --s8:#e66767;
    --seq1:#184f95; --seq2:#256abf; --seq3:#3987e5; --seq4:#6da7ec; --seq5:#9ec5f4;
  }
}
:root[data-theme="dark"]{
  color-scheme:dark;
  --bg:#141413; --surface:#1a1a19; --surface-2:#232321; --line:#33332f; --line-2:#44443f;
  --text:#ffffff; --text-2:#c3c2b7; --text-3:#8f8e86;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s7:#9085e9; --s8:#e66767;
  --seq1:#184f95; --seq2:#256abf; --seq3:#3987e5; --seq4:#6da7ec; --seq5:#9ec5f4;
}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--text);font-family:"Pretendard","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;font-size:14px;line-height:1.55}
a{color:var(--s1)}
header{position:sticky;top:0;z-index:20;background:var(--surface);border-bottom:1px solid var(--line);padding:10px 16px}
header h1{font-size:17px;margin:0 0 2px;font-weight:700}
header .sub{color:var(--text-2);font-size:12.5px}
nav{display:flex;gap:4px;flex-wrap:wrap;margin-top:8px}
nav button{background:var(--surface-2);border:1px solid var(--line);color:var(--text);padding:6px 11px;border-radius:8px;cursor:pointer;font-size:13px}
nav button[aria-selected="true"]{background:var(--s1);border-color:var(--s1);color:#fff}
.theme{margin-left:auto;font-size:12px;color:var(--text-2);cursor:pointer;background:none;border:1px solid var(--line);border-radius:8px;padding:4px 8px}
main{padding:16px;max-width:1500px;margin:0 auto}
section.tab{display:none}section.tab.active{display:block}
h2{font-size:16px;margin:18px 0 8px}h3{font-size:14px;margin:14px 0 6px}
.muted{color:var(--text-2)}.small{font-size:12px}.mono{font-family:var(--mono);font-size:12px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:8px 0 14px}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.kpi .v{font-size:24px;font-weight:700;line-height:1.1}.kpi .l{color:var(--text-2);font-size:12px;margin-top:3px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:8px 0}
.layers{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px}
.layer{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px;position:relative}
.layer .t{font-weight:700;margin-bottom:6px}.layer .h{font-size:12.5px;color:var(--text-2)}.layer .r{font-size:12.5px;margin-top:8px;padding-top:8px;border-top:1px dashed var(--line)}
.layer.focus{border:2px solid var(--s1)}
.tgt{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:stretch;margin:8px 0}
.tgt .box{border-radius:10px;padding:10px 12px;border:1px solid var(--line);background:var(--surface-2)}
.tgt .box.d{border-left:5px solid var(--s1)}.tgt .box.i{border-left:5px solid var(--s3)}.tgt .box.m{border-left:5px solid var(--s2);align-self:center;min-width:220px}
.tgt .box b{display:block;margin-bottom:4px}
.docmap{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px}
.docgroup{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--surface)}
.docgroup .g{font-weight:700;font-size:13px;margin-bottom:4px}
.doc{font-size:12px;padding:2px 0;display:flex;gap:6px;align-items:center}
.doc .code{font-family:var(--mono);color:var(--text-3);width:38px}
.doc.hi{background:var(--seq1);border-radius:4px;padding:2px 4px;font-weight:700}
.tag{display:inline-block;font-size:11px;padding:1px 6px;border-radius:999px;border:1px solid var(--line-2);color:var(--text-2);margin-left:4px;vertical-align:middle;white-space:nowrap}
.tag.q{border-color:var(--s2);color:var(--s2)}.tag.x{border-color:var(--s7);color:var(--s7)}.tag.ind{border-color:var(--s4);color:var(--s4)}.tag.cond{border-style:dashed}
.tag.api{border-color:var(--s2);color:var(--s2)}.tag.xbrl{border-color:var(--s7);color:var(--s7)}
.split{display:grid;grid-template-columns:minmax(360px,1.1fr) minmax(360px,1fr);gap:14px}
@media(max-width:900px){.split{grid-template-columns:1fr}.detail{position:static;max-height:none}}
.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:6px 0 10px}
.toolbar input[type=search]{padding:6px 9px;border:1px solid var(--line-2);border-radius:8px;background:var(--surface);color:var(--text);min-width:220px}
.toolbar select,.toolbar button{padding:5px 9px;border:1px solid var(--line-2);border-radius:8px;background:var(--surface);color:var(--text);cursor:pointer}
.toolbar label{font-size:12.5px;color:var(--text-2);display:flex;gap:4px;align-items:center}
.tree{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:8px;max-height:78vh;overflow:auto}
.node{display:flex;align-items:center;gap:6px;padding:3px 6px;border-radius:6px;cursor:pointer;min-height:26px}
.node:hover{background:var(--surface-2)}.node.sel{background:var(--seq1);outline:1px solid var(--s1)}
.node .tog{width:16px;color:var(--text-3);font-family:var(--mono);flex:none;text-align:center}
.node .code{font-family:var(--mono);color:var(--text-3);font-size:11.5px;flex:none;min-width:34px}
.node .title{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.node.l0 .title{font-weight:700}.node.l1 .title{font-weight:700}.node.l2 .title{font-weight:600}
.node .pres{display:inline-flex;gap:2px;flex:none}
.node .pres i{width:9px;height:9px;border-radius:2px;border:1px solid var(--line-2);background:transparent;display:block}
.node .pres i.y{background:var(--s1);border-color:var(--s1)}.node .pres i.e{background:repeating-linear-gradient(45deg,var(--line-2) 0 2px,transparent 2px 4px)}.node .pres i.w{background:var(--seq1);border-color:var(--seq2)}
.node .pres i.hl{outline:2px solid var(--s2)}
.pill{flex:none;font-size:11px;font-family:var(--mono);padding:0 6px;border-radius:999px;min-width:26px;text-align:center;color:var(--text)}
.pill.f0{color:var(--text-3);border:1px solid var(--line)}.pill.f1{background:var(--seq1)}.pill.f2{background:var(--seq2)}.pill.f3{background:var(--seq3);color:#fff}.pill.f4{background:var(--seq4);color:#fff}
.pill.r{border:1px solid var(--s7);color:var(--s7)}
.kids{margin-left:14px;border-left:1px solid var(--line);padding-left:4px}
.detail{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;max-height:78vh;overflow:auto;position:sticky;top:110px}
.detail h3{margin-top:12px}
.nw{white-space:nowrap}
.sub{border-left:3px solid var(--accent);padding:2px 0 2px 9px;margin:8px 0}
.sub>.lab{font-weight:600;font-size:13px;margin-bottom:3px}
.detail .path{font-size:12px;color:var(--text-2);font-family:var(--mono)}
table{border-collapse:collapse;width:100%;font-size:12.5px}
th,td{border-bottom:1px solid var(--line);padding:5px 6px;text-align:left;vertical-align:top}
th{color:var(--text-2);font-weight:600;background:var(--surface-2)}
td.num,th.num{text-align:right;font-family:var(--mono)}
.finding{border-left:3px solid var(--s7);padding:6px 10px;margin:6px 0;background:var(--surface-2);border-radius:0 6px 6px 0;font-size:12.5px}
.finding .id{font-family:var(--mono);color:var(--text-3);font-size:11px}
.legend{display:flex;gap:12px;flex-wrap:wrap;font-size:12px;color:var(--text-2);margin:6px 0}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:middle;border:1px solid var(--line-2)}
.bar{display:flex;align-items:center;gap:8px;margin:3px 0;font-size:12.5px}
.bar .lab{width:170px;flex:none;text-align:right;color:var(--text-2)}
.bar .trk{flex:1;height:12px;background:var(--surface-2);border-radius:4px;position:relative}
.bar .fil{height:100%;background:var(--s1);border-radius:4px 4px 4px 4px}
.bar .val{width:70px;font-family:var(--mono);font-size:11.5px}
.heat td.c{text-align:center;font-family:var(--mono);font-size:11.5px;min-width:34px}
.rule{border:1px solid var(--line);border-left:4px solid var(--s7);border-radius:8px;padding:10px 12px;margin:8px 0;background:var(--surface)}
.rule .lab{font-weight:700}.rule .st{font-size:11px;color:var(--text-3);font-family:var(--mono)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:900px){.grid2{grid-template-columns:1fr}}
.chip{display:inline-block;background:var(--surface-2);border:1px solid var(--line);border-radius:6px;padding:1px 6px;font-size:11.5px;margin:2px 3px 2px 0;cursor:pointer}
.chip.it{border-color:var(--s3)}.chip.dt{border-color:var(--s1)}
.note{font-size:12.5px;color:var(--text-2);border-left:3px solid var(--line-2);padding-left:8px;margin:6px 0}
details{margin:4px 0}summary{cursor:pointer;color:var(--text-2);font-size:12.5px}
.sk{display:inline-block;font-size:10.5px;padding:0 5px;border-radius:4px;background:var(--surface-2);border:1px solid var(--line);color:var(--text-2);margin-left:3px}
.status-good{color:var(--good)}.status-warn{color:var(--warn)}.status-bad{color:var(--serious)}
footer{color:var(--text-3);font-size:12px;padding:20px 16px;text-align:center}
@media(max-width:600px){.node .pres{display:none}.node .code{min-width:24px}main{padding:12px}header{padding:8px 12px}}
</style>
</head>
<body>
<header>
  <h1>사업보고서 공통 데이터체계 골격 <span class="muted small" id="meta-title"></span></h1>
  <div class="sub" id="meta-sub"></div>
  <nav id="nav">
    <button data-tab="overview" aria-selected="true">① 전체 구조</button>
    <button data-tab="dtree">② 데이터 트리(골격+살)</button>
    <button data-tab="itree">③ 정보 트리</button>
    <button data-tab="map">④ 매핑</button>
    <button data-tab="obs">⑤ 관측 규약·규칙</button>
    <button data-tab="tables">⑥ 표 유형·개정 후보</button>
    <button data-tab="basis">⑦ 근거·한계·진행</button>
    <button class="theme" id="theme">테마</button>
  </nav>
</header>
<main>
<section class="tab active" id="tab-overview">
  <div class="kpis" id="kpis"></div>
  <h2>서비스 전체 파이프라인 위에서 골격이 놓이는 자리</h2>
  <div class="layers" id="layers"></div>
  <h2>TGT 두 트리와 매핑 (DWH 층의 논리 구조)</h2>
  <div class="tgt">
    <div class="box d"><b>Data Tree · 원문 포함 트리</b>DART 문서유형 → 사업보고서(A001) → 장 → 절 → 항목·표 유형 → 표/문단/그림 → 셀·문장. 포함관계만 그리며 단일 부모. 서식 정의 노드(템플릿)와 보고서별 실제 노드(인스턴스)를 타입으로 구분.<div class="small muted" id="dt-count"></div></div>
    <div class="box m"><b>Mapping · 2수준 대응</b>주제 연결(topic)과 항목 대응(item)만 둔다. 대응은 sameAs·합산·계산을 뜻하지 않는다.<div class="small muted" id="map-count"></div></div>
    <div class="box i"><b>Info Tree · 단일 부모 분류</b>기업 식별 / 지배구조·인력 / 주주·자본 / 사업 / 재무 / 자금조달 / 관계·거래 / 리스크·법규 / 감사·내부통제 / MD&amp;A / 외부 시장데이터. 기업·기간·통화는 노드가 아니라 관측의 문맥.<div class="small muted" id="it-count"></div></div>
  </div>
  <div class="note">계산식·인과·기업 간 비교는 두 트리에 넣지 않고 요청별 분석 작업지와 스킬에서 다룬다(TGT 4.4, 11.4). 관측값에는 주체·시간·범위·단위·기준·상태·조건이 붙는다(⑤ 관측 규약).</div>
  <h2>DART 공시 문서 맵 (사업보고서가 놓이는 상위 맥락)</h2>
  <div class="legend"><span><i style="background:var(--seq1)"></i>이번 골격에서 상세화한 문서</span><span class="tag q">Q</span> 항목 API 존재 <span class="tag x">X</span> XBRL 존재 · 출처: 방향성 PPT 슬라이드 11(초안)</div>
  <div class="docmap" id="docmap"></div>
</section>

<section class="tab" id="tab-dtree">
  <div class="toolbar">
    <input type="search" id="q" placeholder="노드·발견 검색 (예: 지급보증, 배당, K-ICS)">
    <select id="f-scope"><option value="">범위: 전체</option><option value="common">공통</option><option value="industry">업종 변형</option><option value="conditional">조건부</option></select>
    <select id="f-report"><option value="">보고서 강조: 없음</option></select>
    <label><input type="checkbox" id="f-find"> 발견이 있는 노드만</label>
    <label><input type="checkbox" id="f-rule"> 규칙이 매달린 노드만</label>
    <button id="exp">전부 펼치기</button><button id="col">2단계까지</button>
  </div>
  <div class="legend">
    <span><i style="background:var(--s1);border-color:var(--s1)"></i>보고서에 존재(내용 있음)</span>
    <span><i style="background:repeating-linear-gradient(45deg,var(--line-2) 0 2px,transparent 2px 4px)"></i>제목만 있고 비어 있음</span>
    <span><i style="background:var(--seq1);border-color:var(--seq2)"></i>상위 절에 포함(개별 존재 미판정)</span>
    <span><i></i>없음/미대응</span>
    <span id="strip-legend"></span>
    <span>· 파란 알약 = 하위 포함 발견 건수(1–2 / 3–9 / 10–29 / 30+)</span>
    <span>· 보라 알약 = 매달린 규칙 후보 수</span>
  </div>
  <div class="split">
    <div class="tree" id="dtree"></div>
    <div class="detail" id="ddetail"><div class="muted">왼쪽 트리에서 노드를 선택하세요.</div></div>
  </div>
</section>

<section class="tab" id="tab-itree">
  <div class="legend"><span>알약 = 항목 대응 데이터 노드 수 / 주제 연결 데이터 노드 수 (상위 노드는 하위 합산)</span><span>· 스킬 배지 = 이 정보를 요구하는 분석 스킬(TGT 12장)</span></div>
  <div class="split">
    <div class="tree" id="itree"></div>
    <div class="detail" id="idetail"><div class="muted">정보 노드를 선택하면 대응된 데이터 트리 노드와 근거가 나타납니다.</div></div>
  </div>
</section>

<section class="tab" id="tab-map">
  <h2>장(章) × 정보 도메인 대응 밀도</h2>
  <div class="legend"><span>셀 = 대응 간선 수(항목+주제). 단일 색조 순차 램프.</span></div>
  <div class="card" style="overflow:auto"><table class="heat" id="heat"></table></div>
  <h2>대응 간선 목록</h2>
  <div class="toolbar"><select id="m-level"><option value="">수준: 전체</option><option value="item">항목 대응 후보</option><option value="topic">주제 연결</option></select><input type="search" id="m-q" placeholder="검색"></div>
  <div class="card" style="overflow:auto;max-height:70vh"><table id="edges"></table></div>
</section>

<section class="tab" id="tab-obs">
  <h2>관측 한 건의 최소 설명 (모든 leaf에 붙는 살)</h2>
  <div class="card"><table id="fields"></table></div>
  <div class="grid2">
    <div>
      <h2>문맥 유형: 관찰 빈도와 어휘 정규화</h2>
      <div class="legend"><span>5개 보고서 contexts.jsonl 의 relation_type 합계. 두 작성자가 다른 어휘를 써서 정규화가 필요.</span></div>
      <div class="card" id="ctxbars"></div>
    </div>
    <div>
      <h2>상태 어휘와 비교 허용 순서</h2>
      <div class="card" id="vocab"></div>
    </div>
  </div>
  <h2>규칙 후보 (통합판 a0002) — 어느 노드에 매달리는가</h2>
  <div id="rules"></div>
  <h2>주석 주제 유형 (III.3 / III.5 의 L3)</h2>
  <div class="card" style="overflow:auto"><table id="notetopics"></table></div>
</section>

<section class="tab" id="tab-tables">
  <h2>골격 아래에서 관찰된 표 유형</h2>
  <div class="legend"><span>구조 조사에서 수집한 데이터 표를 (노드, 정규화 캡션)으로 묶은 것. 머리글 행이 표 유형의 관측 단위(grain)를 보여준다.</span></div>
  <div class="toolbar"><input type="search" id="t-q" placeholder="노드·캡션·머리글 검색"><label><input type="checkbox" id="t-shared" checked> 2개 이상 보고서에서 관찰된 유형만</label><select id="t-node"><option value="">장: 전체</option></select></div>
  <div class="card" style="overflow:auto;max-height:60vh"><table id="ttypes"></table></div>
  <h2>L3 개정 후보</h2>
  <div class="legend"><span>2개 이상 보고서에서 같은 캡션으로 관찰됐지만 템플릿 L3 제목의 핵심어와 겹치지 않는 표 유형. 골격에 항목을 추가하거나 별칭을 달 후보.</span></div>
  <div class="card" style="overflow:auto"><table id="revs"></table></div>
</section>

<section class="tab" id="tab-basis">
  <h2>G01 20건 진행 현황: 조사됨 / 미취득</h2>
  <div class="kpis" id="prog-kpis"></div>
  <div class="card" style="overflow:auto"><table id="reports"></table></div>
  <h3>미취득 15건: 왜 못 했고 무엇이 필요한가</h3>
  <div class="card small" id="pending-note"></div>
  <div class="card" style="overflow:auto"><table id="pending"></table></div>
  <div class="grid2">
    <div class="card"><h3>확정한 것</h3><ul class="small">
      <li>사업보고서 L1(장)·L2(절) 구조: 5개 보고서 wrapper 목차에서 동일하게 확인. 금융업(보험)의 II장 절 구성만 다르다.</li>
      <li>정보 트리 v0의 11개 도메인과 90개 노드: 단일 부모, 형제 MECE를 원칙으로 초안 확정.</li>
      <li>매핑 2수준(주제/항목)과 266개 간선: 서식 수준 대응. 셀 단위 확정은 파이프라인 인스턴스 단계.</li>
      <li>발견 1,013건 전부를 원문 위치로 절에 귀속(단, 미귀속 1건). 규칙 후보 13개를 발견 경로로 노드에 연결.</li>
    </ul></div>
    <div class="card"><h3>초안·미검증인 것</h3><ul class="small">
      <li>L3(항목·표 유형)은 5개 보고서 소제목 관찰 + 서식 지식으로 작성. 다른 업종(은행·증권·건설·지주 등)의 변형은 미관찰.</li>
      <li>API/XBRL 대응 표시는 OpenDART 명세 참조이며 실제 호출·대조로 검증하지 않음.</li>
      <li>주석 L3는 '주제 유형'이며 키워드 대응. 회사별 주석 제목이 두 주제에 걸칠 수 있다.</li>
      <li>보고서별 '존재/비어있음'은 절 범위의 표·문단 존재로 판정한 물리적 사실이며 의미 검토 완료가 아니다.</li>
      <li>5개 표본 모두 전수 의미조사 미완료(3 paused, 2 blocked). 통계적 대표성 없음.</li>
    </ul></div>
  </div>
  <h2>방법</h2>
  <div class="card small" id="method"></div>
</section>
</main>
<footer>사업보고서 공통 데이터체계 골격 v0.1 · 원문·조사 산출물은 별도 패키지에 보존. 이 페이지는 신규 원문 조사나 외부 조회를 수행하지 않는다.</footer>
<script type="application/json" id="data">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const RPT = D.meta.reports; const ORDER = D.meta.surveyed; const PENDING = D.meta.pending;
const RB = Object.fromEntries(RPT.map(r=>[r.id, r]));
const RN = Object.fromEntries(RPT.map(r=>[r.id, r.company+' '+String(r.fiscal_year).slice(2)]));
const fmt = n => (n==null?'–':Number(n).toLocaleString('ko-KR'));
const esc = s => String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
// ---------- index
const DN={}, DP={}; (function idx(n,p){DN[n.id]=n; DP[n.id]=p; n.children.forEach(c=>idx(c,n.id));})(D.data_tree,null);
const IN={}, IP={}; (function idx(n,p){IN[n.id]=n; IP[n.id]=p; n.children.forEach(c=>idx(c,n.id));})(D.info_tree,null);
const pathOf = (id,map,parent)=>{const a=[];let c=id;while(c){a.unshift(map[c]);c=parent[c];}return a;};
const dpath = id => pathOf(id,DN,DP).map(n=>n.code).join(' › ');
const dlabel = id => { const n=DN[id]; return (n.level>=2? n.code+' ' : '') + n.title; };
// ---------- tabs
document.querySelectorAll('#nav button[data-tab]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('#nav button[data-tab]').forEach(x=>x.setAttribute('aria-selected',x===b));document.querySelectorAll('section.tab').forEach(s=>s.classList.toggle('active',s.id==='tab-'+b.dataset.tab));}));
document.getElementById('theme').addEventListener('click',()=>{const r=document.documentElement;const cur=r.getAttribute('data-theme');const dark=cur?cur==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.setAttribute('data-theme',dark?'light':'dark');});
function showTab(t){document.querySelector('#nav button[data-tab="'+t+'"]').click();}
// ---------- overview
document.getElementById('meta-title').textContent = D.meta.title.replace('사업보고서 공통 데이터체계 골격','');
document.getElementById('meta-sub').textContent = `생성 ${D.meta.generated_utc} · 구조 조사 ${ORDER.map(r=>RN[r]).join(', ')} · 미취득 ${PENDING.length}건 · 데이터 노드 ${D.meta.counts.data_nodes} · 정보 노드 ${D.meta.counts.info_nodes} · 대응 ${D.meta.counts.mapping_edges} · 발견 ${fmt(D.meta.counts.findings)} · 표 유형 ${fmt(D.meta.counts.table_types)} · 관측 ${fmt(D.meta.counts.observations)}`;
const kp=[[D.meta.counts.data_nodes,'데이터 트리 노드(서식 정의)'],[D.meta.counts.info_nodes,'정보 트리 노드'],[D.meta.counts.mapping_edges,'대응 간선(주제+항목)'],[D.meta.counts.findings,'노드에 매단 발견(의미조사 5건)'],[D.meta.counts.observations,'항목에 정의한 관측'],[D.meta.counts.table_types,'관찰된 표 유형(구조조사)'],[`${ORDER.length} / ${ORDER.length+PENDING.length}`,'G01 구조 조사 완료 / 표본']];
document.getElementById('kpis').innerHTML = kp.map(([v,l])=>`<div class="kpi"><div class="v">${fmt(v)}</div><div class="l">${l}</div></div>`).join('');
document.getElementById('layers').innerHTML = D.document_map.service_layers.map((l,i)=>`<div class="layer ${i===1?'focus':''}"><div class="t">${i+1}. ${esc(l.layer)}</div><div class="h">${esc(l.holds)}</div><div class="r"><b>골격의 역할</b> ${esc(l.tree_role)}</div></div>`).join('');
document.getElementById('dt-count').textContent = `템플릿 ${D.meta.counts.data_nodes}개 노드 · L1 ${Object.values(DN).filter(n=>n.level===1).length} · L2 ${Object.values(DN).filter(n=>n.level===2).length} · L3 ${Object.values(DN).filter(n=>n.level===3).length}`;
document.getElementById('map-count').textContent = `${D.meta.counts.mapping_edges}개 간선`;
document.getElementById('it-count').textContent = `${D.meta.counts.info_nodes}개 노드 · 도메인 ${D.info_tree.children.length}`;
document.getElementById('docmap').innerHTML = D.document_map.groups.map(g=>`<div class="docgroup"><div class="g">${g.code}. ${esc(g.title)} <span class="muted small">(${g.docs.length})</span></div>${g.docs.map(d=>`<div class="doc ${d[3]==='detailed'?'hi':''}"><span class="code">${d[0]}</span><span>${esc(d[1])}</span>${d[2].map(t=>`<span class="tag ${t[0]==='Q'?'q':'x'}">${t}</span>`).join('')}</div>`).join('')}</div>`).join('');
// ---------- data tree
const fsel=document.getElementById('f-report'); ORDER.forEach(id=>{const o=document.createElement('option');o.value=id;o.textContent='보고서 강조: '+RN[id];fsel.appendChild(o);});
document.getElementById('strip-legend').textContent = `· ${ORDER.length}칸 순서: ${ORDER.map(r=>RN[r]).join(' · ')}`;
const open = new Set(); Object.values(DN).forEach(n=>{ if(n.level<=1) open.add(n.id); });
let sel=null, hl='';
function presence(n){ return ORDER.map(id=>{const p=(n.instances[id]||{}).present; return `<i class="${p===true?'y':(p==='empty'?'e':(p==='within_parent'?'w':''))} ${hl===id?'hl':''}" title="${RN[id]}: ${p===true?'존재':(p==='empty'?'제목만 있고 비어 있음':(p==='within_parent'?'상위 절에 포함(개별 존재 미판정)':'없음/미대응'))}"></i>`;}).join(''); }
function fpill(n){const v=n.stats.findings_total; const c=v===0?'f0':v<3?'f1':v<10?'f2':v<30?'f3':'f4'; return `<span class="pill ${c}" title="하위 포함 발견 ${v}건">${v}</span>`;}
function matches(n,q,scope,onlyF,onlyR){
  const self = (!q || (n.title+' '+(n.note||'')+' '+(n.grain||'')+' '+(n.observations||[]).map(o=>o.name+' '+(o.axis||'')).join(' ')+' '+n.findings.map(f=>D.findings[f].summary).join(' ')).toLowerCase().includes(q))
     && (!scope || (scope==='industry'? n.scope.startsWith('industry') : n.scope===scope))
     && (!onlyF || n.stats.findings_total>0) && (!onlyR || n.rules.length>0 || n.children.some(c=>c.rules.length));
  return self;
}
function renderDTree(){
  const q=document.getElementById('q').value.trim().toLowerCase(), scope=document.getElementById('f-scope').value, onlyF=document.getElementById('f-find').checked, onlyR=document.getElementById('f-rule').checked;
  function vis(n){ if(matches(n,q,scope,onlyF,onlyR)) return true; return n.children.some(vis); }
  function rec(n){
    if(!vis(n)) return '';
    const kids=n.children.filter(vis);
    const isOpen = open.has(n.id) || (q&&kids.length);
    const tags = (n.scope.startsWith('industry')?`<span class="tag ind">${n.scope.split(':')[1]}</span>`:'') + (n.scope==='conditional'?`<span class="tag cond">조건부</span>`:'') + (n.api&&n.api.length?`<span class="tag api" title="${esc(n.api.join(', '))}">API</span>`:'') + (n.xbrl?`<span class="tag xbrl">XBRL</span>`:'');
    return `<div><div class="node l${n.level} ${sel===n.id?'sel':''}" data-id="${n.id}"><span class="tog" data-tog="${n.id}">${kids.length?(isOpen?'−':'+'):'·'}</span><span class="code">${n.level>=2?esc(n.code):''}</span><span class="title" title="${esc(n.title)}">${esc(n.title)}${tags}</span><span class="pres">${presence(n)}</span>${fpill(n)}${n.rules.length?`<span class="pill r" title="규칙 후보 ${n.rules.length}">R${n.rules.length}</span>`:''}</div>${(isOpen&&kids.length)?`<div class="kids">${kids.map(rec).join('')}</div>`:''}</div>`;
  }
  document.getElementById('dtree').innerHTML = rec(D.data_tree);
}
document.getElementById('dtree').addEventListener('click',e=>{
  const t=e.target.closest('[data-tog]'); if(t){const id=t.dataset.tog; open.has(id)?open.delete(id):open.add(id); renderDTree(); return;}
  const nd=e.target.closest('.node'); if(nd){ selectD(nd.dataset.id); }
});
['q','f-scope','f-find','f-rule'].forEach(id=>document.getElementById(id).addEventListener('input',renderDTree));
fsel.addEventListener('change',()=>{hl=fsel.value;renderDTree();});
document.getElementById('exp').addEventListener('click',()=>{Object.keys(DN).forEach(id=>open.add(id));renderDTree();});
document.getElementById('col').addEventListener('click',()=>{open.clear();Object.values(DN).forEach(n=>{if(n.level<=1)open.add(n.id);});renderDTree();});
function selectD(id, jump){
  sel=id; let p=DP[id]; while(p){open.add(p);p=DP[p];} renderDTree();
  const n=DN[id];
  const inst = ORDER.map(r=>{const i=n.instances[r]; if(!i) return `<tr><td>${RN[r]}</td><td class="muted">없음/미대응</td><td class="num">–</td><td class="num">–</td><td class="num">–</td><td></td></tr>`;
    const c=i.counts||{}; const sh=(i.subheads||[]).slice(0,10);
    return `<tr><td>${RN[r]}</td><td>${i.present===true?'<span class="status-good">존재</span>':(i.present==='empty'?'<span class="status-warn">제목만</span>':(i.present==='within_parent'?'<span class="muted">상위 절에 포함</span>':'<span class="status-bad">없음</span>'))}</td><td class="num">${fmt(c.table)}</td><td class="num">${fmt(c.cell)}</td><td class="num">${fmt(c.paragraph)}</td><td class="small">${esc((i.sections||[]).join(' / '))}${sh.length?`<details><summary>관찰된 소제목 ${i.subheads.length}개</summary>${sh.map(esc).join('<br>')}${i.subheads.length>10?'<br>…':''}</details>`:''}</td></tr>`;}).join('');
  const fl = n.findings.map(f=>D.findings[f]);
  const subF = n.children.length? n.stats.findings_total - n.stats.findings_here : 0;
  const maps = ['item','topic'].map(l=> n.mapping[l].length? `<div><b>${l==='item'?'항목 대응 후보':'주제 연결'}</b> ${n.mapping[l].map(i=>`<span class="chip it" data-it="${i}">${esc(IN[i].code)} ${esc(IN[i].title)}</span>`).join('')}</div>`:'' ).join('');
  const rules = n.rules.map(r=>D.rules.find(x=>x.id===r)).map(r=>`<div class="rule"><div class="lab">${esc(r.label)} <span class="st">${r.id.split('/').pop()} · ${esc(r.state)}</span></div><div class="small">${esc(r.application||r.definition||'')}</div></div>`).join('');
  const she = n.subhead_evidence && Object.keys(n.subhead_evidence).length ? `<h3>소제목 관찰(휴리스틱)</h3><div class="small">${Object.entries(n.subhead_evidence).map(([r,h])=>`<div><b>${RN[r]}</b>: ${h.map(esc).join(' · ')}</div>`).join('')}</div>`:'';
  const obsRows = (o)=>`<tr><td><b>${esc(o.name)}</b></td><td class="small nw">${esc(o.type)}</td><td class="small nw">${esc(o.unit||'')}</td><td class="small">${esc(o.axis||'')}</td><td class="small">${esc(o.time||'')}</td><td class="small">${esc(o.basis||'')}</td><td class="small muted">${esc(o.note||'')}</td></tr>`;
  const obsHead = `<tr><th>관측명(측정량)</th><th>유형</th><th>단위</th><th>관측 축</th><th>시간</th><th>범위·기준</th><th>조건·주의</th></tr>`;
  let obsHtml='';
  if((n.observations||[]).length){
    const ev = n.observation_evidence||{};
    const evTxt = (ev.reports&&ev.reports.length)? `근거 ${ev.reports.map(r=>RN[r]).join(', ')}${ev.level==='절'?' (절 단위 확인)':''}` : '근거: 기업공시서식 기준(초안)';
    if((n.subitems||[]).length){
      obsHtml = `<h3>관측 ${n.observations.length} <span class="small muted">· 하위 항목 ${n.subitems.length}개로 세분 · ${evTxt}</span></h3>`
        + n.subitems.map(g=>`<div class="sub"><div class="lab">${esc(g.code)}. ${esc(g.title)} <span class="small muted">(관측 ${g.observations.length})</span></div><table>${obsHead}${g.observations.map(obsRows).join('')}</table></div>`).join('');
    } else {
      obsHtml = `<h3>관측 ${n.observations.length} <span class="small muted">· ${evTxt}</span></h3><table>${obsHead}${n.observations.map(obsRows).join('')}</table>`;
    }
  }
  const tts = (n.table_types||[]).slice(0,25);
  const ttHtml = tts.length? `<h3>관찰된 표 유형 ${n.table_types.length}${n.table_types.length>25?' (상위 25)':''}</h3><table><tr><th>캡션(대표)</th><th>보고서</th><th>머리글(대표)</th><th>단위</th><th class="num">건</th></tr>${tts.map(t=>`<tr><td>${esc(t.caption||'(캡션 없음)')}</td><td class="small">${t.reports.map(r=>RN[r]).join(', ')}</td><td class="small mono">${esc(t.header)}</td><td class="small">${esc(t.unit||'')}</td><td class="num">${t.count}</td></tr>`).join('')}</table>`:'';
  document.getElementById('ddetail').innerHTML = `
    <div class="path">${esc(dpath(id))}</div>
    <h2 style="margin:4px 0 6px">${esc(n.title)} <span class="tag">${esc(n.scope)}</span> ${n.structures.map(s=>`<span class="tag">${esc(s)}</span>`).join('')}</h2>
    ${n.aliases.length?`<div class="small muted">별칭: ${n.aliases.map(esc).join(' / ')}</div>`:''}
    ${n.grain?`<div><b>관측 단위(grain)</b> <span class="small">${esc(n.grain)}</span></div>`:''}
    ${n.contexts.length?`<div><b>필수 문맥</b> ${n.contexts.map(c=>`<span class="chip">${esc(c)}</span>`).join('')}</div>`:''}
    ${n.api.length?`<div><b>OpenDART API 대응 후보</b> ${n.api.map(a=>`<span class="chip">${esc(a)}</span>`).join('')} <span class="small muted">(명세 참조, 미검증)</span></div>`:''}
    ${n.xbrl?`<div><b>XBRL</b> <span class="small">${n.xbrl===true?'재무제표 태깅 대응':'부분(태깅 주석 범위에 한함)'}</span></div>`:''}
    ${n.note?`<div class="note">${esc(n.note)}</div>`:''}
    ${obsHtml}
    <h3>정보 트리 대응</h3>${maps||'<div class="small muted">직접 대응 없음(하위 노드 참조)</div>'}
    <h3>5개 보고서 인스턴스</h3><table><tr><th>보고서</th><th>존재</th><th class="num">표</th><th class="num">셀</th><th class="num">문단</th><th>원문 절 / 소제목</th></tr>${inst}</table>
    ${she}
    ${ttHtml}
    <h3>규칙 후보 ${n.rules.length}</h3>${rules||'<div class="small muted">이 노드에 직접 매달린 규칙 없음</div>'}
    <h3>발견 ${fl.length}${subF?` <span class="small muted">(하위 노드에 ${subF}건 더)</span>`:''}</h3>
    ${fl.slice(0,60).map(f=>`<div class="finding"><div class="id">${f.company} · ${f.local_id} · ${esc(f.record_type||'')} · ${f.evidence.slice(0,3).join(', ')}</div>${esc(f.summary)}${f.proposal?`<details><summary>제안</summary>${esc(f.proposal)}</details>`:''}</div>`).join('')}${fl.length>60?`<div class="small muted">… ${fl.length-60}건 더</div>`:''}`;
  document.getElementById('ddetail').querySelectorAll('[data-it]').forEach(el=>el.addEventListener('click',()=>{showTab('itree');selectI(el.dataset.it);}));
  if(jump){ const el=document.querySelector(`#dtree .node[data-id="${CSS.escape(id)}"]`); if(el) el.scrollIntoView({block:'center'}); }
}
// ---------- info tree
const iopen=new Set(); Object.values(IN).forEach(n=>{if(n.level<=1) iopen.add(n.id);});
let isel=null;
function renderITree(){
  function rec(n){
    const kids=n.children; const o=iopen.has(n.id);
    const sk=(n.skills||[]).map(s=>`<span class="sk">${esc(D.skills[s]||s)}</span>`).join('');
    return `<div><div class="node l${n.level} ${isel===n.id?'sel':''}" data-id="${n.id}"><span class="tog" data-tog="${n.id}">${kids.length?(o?'−':'+'):'·'}</span><span class="code">${n.level>=1?esc(n.code):''}</span><span class="title" title="${esc(n.title)}">${esc(n.title)}${n.external?'<span class="tag">DART 외</span>':''}${sk}</span><span class="pill ${n.stats.data_nodes_item?'f2':'f0'}" title="항목 대응 ${n.stats.data_nodes_item} / 주제 연결 ${n.stats.data_nodes_topic}">${n.stats.data_nodes_item}/${n.stats.data_nodes_topic}</span></div>${(o&&kids.length)?`<div class="kids">${kids.map(rec).join('')}</div>`:''}</div>`;
  }
  document.getElementById('itree').innerHTML = rec(D.info_tree);
}
document.getElementById('itree').addEventListener('click',e=>{const t=e.target.closest('[data-tog]'); if(t){const id=t.dataset.tog; iopen.has(id)?iopen.delete(id):iopen.add(id); renderITree(); return;} const nd=e.target.closest('.node'); if(nd) selectI(nd.dataset.id);});
function selectI(id){
  isel=id; let p=IP[id]; while(p){iopen.add(p);p=IP[p];} renderITree();
  const n=IN[id];
  const lst=(ids,l)=> ids.length? `<table><tr><th>데이터 노드</th><th class="num">발견</th><th>보고서 존재</th></tr>${ids.map(d=>{const x=DN[d];return `<tr><td><span class="chip dt" data-dt="${d}">${esc(dpath(d))}</span> ${esc(x.title)}</td><td class="num">${x.stats.findings_total}</td><td><span class="pres">${ORDER.map(r=>`<i class="${(x.instances[r]||{}).present===true?'y':((x.instances[r]||{}).present==='empty'?'e':'')}"></i>`).join('')}</span></td></tr>`;}).join('')}</table>`:'<div class="small muted">없음</div>';
  const kids = n.children.length? `<div class="small muted">하위 ${n.children.length}개 노드가 각각 대응을 가진다.</div>`:'';
  document.getElementById('idetail').innerHTML=`<div class="path">${esc(pathOf(id,IN,IP).map(x=>x.code).join(' › '))}</div><h2 style="margin:4px 0 6px">${esc(n.title)}</h2>${n.desc?`<div class="note">${esc(n.desc)}</div>`:''}<div><b>요구 스킬</b> ${(n.skills||[]).map(s=>`<span class="chip">${esc(D.skills[s]||s)}</span>`).join('')||'<span class="small muted">–</span>'}</div>${kids}<h3>항목 대응 후보 (${n.data_item.length})</h3>${lst(n.data_item,'item')}<h3>주제 연결 (${n.data_topic.length})</h3>${lst(n.data_topic,'topic')}`;
  document.getElementById('idetail').querySelectorAll('[data-dt]').forEach(el=>el.addEventListener('click',()=>{showTab('dtree');selectD(el.dataset.dt,true);}));
}
// ---------- mapping
(function(){
  const chapters=D.data_tree.children.filter(c=>c.level===1); const domains=D.info_tree.children;
  const cnt={}; let mx=0;
  Object.values(DN).forEach(n=>{ const ch=pathOf(n.id,DN,DP)[1]; if(!ch) return; ['item','topic'].forEach(l=>n.mapping[l].forEach(i=>{const dom=pathOf(i,IN,IP)[1]; if(!dom) return; const k=ch.id+'|'+dom.id; cnt[k]=(cnt[k]||0)+1; mx=Math.max(mx,cnt[k]);})); });
  const col=v=> v===0?'transparent': v<=mx*0.2?'var(--seq1)': v<=mx*0.4?'var(--seq2)': v<=mx*0.6?'var(--seq3)': v<=mx*0.8?'var(--seq4)':'var(--seq5)';
  const fg=v=> v>mx*0.4?'#fff':'inherit';
  document.getElementById('heat').innerHTML = `<tr><th>장 \\ 도메인</th>${domains.map(d=>`<th class="num" title="${esc(d.title)}">${esc(d.code)} ${esc(d.title.split('·')[0].split('(')[0]).slice(0,6)}</th>`).join('')}</tr>` + chapters.map(c=>`<tr><th>${esc(c.code)} ${esc(c.title)}</th>${domains.map(d=>{const v=cnt[c.id+'|'+d.id]||0;return `<td class="c" style="background:${col(v)};color:${fg(v)}">${v||''}</td>`;}).join('')}</tr>`).join('');
  const rows=[]; Object.values(DN).forEach(n=>['item','topic'].forEach(l=>n.mapping[l].forEach(i=>rows.push({d:n.id,l,i}))));
  function render(){ const lv=document.getElementById('m-level').value, q=document.getElementById('m-q').value.toLowerCase();
    const r=rows.filter(x=>(!lv||x.l===lv)&&(!q||(dpath(x.d)+DN[x.d].title+IN[x.i].title).toLowerCase().includes(q)));
    document.getElementById('edges').innerHTML=`<tr><th>데이터 트리 노드</th><th>수준</th><th>정보 트리 노드</th><th class="num">발견</th></tr>`+r.slice(0,600).map(x=>`<tr><td><span class="chip dt" data-dt="${x.d}">${esc(dpath(x.d))}</span> ${esc(DN[x.d].title)}</td><td>${x.l==='item'?'항목':'주제'}</td><td><span class="chip it" data-it="${x.i}">${esc(IN[x.i].code)}</span> ${esc(IN[x.i].title)}</td><td class="num">${DN[x.d].stats.findings_total}</td></tr>`).join('')+(r.length>600?`<tr><td colspan="4" class="muted">… ${r.length-600}건 더</td></tr>`:'');
    document.getElementById('edges').querySelectorAll('[data-dt]').forEach(el=>el.addEventListener('click',()=>{showTab('dtree');selectD(el.dataset.dt,true);}));
    document.getElementById('edges').querySelectorAll('[data-it]').forEach(el=>el.addEventListener('click',()=>{showTab('itree');selectI(el.dataset.it);}));
  }
  document.getElementById('m-level').addEventListener('change',render); document.getElementById('m-q').addEventListener('input',render); render();
})();
// ---------- observation schema
(function(){
  const o=D.observation_schema;
  document.getElementById('fields').innerHTML=`<tr><th>필드</th><th>뜻</th><th>설명</th></tr>`+o.minimum_description.map(f=>`<tr><td class="mono">${esc(f.field)}</td><td><b>${esc(f.ko)}</b></td><td>${esc(f.desc)}</td></tr>`).join('')+`<tr><td colspan="3" class="small muted">TGT 3.4 여섯 속성: ${o.tgt_six_attributes.join(' · ')} · 필드명은 설명용이며 물리 스키마 확정이 아니다.</td></tr>`;
  const mx=Math.max(...o.context_relation_types.map(c=>c.observed_total));
  document.getElementById('ctxbars').innerHTML=o.context_relation_types.map(c=>`<div class="bar"><div class="lab" title="${esc(c.observed_synonyms.join(', '))}">${esc(c.ko)} <span class="mono muted">${esc(c.canonical)}</span></div><div class="trk"><div class="fil" style="width:${(100*c.observed_total/mx).toFixed(1)}%"></div></div><div class="val">${fmt(c.observed_total)}</div></div><div class="small muted" style="margin-left:178px">${Object.entries(c.observed_count).map(([r,v])=>`${RN[r]} ${fmt(v)}`).join(' · ')} · 원어휘: ${c.observed_synonyms.join(', ')}</div>`).join('')+`<div class="small muted" style="margin-top:8px">문맥 상태: ${o.context_states.join(' / ')}</div>`;
  document.getElementById('vocab').innerHTML=`<b>값 상태 어휘</b><div>${o.value_status_vocab.map(v=>`<span class="chip">${esc(v)}</span>`).join('')}</div><b style="display:block;margin-top:10px">비교를 허용하는 순서</b><ol class="small">${o.comparability_order.map(s=>`<li>${esc(s)}</li>`).join('')}</ol><div class="note">${esc(o.note)}</div>`;
  document.getElementById('rules').innerHTML=D.rules.map(r=>`<div class="rule"><div class="lab">${esc(r.label||r.id)} <span class="st">${r.id.split('/').pop()} · ${esc(r.state)}${r.inherited_from?' · a0001 승계':''}</span></div>${r.application?`<div class="small"><b>적용</b> ${esc(r.application)}</div>`:''}${r.rejection?`<div class="small"><b>거절</b> ${esc(r.rejection)}</div>`:''}${r.counterexample_guard?`<div class="small"><b>반례 가드</b> ${esc(r.counterexample_guard)}</div>`:''}${r.required_context&&r.required_context.length?`<div class="small"><b>필수 문맥</b> ${r.required_context.map(c=>`<span class="chip">${esc(c)}</span>`).join('')}</div>`:''}<div class="small" style="margin-top:4px"><b>매달린 노드</b> ${r.nodes.length?r.nodes.map(d=>`<span class="chip dt" data-dt="${d}">${esc(dpath(d))} ${esc(DN[d].title).slice(0,22)}</span>`).join(''):'<span class="muted">지원 발견이 현재 표본 밖이거나 미귀속</span>'}</div><div class="small muted">지원 발견: ${r.supporting.map(s=>s.replace('/r0001/finding/','/')).join(', ')||'–'}</div></div>`).join('');
  document.getElementById('rules').querySelectorAll('[data-dt]').forEach(el=>el.addEventListener('click',()=>{showTab('dtree');selectD(el.dataset.dt,true);}));
  document.getElementById('notetopics').innerHTML=`<tr><th>코드</th><th>주제</th><th>내용</th><th>필수 문맥</th><th>키워드</th></tr>`+D.note_topics.map(t=>`<tr><td class="mono">${t.code}</td><td><b>${esc(t.title)}</b></td><td class="small">${esc(t.desc)}</td><td class="small">${t.contexts.map(esc).join(' · ')}</td><td class="small muted">${t.keywords.join(', ')}</td></tr>`).join('');
})();
// ---------- table types tab
(function(){
  const sel=document.getElementById('t-node'); D.data_tree.children.forEach(c=>{const o=document.createElement('option');o.value=c.id;o.textContent=c.code+' '+c.title;sel.appendChild(o);});
  function render(){
    const q=document.getElementById('t-q').value.toLowerCase(), sh=document.getElementById('t-shared').checked, nd=sel.value;
    const rows=D.table_types.filter(t=>(!sh||t.reports.length>=2)&&(!nd||t.node.startsWith(nd))&&(!q||(dpath(t.node)+(t.caption||'')+t.header+DN[t.node].title).toLowerCase().includes(q))).sort((a,b)=>b.reports.length-a.reports.length||a.node.localeCompare(b.node));
    document.getElementById('ttypes').innerHTML=`<tr><th>노드</th><th>캡션(대표)</th><th class="num">보고서</th><th>머리글(대표 첫 행)</th><th>단위</th><th class="num">건</th></tr>`+rows.slice(0,500).map(t=>`<tr><td><span class="chip dt" data-dt="${t.node}">${esc(dpath(t.node))}</span> <span class="small">${esc(DN[t.node].title).slice(0,22)}</span></td><td>${esc(t.caption||'(캡션 없음)')}</td><td class="num" title="${t.reports.map(r=>RN[r]).join(', ')}">${t.reports.length}</td><td class="small mono">${esc(t.header)}</td><td class="small">${esc(t.unit||'')}</td><td class="num">${t.count}</td></tr>`).join('')+(rows.length>500?`<tr><td colspan="6" class="muted">… ${rows.length-500}건 더</td></tr>`:'');
    document.getElementById('ttypes').querySelectorAll('[data-dt]').forEach(el=>el.addEventListener('click',()=>{showTab('dtree');selectD(el.dataset.dt,true);}));
  }
  ['t-q','t-shared','t-node'].forEach(id=>document.getElementById(id).addEventListener('input',render)); render();
  document.getElementById('revs').innerHTML=`<tr><th>노드</th><th>관찰 캡션</th><th class="num">보고서</th><th>머리글</th><th>제안</th></tr>`+(D.revision_candidates.length?D.revision_candidates.map(r=>`<tr><td><span class="chip dt" data-dt="${r.node}">${esc(dpath(r.node))}</span> ${esc(r.parent_title).slice(0,20)}</td><td>${esc(r.caption)}</td><td class="num">${r.reports.length}</td><td class="small mono">${esc(r.header)}</td><td class="small">L3 항목 추가 또는 기존 항목 별칭 등록 검토</td></tr>`).join(''):'<tr><td colspan="5" class="muted">없음</td></tr>');
  document.getElementById('revs').querySelectorAll('[data-dt]').forEach(el=>el.addEventListener('click',()=>{showTab('dtree');selectD(el.dataset.dt,true);}));
})();
// ---------- basis
(function(){
  const S=D.survey_summary; const sv=S.filter(r=>r.surveyed), pd=S.filter(r=>!r.surveyed);
  document.getElementById('prog-kpis').innerHTML=[[sv.length,'구조 조사 완료(골격에 매달림)'],[sv.filter(r=>r.semantic).length,'셀 단위 의미조사 존재(모두 부분)'],[pd.length,'미취득(원문 접근 차단)'],[D.meta.counts.revision_candidates,'L3 개정 후보'],[sv.reduce((a,r)=>a+r.unmatched.length,0),'템플릿 미대응 목차 항목']].map(([v,l])=>`<div class="kpi"><div class="v">${fmt(v)}</div><div class="l">${l}</div></div>`).join('');
  document.getElementById('reports').innerHTML=`<tr><th>ID</th><th>회사·연도</th><th>업종</th><th>접수번호</th><th>사업기간</th><th>구조 조사</th><th class="num">목차 정렬</th><th class="num">데이터 표</th><th>의미조사</th><th class="num">발견</th><th>재개 위치·한계</th></tr>`+sv.map(r=>`<tr><td class="mono">${r.id}</td><td>${esc(r.company)} ${r.fiscal_year}</td><td class="small">${esc(r.sector||'')}</td><td class="mono">${r.receipt_id||'–'}</td><td class="small">${esc(r.period||'')}</td><td><span class="status-good">완료</span></td><td class="num">${r.aligned}/${r.sections}</td><td class="num">${fmt(r.tables_data)}</td><td>${r.semantic?(r.semantic.work_state==='paused'?'<span class="status-warn">paused</span>':'<span class="status-bad">blocked</span>'):'<span class="muted">없음</span>'}</td><td class="num">${r.semantic?fmt(r.semantic.outputs.findings):'–'}</td><td class="small">${esc(r.semantic?r.semantic.resume:'')}</td></tr>`).join('')+`<tr><td colspan="11" class="small muted">의미조사 열은 초기 5건의 셀 단위 조사 상태(batch G01: 착수 ${D.meta.batch.attempted}, paused ${D.meta.batch.paused}, blocked ${D.meta.batch.blocked}, 전수완료 ${D.meta.batch.fully_reviewed}). 구조 조사는 목차 정렬·절별 구조 통계·표 카탈로그까지이며 셀 단위 의미 판별을 포함하지 않는다.</td></tr>`;
  document.getElementById('pending-note').innerHTML = pd.length? `<b>${esc(pd[0].acquisition.reason)}</b><div style="margin-top:6px">필요 자료: ${pd[0].acquisition.needed.map(esc).join(' / ')} → <span class="mono">python3 build/survey_structure.py BRxxxx --html … --wrapper …</span> 실행 후 <span class="mono">build.py → render_html.py</span>. 셀 단위 의미조사는 하지 않는다(${esc(pd[0].planned_depth)}).</div>`:'미취득 보고서 없음';
  document.getElementById('pending').innerHTML=`<tr><th>ID</th><th>회사·연도</th><th>업종</th><th>사업기간</th><th>표본 선정 이유</th><th>골격 검증에서 기대하는 변형(가설, 미검증)</th></tr>`+pd.map(r=>`<tr><td class="mono">${r.id}</td><td>${esc(r.company)} ${r.fiscal_year}</td><td class="small">${esc(r.sector||'')}</td><td class="small">${esc(r.period||'')}</td><td class="small">${esc(r.sampling_reason||'')}</td><td class="small">${(r.expected_variants||[]).map(v=>`<div>· ${esc(v)}</div>`).join('')}</td></tr>`).join('');
  document.getElementById('method').innerHTML=`<ol><li><b>골격</b>: 5개 보고서의 DART wrapper 목차(node1/node2/node3)와 본문 앵커(&lt;A name='tocN'&gt;), XBRL 표그룹 제목으로 장·절·주석 위치를 원문 문자 위치(줄바꿈 포함 코드포인트 기준, nodes.jsonl 과 동일 기준)로 확정했다.</li><li><b>L3 항목·표 유형</b>: 절 안의 '가./(1)/1)/[ ]' 형식 소제목을 5개 보고서에서 집계해 공통 항목을 잡고, 기업공시서식 작성기준의 표 구성으로 보완했다. 주석은 회사별 번호가 달라 '주제 유형' 31개로 두었다.</li><li><b>구조 조사(깊이 조정)</b>: 나머지 표본은 셀 단위 의미 판별 대신 build/survey_structure.py 로 목차 정렬·절별 표/셀/문단 수·소제목·표 카탈로그(캡션·단위·기준일·머리글 행·행열 수·병합)만 수집한다. 골격의 검증·확장에 필요한 깊이이며, 의미조사는 골격이 안정된 뒤 표 유형 단위로 재개한다.</li><li><b>살</b>: 초기 5건의 findings.jsonl 근거 노드 위치를 절 범위와 대조해 각 발견을 가장 깊은 절의 템플릿 노드에 매달았다. a0002 규칙·유형 후보는 supporting_discoveries 의 발견을 따라 노드에 연결했다. 표 유형은 (노드, 정규화 캡션)으로 묶어 보고서 간 공통성을 세었다.</li><li><b>인스턴스 오버레이</b>: 절 범위 안의 표·셀·문단 수를 세어 '존재/제목만/상위 절에 포함/없음'을 판정했다. 하위가 존재하면 상위도 존재로 집계한다.</li><li><b>정보 트리·매핑</b>: TGT v5 04장 원칙(단일 부모, 2수준 대응)과 PPT 슬라이드 13 예시를 따라 초안을 작성했다. 스킬 배지는 TGT 12장 5개 스킬의 입력 요구를 거칠게 표시한 것이다.</li></ol><div class="muted">재현: build/author_skeleton.py → build/survey_structure.py(보고서별) → build/build.py → build/render_html.py. 입력: inputs/reports/BRxxxx/{structure,identity}.json, inputs/derived/*.json, inputs/aggregate_*/*.jsonl.</div>`;
})();
renderDTree(); renderITree();
(function(){ // #tab=dtree&d=DT.A001.III.6.02&i=IT.3.6
  const h=new URLSearchParams(location.hash.replace(/^#/,'')); const t=h.get('tab'); const d=h.get('d'); const i=h.get('i');
  selectD(d&&DN[d]?d:'DT.A001.III.6.02', !!d);
  if(i&&IN[i]) selectI(i); else selectI('IT.3.6');
  if(t) showTab(t);
})();
</script>
</body>
</html>
"""

html = HTML.replace("__DATA__", data)
out = os.path.join(DIST, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("written", out, os.path.getsize(out), "bytes")
