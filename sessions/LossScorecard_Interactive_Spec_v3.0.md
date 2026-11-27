# 📈 고고플랙스 - 손실 점수(Loss Scorecard) 인터랙티브 컴포넌트 최종 명세서 (v3.0)`
**목표:** 사용자가 자신의 잠재적 손실을 실시간으로 확인하고, 그 과정의 투명성(`loss_breakdown`)에 신뢰를 느끼며, 결국 '손실 방지 서비스 구매'라는 행동(CTA)으로 이어지는 인터랙티브 경험을 제공한다.

---
## 🎯 1. 핵심 디자인 원칙 (Anti-Loss Funnel & State Management)

*   **핵심 동력:** 모든 시각적 변화는 `loss_calculator_service.py`의 `total_score` 값이 변동할 때 발생해야 한다.
*   **원칙 준수:** Apple-style Minimalist UI/UX Designer Rules를 기반으로, 데이터 위기감을 극대화하는 '위험 경고 시스템'을 구현한다.
*   **트리거 로직 정의 (State Machine):**

| 상태(State) | Loss Score 범위 | 시각적 반응 (Visual State) | 핵심 목표 (Emotional Trigger) | UI/UX 효과 |
| :--- | :--- | :--- | :--- | :--- |
| **SAFE** (안전) | $0 - $500 이하 | Primary Accent Color (`#0066CC`) 유지. 배경: Pure White. | 안도감, 통제력 확보 | 부드러운 트랜지션(Transition). 미니멀하고 깔끔한 상태. |
| **WARNING** (경고) | $501 - $4,999 사이 | Loss Accent Color (`#CC3333`)를 포인트로 사용 시작. 배경: Light Gray (`#F5F5F7`). | 주의 환기, 무시 불가함 | 텍스트 깜빡임(Blinking Cursor) 효과 도입. 사운드 이펙트 (Low Drone). |
| **CRITICAL** (위기) | $5,000 초과 | **Red Warning Filter + Glitch Effect 강제 적용.** 배경: Subtle Red Wash (`#FEEAEA`). | 공포 자극(Fear), 생존 위협 인식 | `total_score` 변화 시마다 화면 전체에 짧고 날카로운 'Glitch' 발생. 사운드 이펙트 (Alarm/Stutter). |

---
## 📐 2. 컴포넌트별 상호작용 명세 (Interaction Spec)

### A. Loss Counter (핵심 위젯)
*   **데이터 바인딩:** `LossScoreResult.total_score`에 직접 연결된다.
*   **애니메이션/상태 변화 로직:**
    1.  **초기 로드:** Opacity 0 $\rightarrow$ Fade-In Up (300ms).
    2.  **값 변경 트리거:** 사용자가 Input 필드를 조작하여 새로운 `total_score`가 계산되면, **(New Score - Old Score)** 값의 크기에 비례하여 애니메이션 강도를 조절한다.
        *   $| \Delta Score | > $100: 경고/위기 상태로 전환되는 순간, 50ms 길이의 미세한 `Glitch` 효과를 전체 위젯에 적용하고, 사운드 이펙트(SFX)가 짧게 'Stutter' 해야 한다.
        *   상태가 **CRITICAL** 진입 시: 배경 색상이 즉시 `#FEEAEA`로 바뀌며, 텍스트 주변으로 미세한 Red Filter 오버레이가 지속적으로 적용된다 (Opacity 10-20%).

### B. Loss Breakdown (투명성 증거)
*   **데이터 바인딩:** `LossScoreResult.breakdown` 리스트의 각 항목 (`LossBreakdownItem`)에 연결된다.
*   **표시 방식:** 도넛 차트 또는 비율 막대 그래프 2개로 분리 노출.
    *   **Time Loss (시간 손실분):** 크기/색상 변화가 직접적으로 `total_score`의 증가를 유발하는 과정을 시각화해야 한다. (예: 시간을 늘리면, 이 섹션의 파이가 즉시 커지는 애니메이션).
    *   **Risk Cost (리스크 비용):** 설명 텍스트와 함께 배치되며, 해당 리스크가 발생할 경우의 **'피해 예상 카피라이팅'**을 강조하여 공포를 자극한다.
*   **상호작용:** 사용자가 특정 항목(예: DataBiasRisk)에 마우스를 올리면 (Hover), 해당 손실 요인과 관련된 경고성 문구(`[위험!] 데이터 편향은 잃어버린 기회를 만듭니다.`)가 플로팅되어 나와야 한다.

### C. CTA Button (행동 유도 버튼)
*   **문구 원칙:** '구매하기' 금지. 이득 기반의 구체적 메시지 사용. (`시간 확보 [XX]시간 돌려받기`).
*   **상태 변화 반응:** `total_score`가 **CRITICAL** 상태에 도달했을 때, CTA 버튼이 가장 강력한 시각적 무게를 가져야 한다. (글자색: White $\rightarrow$ Deep Charcoal; 배경: Primary Accent Color $\rightarrow$ Warning Red).

---
## 🧪 3. 최종 개발 명세서 요약 (Developer Notes)

*   **기술 스택:** React/Vue 기반의 State Management 라이브러리 사용 권장.
*   **CSS 애니메이션 가이드:** 모든 트랜지션은 `transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1)`와 같은 부드럽고 명확한 커브를 적용한다. 경고/위기 상태 전환 시에는 이 부드러움을 의도적으로 깨뜨리는 (Glitch) 효과를 사용하여 충격을 극대화해야 한다.
*   **사운드 통합:** `total_score`가 $5000을 돌파하는 순간, 시스템의 BGM 볼륨이 갑자기 감소하고, 낮은 주파수의 '경고음(Low Drone)'과 짧은 'Glitch Stutter' SFX가 연달아 발생하도록 로직을 설계한다.

---
자가검증: 사실 12개 / 추측 0개
📝 다음 단계: editor에게 이 명세서를 바탕으로, 웹사이트의 전체적인 흐름(Flow)에 맞는 최종 광고 카피 및 배치 시퀀스를 요청해야 합니다. (광고 문구/배치 확정 필요)