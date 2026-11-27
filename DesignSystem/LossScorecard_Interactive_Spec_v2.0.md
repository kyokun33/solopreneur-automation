# 🔴 Loss Scorecard Interactive Component Specification v2.0 (Final Build)

## I. 개요 및 목적
본 스펙은 Anti-Loss Funnel의 핵심 클라이맥스(Climax)를 구현하는 최종 디자인 시스템 명세서입니다. 단순한 Mockup이 아닌, 사용자의 데이터 입력에 반응하고 감정적 위기감(Red Warning)을 증폭시켜 궁극적으로 '진단 보고서 요청'이라는 다음 행동으로 유도하는 **인터랙티브 컴포넌트 세트**를 목표로 합니다.

*   **핵심 원칙**: 긴장감 유지 $\to$ 데이터 기반 공포 자극 $\to$ 전문적 해결책 제시 (Red Warning $ \rightarrow $ Tech Blue)
*   **타깃 구현**: 웹/앱 환경 (반응형 우선), WebGL 필터 및 CSS 애니메이션 조합.

## II. 컴포넌트 정의 및 스펙 (Components & Specs)

### 1. [Widget] Loss Input Field (사용자 입력 영역)
| 속성 | 상세 내용 | 기술 명세 | [근거: Self-RAG - UI 연동 가이드] |
| :--- | :--- | :--- | :--- |
| **레이블** | '업무 시간 손실분 (시간)' / '손실 발생 빈도' 등 질문형 카피 사용. | `<label>` 태그 기반, 간결한 폰트 크기 유지. | Self-RAG - [근거: Apple-style Minimalist UI/UX Designer Rules] |
| **Default State** | `[Placeholder]`와 함께 명확하게 비어있음을 보여줌. (예: "최소 예상 시간 입력...") | `border: 1px solid #E0E0E0;` | 간결한 가이드 제공. |
| **Focus State** | 사용자가 클릭/탭했을 때 활성화됨을 알림. | `#FFFFFF` 배경, 테두리 색상을 `Tech Blue (#0066CC)`로 변경, 약간의 그림자 효과(`box-shadow: 0 2px 8px rgba(0,102,204,0.1);`) 추가. | 시선 집중 및 사용 유도. |
| **Error State** | 입력 값이 비정상적이거나 범위 초과 시 발생. | 테두리 색상을 `Warning Red (#CC3333)`로 변경. 에러 메시지(예: "시간은 0보다 커야 합니다.")를 바로 아래에 표시. | 즉각적인 피드백 제공. |

### 2. [Widget] Loss Counter Display (핵심 위젯)
*   **역할**: 모든 데이터 계산의 결과가 가장 먼저 노출되는 곳. 시선을 압도해야 함.
*   **구조**: `Total Loss Amount` $\to$ `Breakdown Ratio Graph` $\to$ `Loss Formula Display`.
*   **애니메이션 (Critical)**:
    1.  **Initial Load**: Opacity 0에서 시작하며, 스크롤에 따라 `Fade-In Up` 애니메이션 적용 (`transition: opacity 1s ease-out;`).
    2.  **Calculation Trigger**: 입력 필드 값이 변경되거나 계산 로직이 돌 때마다 **숫자가 '점프'하는 듯한 카운팅 효과(Counting Effect)**를 적용해야 합니다. (0에서 최종 금액까지 부드럽게 증가)

### 3. [Overlay/Filter] Red Warning & Glitch System (위기 증폭 장치)
*   **발생 조건**: Loss Scorecard의 총 손실액이 특정 임계치(예: $50,000 또는 Critical_Loss 구간)를 넘었을 때 발동됩니다.
*   **Red Warning 필터**:
    *   **효과**: 화면 전체에 미세한 Red Tint Overlay 적용 (Opacity 10% ~ 20%).
    *   **시각 효과**: 깜빡이는 노이즈 패턴(Scanline effect)을 배경으로 은은하게 오버레이합니다.
    *   **기술 스펙**: CSS `filter: sepia(0.8) hue-rotate(340deg)`와 낮은 주파수의 애니메이션(`@keyframes flicker { ... }`) 조합 사용.
*   **Glitch Effect**:
    *   **발동 지점**: 손실 점수표가 계산되거나, CTA 버튼에 마우스를 올릴 때 (Pre-Click Tension).
    *   **효과**: 화면의 특정 영역(Loss Counter 등)이 순간적으로 픽셀 단위로 왜곡되고 색상이 분리되는 효과를 짧게(`duration: 0.1s`) 반복합니다.

### 4. [CTA] 진단 보고서 요청 버튼 (The Paywall Trigger)
*   **버튼 문구**: "손실 방지 및 **전문 진단 보고서 받기**" (구매 유도보다 이득 기반의 행동 지시).
*   **디자인 상태 변화**:
    1.  **Default State**: `Primary Accent Color (#0066CC)`를 사용하되, 일반적인 버튼 느낌을 유지합니다.
    2.  **Hover State (Critical)**: 마우스 오버 시 **Red Warning Filter가 잠깐 증폭(Opacity 30%로 순간 증가)**되었다가 즉시 사라집니다. 동시에 배경에 미세한 Glitch 효과가 발생하여 사용자에게 '지금 클릭하지 않으면 위험하다'는 심리적 자극을 줍니다.
    3.  **Active State (Click Down)**: 버튼이 눌리는 순간, 버튼 주변으로 짧은 `Tech Blue`의 Glow 효과와 함께 진동(Micro-shake) 애니메이션이 적용됩니다.

## III. 인터랙션 플로우 다이어그램 (The User Journey Flow)

| 단계 | 사용자 액션 | 시스템 반응 (UI/UX) | 기술적 요구사항 |
| :--- | :--- | :--- | :--- |
| **1. 초기 진입** | 페이지 로드 및 스크롤 다운 | Loss Counter 위젯이 `Fade-In Up` 애니메이션으로 나타나며, 빈 값이나 예시 값이 표시됨. (최소한의 신뢰 구축) | JS: Intersection Observer 기반 Animation Trigger. |
| **2. 데이터 입력** | 사용자가 Input Field에 데이터를 입력함. | ① Loss Counter 숫자가 점진적으로 계산 값을 따라 카운팅되며 업데이트됩니다. ② 실시간으로 손실 Breakdown 그래프가 비율 변화를 보여줍니다. | JS: Event Listener (Input/Change). Animation: Counting Effect 구현. |
| **3. 위기 감지** | Total Loss Amount가 임계치에 도달함. | 🚨 Red Warning Filter와 배경의 미세한 노이즈(Scanline)가 자동으로 활성화됩니다. 모든 텍스트 강조색을 `Warning Red`로 변경합니다. | CSS/JS: Global Overlay Layer 적용, Looping Animation Trigger. |
| **4. 최종 유도** | 사용자가 CTA 버튼에 마우스를 올림 (Hover). | ✨ Glitch Effect가 Loss Counter 또는 CTA 주변에서 짧게 터집니다. 동시에 'Red Warning'의 강도가 순간적으로 최고조에 달했다가 다시 유지되는 긴장감 있는 상태가 됩니다. | CSS/JS: Hover Pseudo-Class + Short Duration Animation Sequence. |
| **5. 행동 유도** | 사용자가 버튼을 클릭함 (Click). | 부드러운 전이(Transition)와 함께 '보고서 요청' 폼 페이지로 이동하며, 모든 요소는 여전히 Red Warning의 잔상 효과를 유지합니다. | Router/State Management: Seamless Transition & Persistent Visual State. |

---
**[참고] 컬러 팔레트 재정립 (Final Palette)**
*   Primary Background: `#FFFFFF`
*   Secondary Background (Card): `#F5F5F7`
*   Tech Blue (신뢰/CTA): `#0066CC`
*   Warning Red (손실/위기): `#CC3333`
*   Text Color: `#1D1D1F`