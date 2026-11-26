# 🚀 고고플랙스 Loss Scorecard - 영상 제작용 Mockup Spec (Final Assets)

## I. 핵심 목표
최종 목적: 시청자에게 '위기감(Red)'을 느끼게 한 후, '해결책(Blue/Green)'으로 이끌어 CTA를 클릭하게 만든다.
디자인 철학: Apple-style Minimalism + Anti-Loss Funnel 극대화.

## II. 상태별 디자인 및 인터랙션 가이드

### 🟢 State 1: 정규 상태 (Baseline)
*   **Visual Tone:** 신뢰, 전문성, 안정감. (Primary Accent Blue `#0066CC`)
*   **스코어 게이지:** Opacity 0 $\to$ Smooth Fade-In Up. 배경색은 Pure White (`#FFFFFF`).
*   **손실 Breakdown:** 미미한 손실을 보여주며 '여유'를 느끼게 한다.

### 🔴 State 2: 리스크 감지 (The Panic Point)
*   **Visual Tone:** 공포, 긴급함, 위기감. (Loss Accent Red `#CC3333`)
*   **트리거:** 스코어의 급격한 하락 애니메이션(ScoreGauge component).
*   **레이아웃 변경:** 전체 화면에 얇은 경고 오버레이(`opacity: 0.15` Red)를 적용하여 긴장감을 조성한다.
*   **강조 요소:** `Loss Counter` 섹션이 가장 크고, 손실 원인(시간/비용)을 분리하여 명확히 보여준다.

### 💙 State 3: 회복 및 해결책 제시 (Resolution)
*   **Visual Tone:** 안도감, 통제력, 확신. (Primary Accent Blue `#0066CC`)
*   **트랜지션:** Red $\to$ Blue로의 급격한 색상 전환(Color Shift Animation). 스코어가 안정화되는 애니메이션을 사용한다.
*   **CTA 변화:** 경고성 CTA 문구에서 **'행동 유도형 (Action-Oriented)'** 문구로 변경하고, 버튼 주변에 은은한 성공 효과(Soft Glow)를 준다.

## III. 필수 에셋 및 변수 정의
1.  **Color Palette:** `#FFFFFF`, `#F5F5F7`, `#0066CC` (Primary), `#CC3333` (Loss), `#1D1D1F` (Text).
2.  **Typography:** Inter/Pretendard, H1은 Bold 48pt 이상으로 설정하여 위기감을 강조한다.
3.  **Animation Spec:** 모든 전환은 `transition: 0.3s ease-in-out`을 유지하며, Red $\to$ Blue 전환 시 **'물리적인 복구(Physical Recovery)'** 느낌의 스프링 애니메이션을 적용한다.