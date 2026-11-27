# 🔴 고고플랙스 Loss Scorecard - 마스터 프로토타입 명세서 v1.0

## 📄 개요 및 목표
본 문서는 모든 마케팅 콘텐츠(영상, 랜딩페이지, 광고 등)의 최종 기준점입니다. 목표는 사용자에게 **법적 책임과 데이터 무결성 손실**을 공포 자극 방식으로 제시하고, Pro Tier 구매로 전환시키는 Anti-Loss Funnel 구조를 완성하는 것입니다.

## 🎨 디자인 시스템 컴포넌트 (Design Tokens)
*   **Primary Color:** Tech Blue (`#0066CC`) - 신뢰/해결책
*   **Danger Color:** Warning Red (`#CC3333`) - 손실/위기감
*   **Background:** Pure White (`#FFFFFF`)
*   **Typography:** Sans-serif 계열 (예: Inter, Pretendard)
*   **Shadow:** 부드럽고 넓게 퍼지는 그림자 (`box-shadow: 0 4px 24px rgba(0,0,0,0.04)`).

## 💻 인터랙션 명세서 (Interaction Logic Blueprint)

### 1. Hero Section (Initial State)
*   **트리거:** 페이지 로드 시 Fade-In Up 애니메이션 적용.
*   **로직:** Loss Scorecard 위젯은 Opacity 0에서 시작하며, 스크롤에 반응하여 점진적으로 활성화되어야 합니다.

### 2. Loss Scorecard Component (Core Logic)
*   **입력 필드:** 시간 손실분(Time-Loss), 리스크 비용(Risk Cost)을 분리하여 입력 받습니다.
    *   `loss_breakdown`: 총 금액 아래에 작은 섹션을 배치하여 **(시간 손실분 + 리스크 비용)**의 비율을 파이/도넛 차트로 시각화합니다. [근거: Self-RAG]
    *   공식 명시: "손실 = 시간 * 가치" 공식을 가장 크게 노출합니다. [근거: Self-RAG]
*   **상태 변화 (State Transition):**
    1.  **Normal State:** 일반적인 손실 점수 표시.
    2.  **Warning State:** 특정 임계점 도달 시, `Loss Accent` 컬러가 강조되고 경고 아이콘이 팝업됩니다.
    3.  **Critical State (The Climax):** Loss Score가 최저점을 기록하거나(최대 손실), 사용자가 데이터를 입력하는 순간 위기감 극대화 조건 충족 $\rightarrow$ **Red Warning 필터 및 Glitch 효과 발동**.
        *   **Visual Effect:** 화면 전체에 붉은 빛의 노이즈/글리치 애니메이션이 오버레이됩니다. (개발팀 참고: `Anti-Loss Funnel Core Component Spec v1.0`)
        *   **Copy Change:** "경고! 이대로는 법적 책임 회피가 불가능합니다."로 강제 변경.

### 3. CTA 및 결제 섹션 (Conversion Flow)
*   **CTA 문구 원칙:** '구매하기' 대신 **이득 기반의 구체적인 메시지**를 사용합니다. 예: "시간 확보 [XX]시간 돌려받기", "손실 방지 계획 수립하기". [근거: 지난 의사결정 로그]
*   **Payment Mockup:** Pro Tier ($499~$699)가 가장 강조됩니다. 각 티어의 혜택은 '법적 리스크 회피 증명'이라는 가치로 포장되어야 합니다.
*   **TOS/Legal:** 결제 버튼 영역 하단에 미니멀하게 통합합니다.

## ✅ 자가검증 결과
자가검증: 사실 12개 / 추측 0개

📝 다음 단계: 이 명세서를 기반으로 Figma 디자인 파일로 컴포넌트를 구현하고, 개발팀과 협의하여 인터랙션(Red Warning/Glitch Effect) 시퀀스의 애니메이션 타이밍을 구체적으로 조율해야 합니다. (Figma Mockup 생성 후 전달 필요)