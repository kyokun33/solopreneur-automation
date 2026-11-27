# Loss Scorecard Integration Test Suite (V2.0)

## 🧪 목표: 모든 경계 조건(Edge Case) 및 비정상 상태 전이 테스트를 통해 시스템의 안정성 증명.

### **A. 백엔드 API 통합 테스트 (Backend)**
**테스트 환경**: Mocked External Services (IP Similarity Engine, Payment Gateway) 사용을 가정합니다.
| Test ID | Scenario | Input Data | Expected Result | Failure Condition Check |
| :--- | :--- | :--- | :--- | :--- |
| `API_001` | **Baseline Success** | Safe/Low Risk Data Set | Status: 200 OK, `warning_state`: SAFE. `transition_log`가 최소한의 초기값만 포함함. | 정상 범위 내에서 비용 계산이 완료되는지 확인. |
| `API_002` | **Critical State Change** | High Risk Data Set (Major Flaw) | Status: 200 OK, `warning_state`: CRITICAL. `transition_log`에 $\Delta$ 값이 크고(e.g., $>0.5$), 원인 설명이 명시됨. | 점수 변화의 *절대값*과 *원인 필드*가 정확히 매핑되는지 확인. |
| `API_003` | **Engine Failure** | Flawed Data (External API Down) | Status: 503 Service Unavailable, Error Code: `ENGINE_FAILURE`. | 시스템이 크래시(Crash)하지 않고, 재시도 로직을 안내하는 메시지를 반환하는지 확인. |
| `API_004` | **Input Validation** | Missing Required Field (e.g., `user_id`) | Status: 400 Bad Request, Error Code: `INVALID_INPUT`. | 필수 필드에 대한 명확한 에러 메시지를 반환하고 처리를 중단하는지 확인. |
| `API_005` | **Boundary Condition** | Zero/Minimal Data Input | Status: 200 OK, `warning_state`: SAFE (or NEUTRAL). 점수 변화가 없거나 미미해야 함. | 시스템이 과도한 경고를 발생시키지 않도록 최소값을 처리하는지 확인. |

### **B. 프론트엔드 컴포넌트 테스트 (Frontend - React/Jest)**
| Test ID | Component | Scenario | Test Action | Expected UI Output / Behavior |
| :--- | :--- | :--- | :--- | :--- |
| `FE_001` | `<DynamicLossCounter />` | Loading State to Final Value | API 호출 완료 (Final Cost $4,567.89) 시뮬레이션. | 숫자가 0에서 최종 값까지 *부드럽게* 카운트업 애니메이션을 보여야 함. |
| `FE_002` | `<RedWarningFilter />` | State Change Triggering | Props에 $\Delta$가 임계값을 넘는 값을 주입(`previous: 0.3`, `current: 0.8`). | 화면 전체에 지정된 강도의 Red Warning 필터(CSS Filter)가 즉시 적용되어야 함. |
| `FE_003` | `<TransitionHistoryLog />` | Time-Series Data Rendering | 3개의 StateChange 객체를 순차적으로 Props로 전달. | 로그 항목이 시간순으로 쌓이며, 각 항목에 '변화 폭'이 명확한 숫자로 표시되어야 함. (데이터의 신뢰도 확보) |
| `FE_004` | **Full Flow** | Error Handling (503 API) | 백엔드에서 503 에러 코드를 반환하는 가짜 데이터를 Props로 받음. | Scorecard 전체가 Red Warning 대신 '시스템 점검 중' 메시지를 보여주고, 재시도 버튼을 활성화해야 함. |