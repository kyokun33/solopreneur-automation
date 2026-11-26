# 📄 Landing Page Sales Copyflow (Anti-Loss Funnel)

> **Design Reference:** `Designer.md` (Mobile 4:5 Ratio, Minimalist UI)  
> **Core Logic:** Loss Aversion ($55/hr Opportunity Cost)  
> **Brand Tone:** 친근함 + Urgent Protection

---

## 1. Hero Section: 손실의 시작점 (The Hook)
**[UI Element]** `H1 Headline` (Inter Bold, Deep Charcoal)
- **Text:** "혹시 지금도 시간당 $55 를 잃고 계신가요?"
**[UI Element]** `Sub-headline` (Light Gray, 16px)
- **Text:** "오늘 하루가 끝날 때쯤이면, 보이지 않는 손실은 이미 당신의 자산에서 사라져버립니다."
**[UI Element]** `Loss Counter Widget` (Warning Red Background, Pulse Animation)
- **Text:** `(Live Risk: $0.00 → $55/hr)`  
  *Copy Logic:* 페이지 로드 시 숫자가 실시간으로 올라가는 애니메이션을 적용하여 "지금도 손실이 발생하고 있다"는 느낌을 즉시 줍니다.
**[UI Element]** `Primary CTA Button` (Tech Blue)
- **Text:** "손실 멈추기 - 지금 바로 시작하기"

---

## 2. Problem Section: 손실의 실체 (Problem Amplification)
**[UI Element]** `Section Title`
- **Text:** "당신이 모르는 시간의 비용, $55 의 함정"
**[UI Element]** `Card 1: Inflation vs Loss` (Icon: Downward Trend Arrow)
- **Title:** "인플레이션은 당신을 부자가 만든다? 아니요."
- **Body:** "물가는 오르고 있는데, 당신의 시간은 정액으로 사라집니다. 시급 $55 를 생각해보세요. 한 커피 값, 한 번의 지하철 요금, 혹은 한 시간의 휴식보다 더 빠르게 당신의 자산이 줄어듭니다."
**[UI Element]** `Card 2: Risk Cost` (Icon: Shield Crack)
- **Title:** "방관하는 비용은 $55 보다 훨씬 큽니다."
- **Body:** "수동 업무로 인한 기회비용은 단순 시급보다 높습니다. 밤새워 일해도, 자동화가 만들어주는 시간만큼의 가치가 더 큰데, 지금 그것을 놓치고 계십니다."
**[UI Element]** `Risk Calculator Input` (Interactive Form)
- **Label:** "당신의 오늘이 몇 시간 남았나요?"
- **Logic:** 사용자는 자신의 남은 시간을 입력하고, 시스템은 `$55 × 시간 = 누적 손실액`을 계산하여 보여줍니다.

---

## 3. Solution Section: 고고플랙스 솔루션 (Solution Presentation)
**[UI Element]** `Section Title`
- **Text:** "손실을 막아내는 가장 빠른 길"
**[UI Element]** `Feature Highlight 1: Automation` (Icon: Robot Arm)
- **Title:** "수동 노동을 자동화로 대체하세요."
- **Body:** "고고플랙스는 당신의 수고를 대신합니다. 지금 당장 멈출 수 있는 손실을 AI 로 차단하고, 그 시간을 더 가치 있는 일로 채웁니다."
**[UI Element]** `Feature Highlight 2: Security` (Icon: Vault)
- **Title:** "자산 보호 방어선"
- **Body:** "경제 불안, 인플레이션, 기회비용. 세 가지 위험 요소를 AI 로 방어합니다. 손실을 회피하는 것이 곧 최고의 수익입니다."
**[UI Element]** `Social Proof/Trust` (Icon: 5 Stars)
- **Title:** "이미 선택한 1 만명의 신뢰"
- **Body:** "수익성을 추구하는 1 인 기업가들의 선택. 당신의 시간과 자산을 보호합니다."

---

## 4. Pricing Section: 손실 회피 티어 (Tiered Paywall Triggers)
**[UI Element]** `Pricing Header`
- **Text:** "손실을 멈추는 비용, 투자보다 훨씬 저렴합니다"
**[UI Element]** `Tier 1: Starter ($97)` (Low-Medium Contrast)
- **Title:** "손실 방지 기본형"
- **Sub-title:** "단순 자동화 기능으로 손실 속도 저감"
- **Pain Point Link:** "시간당 $55 를 조금이라도 늦추고 싶다면?"
- **CTA:** "시작하기 ($97)"
**[UI Element]** `Tier 2: Growth ($197)` (Primary Contrast, Suggested)
- **Title:** "손실 회피 최적형"
- **Sub-title:** "핵심 모듈 해금으로 손실 완전 차단"
- **Pain Point Link:** "단순히 멈추는 것이 아니라, 기회를 잡으려면?"
- **CTA:** "회비 시작하기 ($197)"
**[UI Element]** `Tier 3: Enterprise ($497)` (High Contrast, Premium)
- **Title:** "자산 보호 최상급"
- **Sub-title:** "엔터프라이즈 솔루션으로 기회비용 극대화"
- **Pain Point Link:** "지금의 손실을 미래의 자산으로 바꾸려면?"
- **CTA:** "최대 투자하기 ($497)"
**[Paywall Trigger Logic]**
- 사용자가 하단으로 스크롤하면, Tier 1 은 기본 정보만 노출. Tier 2 는 `Unlock` 버튼 클릭 시 추가 기능 (예: '실시간 리스크 감지')이 애니메이션으로 풀림. Tier 3 은 '자산 보호' 관련 데이터 (예: '월간 예상 손실 절감 $5,000+') 가 숨겨져 있어 클릭 시 드러남.

---

## 5. Footer Section: 최종 행동 유도 (Final CTA)
**[UI Element]** `Footer Background` (Light Gray)
- **Text:** "지금 바로 손실을 멈출까요?"
**[UI Element]** `Final CTA Button` (Tech Blue, Full Width)
- **Text:** "손실 회피하기 ($55/시간)"
**[Risk Warning]** (Small Text below button)
- **Text:** "기회비용 계산: $55 × 시간 = 당신의 자산 감소. 지금 행동하지 않으면 더 큰 비용이 발생할 수 있습니다."
**[UI Element]** `Copyright & Trust`
- **Text:** © 2026 GogoFlex. 모든 콘텐츠는 수익성 추구 1 인 기업가 위한 것입니다.