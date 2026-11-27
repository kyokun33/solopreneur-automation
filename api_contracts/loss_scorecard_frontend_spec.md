# Loss Scorecard Component Library Specification (React/TypeScript)

## ⚛️ Core Components
모든 컴포넌트는 타입스크립트(TypeScript)로 작성되며, 상태 변화에 반응하는 로직이 포함되어야 합니다.

### 1. `<LossScoreCard />` (Parent Container)
*   **Responsibility**: 전체 Scorecard의 레이아웃 및 데이터 흐름 관리. API 호출을 담당하고, `CalculationResponse`를 받아 하위 컴포넌트들에게 Props로 분배합니다.
*   **State Management**: `useState<CalculationResponse | null>` 형태로 API 결과를 저장하며, 로딩/에러 상태(Loading/Error) 처리를 최우선으로 합니다.
*   **API Call Flow**: 사용자 액션 $\rightarrow$ (Async Call to `/api/v1/risk/calculate-score`) $\rightarrow$ `loading: true` $\rightarrow$ Success/Failure 처리.

### 2. `<DynamicLossCounter />`
*   **Responsibility**: `$final_estimated_cost` 값을 시각적으로 카운트업(Counting Up)합니다.
*   **UX Requirement**: 단순한 숫자 변경이 아닌, **'점진적인 증가 애니메이션'**을 사용해야 합니다 (Transition: 0.3s ease-in-out).
*   **Props**: `initialValue: number`, `finalValue: number`

### 3. `<RedWarningFilter />`
*   **Responsibility**: 리스크 점수 변화(`StateChange`)에 반응하여 시각적 필터를 적용합니다.
*   **Logic**: Red Warning은 단순히 'Critical' 상태일 때만 작동하는 것이 아니라, **점수의 변화 폭(Change Amount)**이 특정 임계값($\Delta > 0.3$)을 초과할 때 즉시 트리거되어야 합니다.
*   **Props**: `currentScore: number`, `previousScore: number`

### 4. `<TransitionHistoryLog />` (The most complex component)
*   **Responsibility**: API가 제공하는 `transition_log` 배열을 순회하며, 모든 상태 변화(`StateChange`)를 시간순으로 리스트업합니다.
*   **Display Detail**: 각 항목은 다음 정보를 포함해야 합니다: 1) 발생 시점(Timestamp), 2) 이전 점수/현재 점수, 3) **변화 폭(`+0.5`와 같은 값)**, 4) 원인(`trigger_event`).
*   **Interactivity**: 이 목록이 스크롤되면서 `RedWarningFilter`가 간헐적으로 재적용되는 시뮬레이션 효과를 주면 몰입도가 극대화됩니다.