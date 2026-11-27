# 🔴 Anti-Loss Funnel Core Component: Red Warning & Glitch Effect Specification (Developer Kit v1.0)
**[목적]**: 사용자에게 정량화된 손실(Time-Loss & Risk Cost)을 직면하게 하여 위기감(Fear)을 극대화하고, 즉각적인 '진단 보고서 요청'이라는 행동 유도를 목표로 합니다. 이 효과는 웹사이트 로드 시 또는 핵심 손실 수치가 계산되는 순간에 트리거됩니다.

---

## ⚙️ 1. 시스템 개요 및 동작 원리 (System Overview)
**[트리거 조건]**: 사용자가 페이지를 스크롤하여 '손실 카운터(Loss Counter)' 섹션에 도달하거나, 혹은 비즈니스 로직이 손실 금액을 계산하는 순간 (e.g., `loss_amount > $50,000`).
**[기본 상태]**: 배경은 `#FFFFFF` 또는 `#F5F5F7`. 시야가 깨끗하고 전문적입니다.
**[경고 활성화 상태]**: 전체 화면에 오버레이 필터(Overlay Filter)가 적용되며, Red Warning과 Glitch 효과가 순차적으로 발생합니다.

---

## 🖼️ 2. 비주얼 스펙 (Visual Specification)

### A. Red Warning Overlay Filter
*   **컬러 코드**: `#CC3333` (Loss Accent).
*   **효과**: 전체 화면에 투명도(Opacity)가 높은 반투명 빨간색 레이어가 씌워집니다. 이 필터는 대비를 떨어뜨리고 시야를 왜곡하여 '비상 상황'의 느낌을 물리적으로 전달합니다.
*   **CSS/JS 구현 포인트**:
    *   `position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 9999;`
    *   초기 `opacity`는 `0.0`으로 설정하고, 트리거 시 `opacity`를 **`0.3 ~ 0.5`**로 애니메이션 인(In)합니다.

### B. Glitch Effect (기술적 스펙 시각화)
이 효과는 단순한 CSS 필터가 아닌, 여러 단계의 *디지털 오류*처럼 보이게 하는 레이어 조합입니다.
1.  **Chromatic Aberration (색수차)**: 텍스트/이미지 가장자리에 RGB 채널 분리 왜곡을 적용합니다. (`filter: url(#chroma-shift)` 사용 권장)
2.  **Horizontal Shift**: 화면 좌우로 미세하게 번지고 떨리는 효과를 반복적으로 발생시킵니다.
3.  **Scanline/Noise**: 필름 그레인이나 스캔 라인 노이즈가 배경에 덧씌워져 데이터 무결성이 깨진 듯한 느낌을 부여합니다.

---

## 🎬 3. 애니메이션 키프레임 스토리보드 (Developer Flow Guide)
전체 효과는 총 **2~3초**에 걸쳐 완료되며, 다음의 순서와 타이밍(Timing)을 엄격하게 지켜야 합니다.

| Time | Duration | Event Trigger | Visual Effect (기술적 스펙) | Description & Action Items |
| :---: | :---: | :---: | :---: | :---: |
| **T=0s** | 0.1s | **[INIT]** 손실 계산 API 호출 성공 시 | Opacity 0 / Filter Off | 모든 요소가 정상적으로 보임 (Normal State). |
| **T=0.1s** | 0.2s | **[TRIGGER]** Red Warning 발동 시작 | Glitch Effect Start (Low Intensity) | 화면의 가장자리에서 미세한 '지직'거리는 노이즈와 색수차(Chromatic Aberration)가 갑작스럽게 나타납니다. 글자가 순간적으로 왜곡되어 보입니다. |
| **T=0.3s** | 1.0s | **[MAX STRESS]** Red Warning 필터 최대 투사 | Opacity $\to$ 0.4 / Glitch Max | 가장 강한 위기감 구간. 빨간색 오버레이가 갑작스럽게 커지며, 모든 콘텐츠(H1, 수치 등)에 걸쳐 글리치가 최고조로 발생합니다. 이 순간 **'손실 점수표'의 손실액($X만)**이 화면 중앙에서 가장 강력하게 깜빡이며 노출되어야 합니다. |
| **T=1.3s** | 0.5s | **[FADE OUT]** 시스템 경고 완화 단계 | Opacity $\to$ 0.2 / Glitch Decay | 빨간색 오버레이가 서서히 투명해지고, 글리치 효과의 빈도와 강도가 감소합니다. 사용자의 주의를 '다음 행동(CTA)'으로 유도하는 시점입니다. |
| **T=1.8s** | 0.2s | **[RESOLUTION]** 해결책 제시 (How-To 섹션) | Opacity $\to$ 0 / Filter Off | Red Warning 필터가 완전히 사라지고, 배경과 모든 요소들이 깨끗하고 명료한 색상(Primary Accent: `#0066CC`)으로 전환됩니다. 시각적 안정감을 회복시켜 신뢰도를 확보합니다. |

---

## 📐 4. 코드/CSS 구현 가이드 (Developer Implementation Guide)
### A. CSS Transition Properties
*   `transition-property`: `opacity, filter, transform`
*   `transition-timing-function`: `cubic-bezier(0.25, 1, 0.5, 1)` (부드러운 가속/감속)
*   `transition-duration`: 3s (전체 루프 기준)

### B. JavaScript Control Flow
*   **Loss Calculation Event Listener**: `window.addEventListener('scroll', handleScroll);` 또는 API 호출 성공 시 `triggerWarningEffect(lossAmount)` 함수 실행.
*   **Key Function**: `triggerWarningEffect(amount)`는 위 표의 타이밍에 맞춰 CSS 클래스(`is-warning`, `glitch-active`)를 추가/제거하고, 손실 금액을 계산하여 DOM에 삽입합니다.

---