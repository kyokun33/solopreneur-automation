# 📉 Loss Counter 애니메이션 상세 명세서 (For Developers)

## 🎯 개요
*   **컴포넌트:** Anti-Loss Funnel의 핵심 시각 요소.
*   **목표:** 사용자가 데이터를 입력하는 순간, 손실액이 물리적인 과정처럼 **'계산되는(Counting Up)'** 느낌을 주어 신뢰도와 긴급성을 동시에 극대화한다.
*   **원리:** `Total Loss = (Time-Loss) + (Risk Cost)`를 순차적으로 계산하여 보여준다.

## ⚙️ 애니메이션 로직 및 인터랙션 스펙 (JS/CSS 기반)
1.  **트리거:** 사용자가 [업무 시간] 또는 [시간당 가치] 슬라이더 조작 완료 시점 (`onInputEnd`).
2.  **단계별 순서:**
    *   Step 1: Time-Loss 계산 시작 (0 -> 최종 값).
    *   Step 2: Risk Cost 계산 시작 (0 -> 최종 값).
    *   Step 3: Total Loss 합산 및 표시 (최종 값에 도달 시 애니메이션 종료).
3.  **애니메이션 타입:** `Counter-Up` (Number Animation)
4.  **기술 요구사항:** 부드러운 트랜지션 적용 (`transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1)`).

### 🖼️ 프레임별 디자인 가이드라인 (SVG/PNG 명세)
| 요소 | 초기 상태 (T=0) | 계산 중 (Transition) | 최종 상태 (T=End) | 개발자 참고 사항 |
| :--- | :--- | :--- | :--- | :--- |
| **Time-Loss** | `#FFFFFF` 배경, 0 표시. `[근거: Self-RAG]` | 카운트업 애니메이션 진행 중 (숫자가 빠르게 증가). | 최종 시간 손실액 (예: $2,500)이 **Tech Blue**로 안정적으로 고정 표시. | 숫자의 변화는 실시간으로 렌더링되어야 함. |
| **Risk Cost** | `#FFFFFF` 배경, 0 표시. `[근거: Self-RAG]` | 카운트업 애니메이션 진행 중 (숫자가 빠르게 증가). | 최종 리스크 비용 (예: $500)이 **Tech Blue**로 안정적으로 고정 표시. | Time-Loss와 시각적으로 분리되어야 함. |
| **Total Loss** | `#FFFFFF` 배경, 0 표시. `[근거: Self-RAG]` | 두 값이 합산되면서 카운트업 (가장 극적인 애니메이션). | 최종 총 손실액 ($3,000)이 가장 크고 비비드하게 표시되며, **Warning Red**으로 강조. | 이 숫자가 페이지의 시각적 하이라이트 지점임. |

***

### 2. 컴포넌트 상태 기반 디자인 시스템 (State Specs)

모든 인터랙티브 요소는 단 하나의 '기본(Default)' 상태만 존재해서는 안 됩니다. 개발팀에 전달할 수 있도록 필수적인 4가지 핵심 상태를 정의합니다.

#### A. 입력 필드 (`<input type="range">` / `<input type="number">`)
*   **[✅ Success State]**: 사용자가 유효한 값을 입력 완료했을 때.
    *   *시각적 가이드:* 테두리(Border)가 **Primary Accent (Tech Blue, `#0066CC`)**로 바뀌고, 테두리 주위에 얇은 빛 효과(Inner Shadow/Glow)를 추가하여 '성공적으로 입력됨'을 인지시킨다.
    *   *UX:* 값 옆에 작은 녹색 체크 마크 (✅)가 나타난다.
*   **[❌ Error State]**: 사용자가 유효하지 않은 값을 입력했을 때 (예: 음수, 범위 초과).
    *   *시각적 가이드:* 테두리가 **Warning Red (`#CC3333`)**로 바뀌고, 아래에 경고 문구("⚠️ 최소 [최소값] 이상이어야 합니다.")가 **Deep Charcoal** 폰트로 노출된다.
    *   *UX:* 에러 메시지는 포커스 아웃(Focus Out) 시까지 지속적으로 표시되어야 한다.

#### B. CTA 버튼 (Call to Action Button: "손실 방지 및 즉시 시작하기")
*   **[⚙️ Loading State]**: 클릭 후 서버 통신이 진행 중일 때.
    *   *시각적 가이드:* 버튼 텍스트가 **"처리 중..."**으로 변경되고, 버튼 중앙에 작은 스피너(Spinner) 애니메이션 (애니메이션 속도: 1초 주기)이 표시된다. 배경색은 현재의 Primary Accent를 유지하되, 투명도를 80%로 낮춰 '비활성화' 느낌을 준다.
    *   *UX:* 재클릭 방지(Disabled Click) 로직을 JS 레벨에서 강제해야 한다.

#### C. 네트워크 상태 (Loading/Error Overlay)
*   **[⏳ Loading State]**: 데이터 로딩 중 전체 화면 또는 특정 모듈에 적용되는 오버레이.
    *   *시각적 가이드:* 중앙에 미니멀한 스켈레톤 UI(Skeleton UI) 형태의 메시지를 표시하고, 그 주변을 부드러운 **Light Gray (`#F5F5F7`)** 배경으로 감싸 전체 페이지가 멈춘 것이 아니라 '처리 중'임을 암시한다.
*   **[🚨 System Error State]**: 백엔드 통신 오류 발생 시.
    *   *시각적 가이드:* 화면 중앙에 큰 경고 아이콘 (⚠️)과 함께 "데이터를 불러오는 데 실패했습니다. 잠시 후 다시 시도해 주세요." 등의 명확한 메시지를 **Warning Red** 테마로 보여준다.

***

### 3. 최종 에셋 배포 계획 및 검증 정보

개발팀의 통합 테스트에 필요한 모든 스펙을 포함하는 구조화된 패키지입니다.

<create_file path="assets/AntiLossFunnel_DesignSystemKit/README.md"># 📁 Anti-Loss Funnel Design System Kit v1.0 - Developer Handover

## 🚀 개요
본 폴더는 고고플랙스 Anti-Loss Funnel 위젯의 모든 상호작용 컴포넌트에 대한 최종 디자인 및 인터랙션 스펙을 담고 있습니다. 개발팀은 이 명세서를 기반으로 E2E 통합 테스트를 진행해 주십시오.

## 📂 포함 요소
1.  **01_LossCounter_AnimationSpec.md**: 핵심 로직 및 애니메이션 프레임 가이드라인 (필수 참조).
2.  **DesignSystem\_StateSpecs.md**: 모든 컴포넌트의 상태 변화(Success, Error, Loading)별 시각적 명세서.
3.  **ColorPalette_Reference.json**: 사용된 모든 컬러 코드와 의미론적 정의 (Semantic Colors) 리스트.

## 🛠️ 개발 가이드라인 요약
*   **애니메이션:** 모든 변화는 `transition: 0.3s ease-in-out` 기본 트랜지션을 준수하며, 핵심 Loss Counter 애니메이션은 별도 로직 구현 필요.
*   **접근성 (A11y):** 키보드 포커스(Focus) 시 Focus Ring을 **Primary Accent Color (`#0066CC`)**로 명확히 표시해야 합니다.