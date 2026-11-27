# 최종 인터랙티브 사용자 흐름도 (User Flow Map) - 고고플랙스 Anti-Loss Funnel v1.0

## 🎯 목적 및 활용 범위
*   **목적:** 모든 마케팅 콘텐츠(영상, 랜딩페이지, 광고 등)의 스토리텔링 구조와 시각적 일관성을 확립하는 기준 가이드라인.
*   **핵심 원칙:** 사용자에게 '정량화된 손실'을 느끼게 하여, 오직 고고플랙스의 서비스만이 유일한 해결책임을 각인시킨다.

## 🎨 디자인 시스템 원칙 (Style Guide)
| 요소 | 스타일 정의 | 컬러 코드 | 기능적 역할 및 애니메이션 지침 | [근거: Self-RAG] |
| :--- | :--- | :--- | :--- | :--- |
| **배경** | Pure White / Minimalist Space | `#FFFFFF` | 넓은 여백(Padding/Margin)을 활용하여 고급스러움과 집중도 확보. | Apple-style Minimalist UI/UX Designer Rules |
| **기본 텍스트** | Deep Charcoal (가독성 최우선) | `#1D1D1F` | 모든 본문 및 일반 카피라이팅에 사용. | Apple-style Minimalist UI/UX Designer Rules |
| **Primary Accent** | 신뢰, 해결책, CTA | `#0066CC` | 최종 행동 유도(CTA), 성공적인 정보 전달 영역에 제한적으로 사용. | Self-RAG - Primary Accent |
| **Loss Accent (Danger)** | 리스크, 경고, 손실액 | `#CC3333` | '손실', '위험', 'Warning' 관련 모든 수치 및 섹션 배경으로 사용. 감정적 공포 극대화. | Self-RAG - Loss Accent |
| **애니메이션** | Glitch Effect & Red Warning Filter | N/A | 불안감을 조성할 때(S1 $\rightarrow$ S2 전환 시) 필수로 적용. Opacity 0에서 Fade-In Up 사용 권장. | 지난 의사결정 로그 / Self-RAG - 초기 상태 |

## 🔄 섹션별 상세 플로우 매핑 (The Funnel Flow)

### 🔴 SECTION 1: [HOO K] – 무지(無知)의 위험성 각인 (Awareness)
*   **감정 변화:** 안심 $\rightarrow$ 의아함 $\rightarrow$ 불안감 고조.
*   **시각 연출:** 깨끗한 인터페이스로 시작하여, 3~5초 지점에서 **Glitch Effect 및 Red Warning Filter**가 순간적으로 오버레이되며 강제적으로 시청자의 주의를 붙잡는다.
*   **주요 메시지:** "당신이 놓치고 있는 법적/재정적 리스크가 있습니다."

### 🟡 SECTION 2: [CLIMAX] – 손실 정량화 경험 및 공포 극대화 (Shock & Quantification)
*   **감정 변화:** 불안감 $\rightarrow$ 충격 $\rightarrow$ 위기 인식.
*   **핵심 인터랙티브 컴포넌트:** **Loss Scorecard Widget** (페이지 중앙 최우선 노출).
    1.  **계산 원리 시각화:** `[손실 = 시간 손실분(T) + 리스크 비용(R)]` 공식을 가장 크게, 눈에 띄게 제시한다. 이 수치가 실시간으로 계산되는 애니메이션을 통해 투명성을 확보해야 한다.
    2.  **시각적 충격:** 위젯의 모든 요소는 **Red Warning Filter**가 적용되어야 하며, 점수가 변할 때마다 경고음(SFX)과 함께 강렬하게 시각화된다.
    3.  **분해 구조 (Loss Breakdown):** 최종 손실액 아래에 작은 차트를 배치하여 $T$와 $R$의 비율을 명확히 분리 보여준다.

### 🔵 SECTION 3: [CTA] – 해결책 제시 및 행동 유도 (Action)
*   **감정 변화:** 공포 $\rightarrow$ 안도/해결 가능성 인지 $\rightarrow$ 즉각적 행동.
*   **시각 연출:** 강렬한 Red Warning 필터가 사라지고, Blue Accent 컬러를 사용하여 깨끗하고 신뢰감 있는 섹션으로 전환된다.
*   **최종 CTA 버튼 명세 (MUST FOLLOW):**
    *   ❌ 금지 문구: "구매하기", "신청하기"
    *   ✅ 필수 문구 예시: **"시간 확보 [XX]시간 돌려받기", "손실 방지 계획 수립 및 보고서 요청"**. (이득 기반의 구체적인 메시지)