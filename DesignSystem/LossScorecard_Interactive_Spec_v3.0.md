# 🔴 Loss Scorecard 인터랙티브 디자인 시스템 명세서 v3.0 (Final Spec)

## I. 개요 및 목적
본 문서는 고고플랙스 Anti-Loss Funnel의 핵심 컴포넌트인 **손실 점수(Loss Score)** 변화에 따른 사용자 경험(UX)과 시각적 위기감(Visual Panic)을 극대화하기 위한 디자인 가이드라인입니다.

**목표:**
1.  상태 전이(`Apathy` $\to$ `Warning` $\to$ `Critical`)에 따라 컴포넌트의 **강도와 빈도**를 점진적으로 증폭시켜 공포(Fear) 기반의 행동 유도를 극대화한다.
2.  모든 시각적 효과는 과장되어서는 안 되며, '현실적인 위협'처럼 느껴지도록 정교하게 제어되어야 한다.

## II. 핵심 인터랙티브 컴포넌트 세부 명세

### 1. Red Warning Filter (`Visual_Warning`)
*   **기능:** 배경 전체 또는 핵심 요소에 경고색을 오버레이하여 '위험 지역'임을 시각적으로 알림.
*   **적용 원리:** 투명도(Opacity)와 색상 채도(Saturation)의 증가를 통해 위험 수준을 명확히 구분한다.

| 상태 (State) | 점수 범위 (Loss Score) | 필터 강도 (Intensity) | 오버레이 컬러 (HEX/RGB) | CSS 속성 제어 (Codeable Property) |
| :--- | :--- | :--- | :--- | :--- |
| **Apathy** | 0 ~ $1,500 | None (0%) | `transparent` | `opacity: 0.0` |
| **Warning** | $1,501 ~ $4,999 | Subtle Overlay (20%~40%) | `#CC3333` (Red) @ Opacity 0.15 | `background-color: rgba(204, 51, 51, [Opacity]);` |
| **Critical** | $5,000+ | Severe Overlay (60%~80%) | `#CC3333` (Red) @ Opacity 0.6 | `background-color: rgba(204, 51, 51, [Opacity]);` |

*   **트리거 포인트:** Loss Score가 특정 임계값($1,500 / $5,000)을 **상향 돌파하는 순간** (On Scroll/API Response).
*   **애니메이션 가이드:** `transition: background-color 0.4s ease-out;` 를 적용하여 점진적인 색 변화를 구현한다.

---

### 2. Glitch Effect (`Animation_Glitch`)
*   **기능:** 시스템의 '오류' 또는 '데이터 무결성 문제'를 시각적으로 표현하여 사용자에게 불안감(Anxiety)을 유발하는 트랜지언트 애니메이션.
*   **적용 원리:** 화면 요소에 미세한 떨림, 색상 분리(Chromatic Aberration), 블러 효과를 적용한다.

| 상태 (State) | 트리거 조건 (Trigger Condition) | 활성화 빈도 (Frequency) | 지속 시간 (Duration) | CSS 속성 제어 (Codeable Property) |
| :--- | :--- | :--- | :--- | :--- |
| **Apathy** | Never | N/A | N/A | Disabled |
| **Warning** | 10초마다 또는 스크롤 위치 변화 시 | Low (약 3~5초 간격) | 0.2초 | `animation: glitch-warning 0.2s steps(4);` |
| **Critical** | Loss Score가 $5,000을 초과할 때 | High (0.8초 ~ 1.5초 주기) | 0.3초 | `animation: glitch-critical 0.3s steps(6);` + `filter: contrast(120%);`|

*   **Glitch 핵심 구현 명세:**
    1.  **Horizontal Shift (좌우 이동):** 요소의 자식 레이어(`::before`, `::after`)를 사용하여 약간씩 X축으로 어긋나게 배치하고, 이를 짧은 시간 동안 반복적으로 변형시킨다.
        *   `transform: translate(-2px, 0) skewX(1deg);`
    2.  **Chromatic Aberration (색상 분리):** 요소의 색상을 R, G, B 세 개의 레이어로 복제하고, 각 레이어에 미세한 오프셋(`offset-x: -1px`, `+1px`)을 주어 색상이 층져 보이게 만든다.
        *   `filter: saturate(120%) contrast(110%);`

## III. 상태 전이 및 인터랙션 요약 (Interaction Flow)

| 이벤트/전환 | 발생 시점 (Trigger) | 시각적 변화 (Visual Effect) | 강도 증폭 로직 (Intensity Logic) |
| :--- | :--- | :--- | :--- |
| **Apathy $\to$ Warning** | Loss Score > $1,500 돌파 | 1. Red Filter 활성화 (`Opacity: 0.15`) <br> 2. Glitch 시작 (낮은 빈도) | *시각적 신호*: 색상과 떨림의 '존재감' 확보. **"주의 필요"** 메시지 강조. |
| **Warning $\to$ Critical** | Loss Score > $5,000 돌파 | 1. Red Filter 강하게 활성화 (`Opacity: 0.6`) <br> 2. Glitch 빈도 증가 & 강한 필터 적용 | *시각적 신호*: 색상과 떨림의 '빈도'와 '강도' 극대화. **"즉시 행동 필요"** 메시지 강조. |

***

## IV. 개발팀 참고 사항 (For Codari Team)
1.  **애니메이션 제어:** 모든 애니메이션은 `requestAnimationFrame` 기반으로 구현하여 성능 저하를 최소화해야 합니다. CSS 애니메이션만으로는 복잡한 상태 변화의 부드러움을 담보하기 어렵습니다.
2.  **상태 매핑 필수:** Red Filter와 Glitch Effect의 활성화 여부, 강도(Opacity 값), 빈도(Interval)는 반드시 `LossScorecardState` 타입에 의해 제어되어야 합니다. 하드코딩된 값을 사용해서는 안 됩니다.