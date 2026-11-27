# 🎯 고고플랙스 Anti-Loss Funnel User Flow Map v2.0
**[목표]**: 리스크 인지 $\rightarrow$ 위기감 증폭 $\rightarrow$ Pro Tier 전환 유도 (마케팅 가이드라인)

## 1. 시스템 구조 개요
*   **Funnel 논리**: Awareness (손실 인식) $\rightarrow$ Interest (위험 증가) $\rightarrow$ Desire (해결책 발견) $\rightarrow$ Action (구매 확정).
*   **핵심 위젯**: Loss Counter Widget (Loss = 시간 * 가치 + 리스크 비용).

## 2. 섹션별 디자인 및 인터랙션 명세 (Mockup Detail)

### A. Hero Section: The Hook & Initial Diagnosis
*   **Layout**: 중앙 정렬, 극도의 여백(Whitespace) 활용.
*   **H1**: `Anti-Loss Hook` 카피 사용. 폰트 가중치(Weight) 최대화.
*   **Interaction**: 페이지 로드 시 Loss Counter가 Opacity 0 $\rightarrow$ Fade-In Up (Transition: 0.5s ease-out).

### B. Diagnosis Section: Red Warning Escalation Core
*   **Trigger**: 사용자가 입력값 변경 또는 스크롤 위치 변화에 따라 실시간으로 손실 점수(Score)가 계산됨.
*   **State Transition Logic**:
    *   `IF (Loss Score > $2,000)` $\rightarrow$ **TRIGGER RED WARNING**.
    *   **Visual Effect**: 배경 전체에 `backdrop-filter: blur()`를 적용하고 `#CC3333`의 Red Filter 오버레이. 미세한 Glitch 효과 애니메이션 필수.
    *   **UX Copy**: "🚨 경고: 귀하의 데이터는 현재 심각한 법적 리스크 상태에 있습니다." (글자 크기 최대, 굵은 볼드체)
*   **CTA Change**: 기존 CTA가 '진단 시작'에서 **'위험 보고서 요청 및 방어 계획 수립하기'**로 즉시 변경.

### C. Solution Section: Pro Tier Positioning
*   **Transition Trigger**: 사용자가 Red Warning 상태를 충분히 경험한 후, 페이지 하단의 Solution 섹션으로 자연스럽게 스크롤 다운할 때 발생.
*   **Design Focus**: 3가지 플랜을 제시하되, **Pro Tier($499~$699)**에만 'Shield' 아이콘과 함께 추가적인 강조 영역(Secondary Accent) 부여.
*   **Copy Emphasis**: "단순한 컨설팅이 아닌, **시스템적 리스크 전이 로직 기반의 법적 책임 증명 아키텍처**를 확보합니다." (권위적 용어 사용).

### D. Paywall: The Final Call to Action
*   **Layout**: 화면 전체를 가로지르는 Full-Width Section으로 배치하여 긴급성 극대화.
*   **Key Visual**: 이전 단계에서 계산된 손실액(`Loss Scorecard`)과, Pro Tier 도입 후 예상되는 회수 가능 금액을 시각적으로 대비시키는 인포그래픽 요소를 삽입. (Before: 🔴 Loss / After: 🔵 Gain).
*   **Final CTA**: **"손실 방지 계획 수립 및 Pro Tier 구매하기"**. 이 버튼은 모든 과정의 최종 목표이자 유일한 탈출구처럼 느껴져야 한다.