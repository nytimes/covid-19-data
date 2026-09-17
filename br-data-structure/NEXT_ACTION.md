# 다음 행동 — G01 나머지 15건을 골격에 매달기

## 현재 상태 (2026-09-17)

- 골격 v0.2: 데이터 트리 288노드 · 정보 트리 90노드 · 매핑 266간선 · 관측 규약.
- 관측 카탈로그 v0.1: 235항목에 관측 1,025건, 항목 세분화(Level 4) 20건. Domain Side 양식 엑셀로 출력(`dist/Domain_Side_사업보고서.xlsx`).
- Depth 정렬 도구(`build/align_depth.py`): 5건 기준 L1 15/15 공통·순서 불일치 0, L2 30/62 공통, 템플릿 미대응 제목 0.
- 구조 조사 완료 5건(삼성전자 2024, DB손해보험 2023, 셀트리온 2023, 선바이오 2021, NH프라임리츠 2021). 표 유형 1,200여 개, 보고서 2건 이상 공통 유형 140여 개.
- 미취득 15건: `inputs/reports/BRxxxx/identity.json` 슬롯만 있음. 이 실행환경은 `dart.fss.or.kr`, `opendart.fss.or.kr`, `kind.krx.co.kr` 접속이 조직 egress 정책으로 차단됨(403 CONNECT). 우회하지 않았다.

## 깊이 조정 (사용자 지시에 따른 결정)

나머지 15건은 **구조 조사**만 한다. 목차 정렬, 절별 표·셀·문단 수, 소제목, 표 카탈로그(캡션·단위·기준일·머리글·행열·병합)까지.
셀 단위 의미 판별(초기 5건 방식, 보고서당 수만 셀)은 골격이 안정된 뒤 **표 유형 단위**로 재개한다.
이유: 지금 목적은 골격의 검증·확장이며, 그 검증에 필요한 정보는 절 구성·표 유형·머리글이지 개별 셀의 문맥이 아니다.

## 보고서 15건을 매다는 절차 (OpenDART API 경로, 권장)

OpenDART 키를 받았으나 이 실행환경은 `opendart.fss.or.kr` 도 차단(403 CONNECT)이라 실행하지 못했다. 키가 있고 접속되는 환경에서:

```bash
export OPENDART_API_KEY=…                 # 키는 환경변수로만. 파일·커밋 금지
python3 build/acquire_opendart.py all     # corpcode → resolve → find → fetch → survey (pending 15건)
python3 build/build.py && python3 build/render_html.py
```

단계별로 하려면 `corpcode / resolve / find / fetch / survey` 를 순서대로, 특정 건만 하려면 `… find BR0043 BR0082` 처럼 ID를 붙인다.
- `resolve`: `inputs/raw/CORPCODE.xml` 로 종목코드(identity.json 의 참고값) → corp_code. 후보가 여럿이면 출력을 보고 identity.json 의 stock_code 를 고친다.
- `find`: 사업연도 종료일부터 150일 창에서 A001 접수 목록을 받아 `사업보고서 (YYYY.MM)` 와 일치하는 최초 제출본을 고른다. 정정본은 `corrections` 에 기록만.
- `fetch`: `document.xml` 원본 zip → `inputs/raw/BRxxxx/` (gitignore). 본문 XML 경로를 identity.json 에 기록.
- `survey`: `survey_structure.py --xml` (dart3.xsd: SECTION-1/2/3·TITLE·TABLE-GROUP 파싱). 합성 샘플 `build/tests/sample_dart.xml` 로 파서를 시험했고 실제 API 응답으로는 아직 검증하지 못했다. 첫 실행 후 `structure.json` 의 `unmatched` 와 `with_pos/sections` 를 반드시 확인한다.

뷰어 HTML 이 있는 경우(초기 5건 패키지 형식)는 종전대로 `--html … --wrapper …` 를 쓴다.

### 대안: dart_bulk_download.py(사용자 보유 수집기) 로 받은 lake 사용

`dart_bulk_download.py`(v1.2.0)가 만든 폴더(`manifest.sqlite3` + `raw/documents/YYYY/MM/DD/<접수번호>.zip`)는 그대로 쓸 수 있다.
전체 A001 수집은 수천 건·수 GB·며칠이 걸리므로, **회사별로 좁은 접수일 창**만 받는다. 회사 고유번호(8자리)가 필요하며
같은 `--out` 폴더에서는 회사 필터를 바꿀 수 없으므로 회사마다 `--out` 을 달리한다.

```bash
python3 build/from_lake.py --plan            # 15건의 회사별 실행 명령(접수일 창 = 사업연도 종료일 ~ +150일) 출력
python dart_bulk_download.py run --out ./lake_BR0043 --corp-code 0XXXXXXX --start 20230331 --end 20230828 --export --wait-on-limit
python3 build/from_lake.py --lake ./lake_BR0043 BR0043      # 원공시 선택, 정정본 기록, XML 추출, 구조 조사
python3 build/build.py && python3 build/render_html.py
```

이미 받아둔 lake(예: 초기 100건 원본 실행 패키지의 원천)가 있으면 API 호출 없이 `from_lake.py --lake <폴더>` 만으로 15건을 찾는다.
lake 에 목록만 있고 원문이 없으면 `listed_not_downloaded` 로 표시되며 `--mode download` 후 다시 실행한다.
어댑터는 수집기 스키마와 같은 가짜 lake 로 끝까지 시험했다(원공시 선택·정정본 기록·XML 추출·구조 조사).

4. `structure.json` 의 `unmatched`(템플릿 미대응 목차 항목)와 시각화 ⑥ 탭의 'L3 개정 후보'를 보고 `build/author_skeleton.py` 의 템플릿(별칭·업종 변형·L3 항목)을 개정한 뒤 `author_skeleton.py → build.py → render_html.py` 를 재실행한다.

## 원문이 도착하면 할 일 (관측 카탈로그 검증)

1. `survey_structure.py --xml` 으로 구조 조사 → `align_depth.py` 로 Depth 정렬. 여기서 나오는 `unmatched` 와 '단독' 분류가 골격 개정 후보다.
2. 표 머리글 시그니처를 관측 카탈로그와 대조한다. 카탈로그에 없는 머리글 = 누락 관측, 카탈로그에만 있는 관측 = 서식에는 있으나 미기재.
   현재 관측 근거는 항목 단위 70 / 절 단위 161 / 없음 4 이므로, 원문이 늘면 '절 단위'를 '항목 단위'로 올리는 것이 1차 목표다.
3. 한 항목 안에서 grain 이 다른 표가 새로 확인되면 Level 4 를 추가한다(현재 20건).
4. `author_observations.py` → `author_skeleton.py` → `build.py` → `render_html.py` → `export_domain_side.py` 순으로 재생성.

## 15건에서 확인할 골격 가설 (identity.json 의 expected_variants)

- 신영증권 2023·2025: II장 금융업 서식(증권) → F1~F4에 '증권' 별칭 필요 여부, 3월 결산 기간 문맥.
- 삼성스팩4호 2021: 빈 절 다수, 설립 후 첫 사업기간, 합병 관련 사후정보.
- 엑세스바이오 2025: 외국법인 특례 기재, 회계기준·통화 문맥.
- 대한항공 2021, 기아 2022, 현대자동차 2021, SK하이닉스 2022·2024, 하이트진로 2023, 대동 2024, 포스코 2021: 일반 서식 안의 업종별 표 변형(항공기 리스, 판매보증, 부문 병존, 재고·설비, 주세, 지주 전환).
- 삼성화재 2025: 보험업 F1~F4 재사용 검증(2025년 서식 변경 여부).
- 한국전력공사 2023: 공기업(정부 최대주주, 요금 규제, 발전자회사).
- 현대건설 2022: III.8.04 수주계약 현황(진행률) 표, XI.2 우발채무.

## 하지 않은 것

- 원문 없는 상태에서 15건의 절 구성·표 유형을 추정해 채우지 않았다.
- 초기 5건의 의미조사(paused/blocked)를 재개하지 않았다.
