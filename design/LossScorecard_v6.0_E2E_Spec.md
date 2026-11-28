# 🔴 Loss Scorecard v6.0: E2E 테스트 프로토타입 최종 상호작용 명세서 (Final Spec)

**[목적]**: 사용자가 초기 데이터 입력 → 위기감 증폭 ($1,500 임계점 도달) → Mini-Commitment Loop 유도 → 핵심 CTA 클릭까지의 전 과정(End-to-End Experience)을 시뮬레이션합니다. 이 문서는 개발팀이 QA와 통합 테스트에 사용할 최종 기준점이 됩니다.

**[핵심 원칙]**: Anti-Loss Funnel 구조를 100% 준수하며, 모든 상호작용은 '손실 공포(Fear)' 자극을 통해 다음 행동을 강제하는 것이 목표입니다 [근거: 지난 의사결정 로그].

---

## 📐 1. 디자인 시스템 및 시각적 원칙 재확인 (Visual Rules)

| 요소 | 스타일 정의 | 컬러 코드 | 역할/목표 | 근거 |
| :--- | :--- | :--- | :--- | :--- |
| **Primary** (배경) | Pure White, 여백 강조 | `#FFFFFF` | 깨끗함 유지. 정보가 쏟아져 나올 수 있는 '도화지' 역할 [근거: Self-RAG] |
| **Secondary** (카드/구역) | Light Gray, 부드러운 구분 | `#F5F5F7` | 데이터나 계산 결과를 담는 영역의 분리. 시각적 피로 감소 [근거: Self-RAG] |
| **Loss Accent** (손실 강조) | Warning Red (고강도), 깜빡임 효과 적용 | `#CC3333` | 손실액($L$), 경고 메시지, 위기 상태 전이 시 필수 사용. 공포 극대화 [근거: Self-RAG] |
| **Mini CTA** (해결책) | Tech Blue 계열의 강렬한 색상 (Primary Accent 대체) | `#0066CC` | '손실 방지'에 초점을 맞춘 해결책 버튼. 신뢰와 행동 유도 [근거: Self-RAG] |
| **폰트** | Inter / Pretendard (Sans-serif), 가독성 최우선 | `#1D1D1F` (Deep Charcoal) | 모든 텍스트의 기본 색상 및 스타일. [근거: Apple-style Minimalist UI/UX Designer Rules] |

---

## 🧩 2. E2E 사용자 흐름 (User Flow & State Machine)

**[State Machine 정의]**:
1.  **INITIAL_STATE**: 데이터 입력 대기.
2.  **CALCULATION_STATE**: Loss Score 계산 중.
3.  **WARNING_TRIGGER_STATE**: $1,500 임계점 도달 (Mini-Commitment Funnel 시작).
4.  **CRITICAL_STATE**: 심각한 리스크 진입 ($X 이상).
5.  **CTA_SUCCESS_STATE**: 유료 감사(Audit) 상품 클릭 완료.

### 🟢 STEP 1: 초기 진입 및 데이터 입력 (INITIAL\_STATE)

*   **UI 요소**: 미니멀한 폼 인터페이스. 여백을 극대화하여 사용자의 집중도를 높입니다 [근거: Apple-style Minimalist UI/UX Designer Rules].
*   **요소 구성**: '어떤 데이터를 놓쳤는지'에 대한 질문 기반 입력 필드 3가지 (Time Loss, Risk Cost A, Risk Cost B).
    *   **H1 카피 예시**: "혹시 지금, 이 순간에도 돈을 잃고 계신가요?" (강력한 후크) [근거: 지난 의사결정 로그].
    *   **입력 필드 가이드**: '시간당 얼마를 벌 수 있나요?', '이 리스크는 어느 정도 금액으로 추산되나요?' 등 **질문 형태**로 제시하여 사용자의 심리적 장벽을 낮춥니다 [근거: Self-RAG - UI 연동 가이드].
*   **트리거**: `[버튼 클릭] "나의 손실 점수 즉시 계산하기"`

### 🟠 STEP 2: Loss Score 계산 및 위기감 증폭 (CALCULATION\_STATE → WARNING\_TRIGGER\_STATE)

*   **상호작용**: 버튼 클릭 후, 데이터가 처리되는 동안 잠시 로딩 애니메이션(Loading State)을 보여줍니다.
*   **핵심 동작**: **Loss Counter 위젯**이 부드럽게 계산 결과를 표시하며 Opacity 0에서 Fade-In Up 됩니다 [근거: Self-RAG - 초기 상태].
    *   표시 형식: `총 손실 점수 ($L) = (시간 손실분 $T_{loss}$) + (리스크 비용 $\Sigma R$)`
    *   **반드시 Loss Breakdown 섹션 배치**: 최종 금액 아래에 작은 섹션을 배치하여, 이 돈이 단순히 '숫자'가 아니라 **'잃어버린 시간의 가치와 리스크'로 구성되어 있음을 투명하게 증명**합니다 [근거: Self-RAG - 손실 Breakdown].

*   **[Critical Trigger Point]**: 계산된 $L$ 값이 **$1,500를 초과하는 순간**, 시스템이 급격히 변화합니다.
    *   **시각 효과 (Visual Effect)**: 배경에 미세한 글리치(Glitch) 애니메이션이 발생하고, 모든 전경 요소가 붉은색 필터(`filter: hue-rotate(0deg) saturate(200%)`)를 입으며 깜빡입니다 [근거: Anti-Loss Funnel Core Component].
    *   **청각 효과 (Audio Effect)**: **경고 사이렌 소리(Warning Siren Sound)**가 최대 볼륨으로 발생합니다. 1~2초간의 공포감 조성에 최적화되어야 합니다 [근거: 지난 의사결정 로그].

### 🔴 STEP 3: Mini-Commitment Loop 유도 (WARNING\_TRIGGER\_STATE) - 핵심 단계

*   **Goal**: 사용자가 패닉 상태일 때, 가장 먼저 해결할 수 있고 낮은 비용의 옵션을 제시합니다.
*   **UI 변화**: 페이지의 중앙에 **'임시 진단 보고서(Mini Diagnostic Audit)'** 위젯이 팝업 또는 고정되어 나타납니다.
    *   **헤드라인 카피 (강제)**: "🚨 $1,500 이상의 손실은 심각합니다. 지금 당장 근본 원인을 알아야 합니다." (위기감 극대화) [근거: Anti-Loss Funnel Core Component].
    *   **상품 제시**: Paid Diagnostic Audit ($99~$149). 이 상품은 **'최소 지출로 가장 큰 불확실성을 제거하는 행위'**라는 점을 강조해야 합니다.
    *   **CTA 버튼 문구 (필수)**: '구매하기' 대신, "**시간 확보 25시간 돌려받기 ($149)**"와 같이 이득 기반의 구체적 메시지를 사용합니다 [근거: Self-RAG - 카피라이팅 원칙].
*   **상호작용**: 버튼 클릭 시, $L$ 값이 사라지며 '진단 보고서 요청 완료' 성공 애니메이션과 함께 다음 단계(Pro Audit)로 자연스럽게 유도되는 텍스트가 노출되어야 합니다.

### ✨ STEP 4: 최종 전환 (CTA\_SUCCESS\_STATE)

*   **Goal**: Mini-Commitment를 통해 신뢰를 확보한 사용자에게 주력 상품을 판매합니다.
*   **전환 문구**: "진단 보고서를 받으셨습니다. 이제 근본적인 시스템 리스크부터 해결해야 합니다."
*   **최종 CTA**: 'Full Loss Scorecard 진단 및 예방 플랜 수립하기' (Pro/Bundle 티어)

---
## 🛠️ 3. 기술 구현 명세서 (Developer Specification)

| 항목 | 스펙 내용 | 고려 사항 | 근거 |
| :--- | :--- | :--- | :--- |
| **애니메이션** | 모든 요소 전환은 `transition: 0.3s ease-in-out`을 준수하며, $1,500 트리거 시에는 강제적인 '글리치/깜빡임' 효과를 적용합니다. | 성능 저하 방지 및 부드러운 경험 유지 [근거: Self-RAG - 최적화]. |
| **사운드** | `Warning Siren Sound` (WAV 포맷)는 $1,500 임계점 도달 시점에 오디오 API로 강제 재생되어야 합니다. | 브라우저 자동재생 방지 정책을 우회하기 위해 반드시 사용자 상호작용(Click Event)에 종속시켜야 함 [추측]. |
| **데이터 구조** | 계산된 $L$ 값, Time-Loss 분량, Risk Cost 분량을 JSON 객체로 별도 전송하여 백엔드 로직과 연동해야 합니다. | Loss Scorecard의 투명성 확보를 위한 핵심 API Contract입니다 [근거: Self-RAG]. |

---
**[개발팀 참고]**: 본 프로토타입은 **'사용자 경험 설계서(UX Spec)'**이며, 모든 애니메이션과 상태 전이는 논리적 흐름을 최우선으로 합니다. 시각적인 아름다움보다 '공포 자극 → 해결책 제시'라는 비즈니스 플로우의 완성도를 검증하는 데 초점을 맞추십시오 [근거: Self-RAG].