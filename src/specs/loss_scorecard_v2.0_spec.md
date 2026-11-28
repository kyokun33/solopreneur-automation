# 💻 Loss Scorecard State Machine V2.0: Developer Interaction Specification v1.0
**[작성 목적]**: Frontend & Backend 개발팀이 E2E 테스트 환경을 구축하고, 모든 상태 전이를 구현하기 위한 단일 진실 공급원(Single Source of Truth) 명세서. 이 문서는 'Loss Score'라는 핵심 지표를 중심으로 UI/UX와 비즈니스 로직의 경계를 정의합니다.

---
## 1. 📊 Loss Scorecard State Machine Definition (V2.0)

**핵심 원칙**: 모든 상태 전이는 **외부 입력(User Input)** 또는 **시간 흐름(Time Elapsed)**에 의해 발생하며, 시스템은 현재 상태를 기반으로 다음 상태와 필요한 시각 효과를 계산합니다.

| State ID | 이름 | Loss Score Range (Trigger) | 핵심 UX 목표 | 주요 행동 유도 (CTA) |
| :--- | :--- | :--- | :--- | :--- |
| `S_INITIAL` | 초기 탐색 단계 | $0 - $1,499.99 | **정보 제공 및 호기심 자극** | '업무 시간 입력' 유도 (Focus) |
| `S_NORMAL_RISK` | 정상 경고 단계 | $1,500 - $14,999.99 | **위험 인지(Awareness) 유발** | 추가 리스크 항목 진단 요청 ($97 Tier) |
| `S_HIGH_WARNING` | 심각 손실 경고 | $15,000 - $249,999.99 | **공포 자극 및 데이터 증명 요구** | 상세 보고서 요청 (Mini-Commitment Loop 시작) |
| `S_CRITICAL_COMMITMENT` | 치명적 위험/전환점 | $250,000+ | **결정적 액션 강제 (Funnel Bottom)** | 유료 진단 상품 구매 ($197 Tier 이상) |

### 🔄 State Transition Logic & API Sequence
State Machine의 핵심은 상태 전이(Transition)를 유발하는 이벤트와 그에 따른 API 호출입니다.

| From State | Trigger Event (Input) | Required Action (API Call) | Next State | Side Effect / Visual Rule |
| :--- | :--- | :--- | :--- | :--- |
| `S_INITIAL` | User submits Work Hours (`hours: 10`) | POST `/api/v1/calculate-loss` (Payload: `{ hours, risk_level: 'low' }`) | `S_NORMAL_RISK` | **Transition:** Loss Score Card Counter starts animating. **Effect:** None. |
| `S_NORMAL_RISK` | User submits High Risk Data (`risk_data: true`) | POST `/api/v1/calculate-loss` (Payload: `{ ... }`) | `S_HIGH_WARNING` | **Transition:** Loss Score Card Counter animates to new value. **Effect:** Red Warning Filter (Level 1) 발동. |
| `S_NORMAL_RISK` | API returns loss > $250k | N/A (Backend Trigger) | `S_CRITICAL_COMMITMENT` | **Transition:** Immediate full screen takeover. **Effect:** Glitch Effect + Red Warning Filter (Level 3). |
| `S_HIGH_WARNING` | User clicks CTA (`commit: true`) | POST `/api/v1/mini-commitment` (Payload: `{ user_id }`) | `S_CRITICAL_COMMITMENT` | **Transition:** Commitment Gateway 활성화. **Effect:** Focus on $199 Mini-Commitment Loop. |

---
## 2. 🔌 API Contract Specification (Backend & Frontend)

**Endpoint**: `/api/v1/calculate-loss` (POST)
**Authentication**: Rate Limiting 필수 / JWT Bearer Token 사용 권장.

### Request Body Schema (TypeScript / JSON)
```typescript
interface LossCalculationRequest {
    // 1. 핵심 입력 데이터
    workHours: number; // 사용자 입력 시간 (필수)
    riskSources: Array<{ sourceId: string; severity: 'LOW' | 'MEDIUM' | 'HIGH'; impact_cost: number }>; // 리스크 항목 배열
    // 2. 현재 시스템 상태 정보 (Contextual Data)
    userSessionData: { sessionId: string; lastActionTime: Date };
}
```

### Response Body Schema (TypeScript / JSON)
이 응답은 모든 클라이언트 컴포넌트의 **단일 진실 공급원(Single Source of Truth)**입니다.

```typescript
interface LossCalculationResponse {
    // 1. 계산 결과 (핵심 지표)
    calculatedLossScore: number; // 최종 손실 점수 (Float, $ 기호 포함 가능하게 처리)
    currentRiskStateId: 'S_INITIAL' | 'S_NORMAL_RISK' | 'S_HIGH_WARNING' | 'S_CRITICAL_COMMITMENT'; 

    // 2. 비즈니스 로직 판단 근거 (디버깅 및 테스트용)
    riskLevelDetails: {
        isHighRiskThresholdMet: boolean; // $15k 초과 여부
        isCriticalThresholdMet: boolean; // $250k 초과 여부
    };

    // 3. UI/UX 동작 명세 (Frontend가 직접 사용)
    visualDirectives: {
        triggerEffectActive: 'none' | 'red_warning' | 'glitch';
        effectIntensityLevel: 1 | 2 | 3; // 1: Mild, 3: Extreme
        ctaVisible: boolean; // Mini-Commitment Loop CTA 표시 여부
    }
}
```

---
## 3. ✨ Behavioral & Visual Specification (CSS/JS)

### A. Red Warning Filter (Level Control)
이 필터는 단순한 배경색 변경이 아닌, **공포와 위기감**을 조성하는 시각적 장치입니다.

*   **Trigger**: `LossCalculationResponse.visualDirectives.effectIntensityLevel`에 의해 결정됩니다.
    *   **Level 1 (`S_NORMAL_RISK`)**: 배경 전체가 아닌, '손실 점수 위젯'과 '경고 메시지 블록' 주변에 미세한 **Red Overlay Gradient (Opacity: 0.15)** 적용.
    *   **Level 2 (`S_HIGH_WARNING`)**: 화면의 일정 영역(특히 메인 콘텐츠)을 감싸는 **Semi-Transparent Red Filter (Opacity: 0.3)**를 DOM에 추가하고, 모든 주요 요소에 `filter: hue-rotate(-10deg);` 등의 미세한 왜곡 효과를 적용합니다.
    *   **Level 3 (`S_CRITICAL_COMMITMENT`)**: **전역(Global) Red Filter (Opacity: 0.7)**를 적용하고, 모든 애니메이션 속도를 의도적으로 느리게 만들어 불안정한 느낌을 증폭시킵니다.

### B. Glitch Effect
*   **Trigger**: 오직 `S_CRITICAL_COMMITMENT` 상태로 전이할 때만 발동합니다. (시스템적 오류를 암시).
*   **Implementation Detail**:
    1.  DOM 전체에 0.2초 동안 **CSS Keyframe Animation (`@keyframes glitch`)**을 적용하여, 색상 채널(R/G/B)의 미세한 오프셋 및 수평 번짐(Shift) 효과를 연달아 발생시킵니다.
    2.  애니메이션 직후 (0.5초 지연), 화면 전체에 **깜빡임(Flicker)** 애니메이션을 추가하여 "시스템 오류"라는 심리적 메시지를 전달합니다.

### C. Mini-Commitment Loop Gateway (The $199 Funnel)
*   **Trigger**: `S_HIGH_WARNING` 상태 진입 후, 사용자가 명시적으로 '추가 분석' 또는 '진단 요청' CTA를 클릭했을 때 활성화됩니다.
*   **Behavior**: 이 게이트웨이는 페이지의 가장 높은 가시성(Highest Visibility) 영역에 위치해야 하며, 배경색이 일시적으로 어두워지고 (Dimming), 모든 시선이 $199 상품 블록으로 강제 집중되어야 합니다.

---