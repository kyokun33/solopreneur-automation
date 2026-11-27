# Loss Scorecard API Contract Specification (V2.0 - State Transition Focus)

## 🎯 Endpoint: `/api/v1/risk/calculate-score`
**Method**: `POST`
**Description**: 사용자의 초기 데이터를 기반으로 법적 리스크 점수(Loss Score)를 계산하고, 그에 따른 경고 상태(Warning State)를 반환합니다. 이 엔드포인트는 단순 데이터 조회가 아닌 '상태 전이' 로직을 수행해야 합니다.

### 📥 Request Body (Input Schema - `UserInput`)
사용자의 초기 입력 정보와 분석할 데이터를 받습니다. 모든 필드는 필수 검증(Validation) 대상입니다.

| Field | Type | Description | Constraints | Example |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | UUID | 식별자. 세션 추적 및 개인화에 사용됨. | Required | `uuid-example-1234` |
| `input_data` | JSON Object | 분석 대상 데이터 (예: 거래 기록, 문서 업로드 메타데이터). | Required | `{ "source": "user_upload", "risk_level": 0.7 }` |
| `context_params` | Dictionary | 추가적인 외부 변수 (e.g., `jurisdiction`, `time_of_day`). | Optional | `{"country": "KR"}` |

### 📤 Response Body (Success Schema - `CalculationResponse`)
성공 시, 계산된 최종 점수와 함께 '상태 변화'를 추적할 수 있는 메타데이터가 포함되어야 합니다.

| Field | Type | Description | Example Value | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `score_id` | UUID | 이번 계산 트랜잭션의 고유 ID. (로깅용) | `uuid-calc-xyz789` | |
| `initial_loss_score` | Float | 초기 리스크 점수 (0.0 ~ 1.0). | `0.25` | Loss Scorecard의 주 측정값. |
| `final_estimated_cost` | Decimal | 최종 추정 손실 비용 ($). | `$4,567.89` | 이 값이 Red Warning의 핵심 트리거입니다. |
| `warning_state` | Enum (Enum) | 현재 시스템이 인지한 경고 상태. | `CRITICAL` / `WARNING` / `SAFE` | **[필수]** UI 렌더링 및 비주얼 효과 결정에 사용됩니다. |
| `transition_log` | List[`StateChange`] | 점수가 변화할 때의 상세 기록 배열. | `[...]` | **[핵심]** 상태 전이 히스토리를 제공하여 클라이언트가 애니메이션을 구현합니다. |

#### StateChange Object Structure (Critical for Animation)
```json
{
  "timestamp": "2026-11-27T...", 
  "previous_score": 0.3, 
  "current_score": 0.8, 
  "change_amount": "+0.5", // 변화 폭 (Float)
  "trigger_event": "Data Integrity Failure Detected" // 원인 설명
}
```

### 🚨 Error Handling Schema (Failure - Standard HTTP Status Codes)
| Status Code | Error Code | Description | Client Action Required |
| :--- | :--- | :--- | :--- |
| `400 Bad Request` | `INVALID_INPUT` | 필수 입력 필드 누락 또는 형식 오류. | 사용자에게 구체적인 누락 필드를 알려주고 재전송 유도. |
| `401 Unauthorized` | `AUTH_MISSING` | API Key/Token 만료 또는 누락. | 백엔드 인증 시스템을 점검하고, 새로운 토큰 발급 프로세스를 안내. |
| `503 Service Unavailable` | `ENGINE_FAILURE` | 내부 엔진(e.g., IP Similarity Engine) 실행 중 오류 발생. | 재시도 로직 구현 (Retry Mechanism). 실패 원인을 간접적으로 알려줌. |