# Lab 17 Golden Set Report

- Implementation: `student`
- Kind: `golden`
- Cases: **20**
- Passed: **20/20**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **1493.3 ms**
- Average token reduction vs full source context: **2.5%**
- Golden bonus: **10/10** (100% required)

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| G01 | short_term | PASS | 0.2 | 227 | 0.0% |  |
| G02 | short_term | PASS | 0.0 | 133 | 0.0% |  |
| G06 | long_term | PASS | 1689.3 | 840 | 0.0% |  |
| G09 | semantic | PASS | 362.2 | 418 | 8.9% |  |
| G10 | semantic | PASS | 537.8 | 410 | 10.7% |  |
| G14 | mixed | PASS | 1807.3 | 581 | 0.0% |  |
| G03 | long_term | PASS | 1743.5 | 1336 | 0.0% |  |
| G04 | long_term | PASS | 2365.5 | 1484 | 0.0% |  |
| G07 | episodic | PASS | 711.7 | 665 | 0.0% |  |
| G08 | episodic | PASS | 634.8 | 680 | 0.0% |  |
| G11 | mixed | PASS | 2014.1 | 581 | 0.0% |  |
| G13 | mixed | PASS | 923.3 | 500 | 11.5% |  |
| G15 | mixed | PASS | 2658.4 | 831 | 0.0% |  |
| G16 | mixed | PASS | 2349.0 | 581 | 0.0% |  |
| G17 | mixed | PASS | 2150.6 | 581 | 0.0% |  |
| G18 | mixed | PASS | 1325.7 | 500 | 11.5% |  |
| G19 | mixed | PASS | 2453.6 | 581 | 0.0% |  |
| G05 | long_term | PASS | 1842.6 | 1363 | 0.0% |  |
| G12 | mixed | PASS | 2251.1 | 581 | 8.1% |  |
| G20 | mixed | PASS | 2045.0 | 756 | 0.0% |  |

## Evidence excerpts

### G01 - short_term

`<SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. | assistant: Noted staging constraint. | user: Filler A about button padding. | assistant: Filler A. | user: Filler B about color tokens. | assistant: Filler B. | user: Filler C about copy tone. | assistant: Filler C. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. - user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. - assistant: Noted staging constraint. </DURA`

### G02 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### G06 - long_term

`<USER_SUMMARY> Lan Tran's project is LOTUS-88. Lan prioritizes Java and Spring Boot for backend examples and does not use Python for backend examples.  Lan prioritizes Java and Spring Boot, and does not use Python for backend examples. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-17 09:42:28     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Evaluation User" }: Minh la Lan, phap ly hoi gat truoc khi bat memory tren san pham. Viet hop dong ngan: backend minh dang dung ngon ngu/framework nao, va quy tac luu/xoa bo nho ca nhan trong la`

### G09 - semantic

`EPISODE: {"id":"kb-payment-retry","entity":"Payment API Retry Policy","summary":"For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3.","source":"internal-api-guideline-v3","updated_at":"2026-08-10T00:00:00Z"} metadata= EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata= EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal `

### G10 - semantic

`EPISODE: {"id":"kb-context-budget","entity":"Memory Context Budget","summary":"Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodic 3 percent, semantic 3 percent; trim lower-priority memory first. Marker: BUDGET-10-4-3-3.","source":"lab-design-note","updated_at":"2026-08-13T00:00:00Z"} metadata= EPISODE: Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodic 3 percent, semantic 3 percent; trim lower-priority memory first. Marker: BUDGET-10-4-3-3. metadata= EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data without explicit opt-in. A de`

### G14 - mixed

`<LONG_TERM> <USER_SUMMARY> Lan Tran's project is LOTUS-88. Lan prioritizes Java and Spring Boot for backend examples and does not use Python for backend examples.  Lan prioritizes Java and Spring Boot, and does not use Python for backend examples. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-17 09:43:05     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Evaluation User" }: Lan uu tien stack backend nao cho LOTUS-88?   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant): Da hieu: LOTUS-88, Jav`

### G03 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used for this project.  Minh Nguyen prefers Python and dislikes Java. For personal demos like ORCHID-27, Python is still preferred. When explaining code, Minh Nguyen prefers short examples. When learning about async/await and encountering confusion between coroutine and Task, Minh Nguyen prefers explanations using a timeline.  When learning about async/await and encountering confusion between coroutine and Task, explain using a timeline. </USER_SUMMARY>  <EPISODES> Episodes are source `

### G04 - long_term

`FACT: The benchmark report has the open loop reference code LAB-REPORT-1600. [valid_at=2026-08-01T09:04:00Z, invalid_at=None] FACT: Minh Nguyen needs to complete the benchmark report before Thursday 16:00. [valid_at=2026-08-01T09:04:00Z, invalid_at=None] FACT: The benchmark report is due by Thursday 16:00. [valid_at=2026-08-01T09:04:00Z, invalid_at=None] FACT: The main issue was connection churn, not the timeout threshold. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: Minh Nguyen increased the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=None]  <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project`

### G07 - episodic

`EPISODE: Hay kiem tra connection pool, lifecycle cua client va concurrency. metadata= EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. metadata= EPISODE: Da ghi nhan trajectory: increase timeout khong hieu qua; ClientSession + concurrency=20 giai quyet connection churn. metadata= EPISODE: Minh sap viet script ca nhan de tai hien su co latency, muon code dung ngon ngu minh thich khi lam mot minh, dong thoi bam sat playbook incident cua lab chu dung vo tang timeout. G EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich cod`

### G08 - episodic

`EPISODE: Hay kiem tra connection pool, lifecycle cua client va concurrency. metadata= EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. metadata= EPISODE: Da ghi nhan trajectory: increase timeout khong hieu qua; ClientSession + concurrency=20 giai quyet connection churn. metadata= EPISODE: Minh sap viet script ca nhan de tai hien su co latency, muon code dung ngon ngu minh thich khi lam mot minh, dong thoi bam sat playbook incident cua lab chu dung vo tang timeout. G EPISODE: Minh sap giai thich coroutine cho ban, dong thoi can nhac policy retry payment vao vi du. Minh h`

### G11 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used for this project.  Minh Nguyen prefers Python and dislikes Java. For personal demos like ORCHID-27, Python is still preferred. When explaining code, Minh Nguyen prefers short examples. When learning about async/await and encountering confusion between coroutine and Task, Minh Nguyen prefers explanations using a timeline.  When learning about async/await and encountering confusion between coroutine and Task, explain using a timeline. </USER_SUMMARY>  <EPISODES> Episodes`

### G13 - mixed

`<EPISODIC> EPISODE: Hay kiem tra connection pool, lifecycle cua client va concurrency. metadata= EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. metadata= EPISODE: Da ghi nhan trajectory: increase timeout khong hieu qua; ClientSession + concurrency=20 giai quyet connection churn. metadata= EPISODE: Mai hop mentor, toi nay minh muon don open-loop. Liet ke viec chua dong, deadline, va ma dinh danh task. Can du ba manh de ghi vao note hop. EPISODE: Minh sap giai thich coroutine cho ban, dong thoi can nhac policy retry payment vao vi du. Minh hoc kieu nao thi de nho? Va re`

### G15 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used for this project.  Minh Nguyen prefers Python and dislikes Java. For personal demos like ORCHID-27, Python is still preferred. When explaining code, Minh Nguyen prefers short examples. When learning about async/await and encountering confusion between coroutine and Task, Minh Nguyen prefers explanations using a timeline.  When learning about async/await and encountering confusion between coroutine and Task, explain using a timeline. </USER_SUMMARY>  <EPISODES> Episodes`

### G16 - mixed

`<LONG_TERM> FACT: The benchmark report has the open loop reference code LAB-REPORT-1600. [valid_at=2026-08-01T09:04:00Z, invalid_at=None] FACT: Minh Nguyen needs to complete the benchmark report before Thursday 16:00. [valid_at=2026-08-01T09:04:00Z, invalid_at=None] FACT: The benchmark report is due by Thursday 16:00. [valid_at=2026-08-01T09:04:00Z, invalid_at=None] FACT: The main issue was connection churn, not the timeout threshold. [valid_at=2026-08-03T10:03:00Z, invalid_at=None] FACT: Minh Nguyen increased the timeout to 60s. [valid_at=2026-08-03T10:00:00Z, invalid_at=None]  <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the com`

### G17 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used for this project.  Minh Nguyen prefers Python and dislikes Java. For personal demos like ORCHID-27, Python is still preferred. When explaining code, Minh Nguyen prefers short examples. When learning about async/await and encountering confusion between coroutine and Task, Minh Nguyen prefers explanations using a timeline.  When learning about async/await and encountering confusion between coroutine and Task, explain using a timeline. </USER_SUMMARY>  <EPISODES> Episodes`

### G18 - mixed

`<EPISODIC> EPISODE: Hay kiem tra connection pool, lifecycle cua client va concurrency. metadata= EPISODE: Cach hieu qua la reuse aiohttp ClientSession va dat concurrency=20. Reflection: loi chinh la connection churn, khong phai timeout threshold. Ma su co ASYNC-FIX-20. metadata= EPISODE: Da ghi nhan trajectory: increase timeout khong hieu qua; ClientSession + concurrency=20 giai quyet connection churn. metadata= EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. EPISODE: Sep hoi chuan hoa backend du an cong ty, minh hay lan voi stack `

### G19 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used for this project.  Minh Nguyen prefers Python and dislikes Java. For personal demos like ORCHID-27, Python is still preferred. When explaining code, Minh Nguyen prefers short examples. When learning about async/await and encountering confusion between coroutine and Task, Minh Nguyen prefers explanations using a timeline.  When learning about async/await and encountering confusion between coroutine and Task, explain using a timeline. </USER_SUMMARY>  <EPISODES> Episodes`

### G05 - long_term

`<USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used for this project.  Minh Nguyen prefers Python and dislikes Java. For personal demos like ORCHID-27, Python is still preferred. When explaining code, Minh Nguyen prefers short examples. When learning about async/await and encountering confusion between coroutine and Task, Minh Nguyen prefers explanations using a timeline.  When learning about async/await and encountering confusion between coroutine and Task, explain using a timeline. </USER_SUMMARY>  <EPISODES> Episodes are source `

### G12 - mixed

`<LONG_TERM> <USER_SUMMARY> Minh Nguyen's personal project is named ORCHID-27, for which Python is still preferred. For the company project BLUEBIRD-42, the backend must use TypeScript with NestJS, and Python should not be used for this project.  Minh Nguyen prefers Python and dislikes Java. For personal demos like ORCHID-27, Python is still preferred. When explaining code, Minh Nguyen prefers short examples. When learning about async/await and encountering confusion between coroutine and Task, Minh Nguyen prefers explanations using a timeline.  When learning about async/await and encountering confusion between coroutine and Task, explain using a timeline. </USER_SUMMARY>  <EPISODES> Episodes`

### G20 - mixed

`<SHORT_TERM> <SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Filler about dashboard widgets. | assistant: Filler. | user: Filler about CSS variables. | assistant: Filler. | user: Filler about copy review. | assistant: Filler. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. </DURABLE_NOTES> <RECENT_TURNS> user: Filler about empty charts. assistant: Filler. user: Filler about telemetry. assistant: Filler. user: Filler about a11y labels. assistant: Filler. </RECENT_TURNS> </SHORT_TERM>`
