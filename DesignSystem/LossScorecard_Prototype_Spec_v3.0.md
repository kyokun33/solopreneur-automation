# 🔴 Loss Scorecard 인터랙티브 컴포넌트 스펙 (v3.0) - Prototype Wireframe

**[목적]**: 사용자가 웹사이트에 진입했을 때, 가장 먼저 마주하는 '위기감 증폭' 섹션의 프로토타입 와이어프레임 및 개발 명세서입니다. 단순한 계산 결과를 보여주는 것이 아니라, **"어떤 근거로 이 손실이 발생했는지"**를 투명하게 증명하여 신뢰도를 확보하고 다음 행동(CTA)으로 유도하는 것이 핵심 목표입니다.

**[전제 조건]**:
1.  API 응답 데이터는 코다리 에이전트가 정의한 `LossCalculatorService`의 최종 JSON 구조(`total_loss`, `calculation_breakdown`)를 따릅니다.
2.  모든 시각 효과(Red Warning, Glitch)는 CSS 및 JavaScript로 제어되는 인터랙티브 요소입니다.

---

## 📐 1. 컴포넌트 개요 및 레이아웃 (The Hero Section)

**[구조]**: Full-width 섹션으로 배치하며, 페이지 로드 시 애니메이션을 통해 강력하게 등장해야 합니다.
**[배경/톤]**: `#FFFFFF` (Primary Background). 위기감 조성 단계이므로, 배경에 아주 은은한 노이즈 필터(Noise Overlay)를 추가하여 긴장감을 유지합니다.

### 📌 A. 헤더 및 후크 (Anti-Loss Hook)
*   **요소:** H1 태그. 가장 큰 폰트 크기 사용 (`font-size: 4rem;`).
*   **카피**: "당신이 무심코 흘린 시간, 예상 손실액은 \[TOTAL LOSS]원 입니다." (Writer Copy 활용)
*   **스타일링:** `[근거: 지난 의사결정 로그]`에 따라, '손실' 키워드는 **Warning Red (`#CC3333`)**으로 강조됩니다.

### 📌 B. 핵심 위젯: Loss Counter (최우선 노출)
*   **위치**: 페이지 중앙, H1 바로 아래. 가장 시각적 무게감이 높아야 합니다.
*   **데이터 바인딩**: `total_loss` 값을 실시간으로 표시합니다.
*   **[🔥 인터랙션]**: 위젯은 초기 Opacity 0에서 시작하며, 스크롤 또는 로드 후 **카운트업 애니메이션(Counter-Up Animation)**이 적용되어야 합니다.
    ```css
    /* CSS Spec */
    .loss-counter {
        font-size: 6rem; /* 최대 크기 */
        color: #CC3333; /* Warning Red */
        transition: opacity 1s ease-out, transform 0.5s ease-out;
    }
    /* JS Trigger */
    @media (initial-view) {
       .loss-counter { animation: countUp(2s); }
    }
    ```

---

## 🔬 2. Loss Breakdown 섹션 (신뢰 구축 단계)

이 섹션은 '왜 이 점수가 나왔는지'를 시각적으로 증명하는 Heart of the Funnel입니다. 코다리의 `calculation_breakdown` 데이터를 사용합니다.

**[컨셉]**: 손실의 원인을 3개의 독립적이고 명확한 카드(Card) 형태로 제시하며, 각 카드는 Red Warning 필터와 Tech Blue 강조를 혼합하여 보여줍니다.
**[레이아웃]**: 3열 그리드(`display: grid; grid-template-columns: repeat(3, 1fr);`).

### ✨ Breakdown Card (개별 요소 스펙)
*   **제목 (Category)**: 예) "시간 손실분", "지식 리스크 비용".
*   **핵심 수치**: 해당 항목의 점수. 이 숫자는 Warning Red로 강조됩니다.
*   **세부 설명/계산 과정**: 가장 중요한 부분. `[근거: Self-RAG - 투명성 확보]`에 따라, **공식 명시**와 **비율 시각화**가 필수입니다.

<!-- HTML 구조 예시 (Card 1) -->
<div class="breakdown-card red-warning-border">
    <h3>⏰ 시간 손실분 (Time Loss)</h3>
    <p class="loss-value">$2,750</p> <!-- Warning Red Text -->
    <div class="formula-box">
        <strong>손실 = 시간 × 가치</strong> <span class="calc-detail">(25시간 * $110/시간)</span>
    </div>
    <!-- 시각적 증명: Donut Chart 또는 Bar Graph 사용 -->
    <div class="loss-ratio-chart">[Donut Chart Placeholder] </div>
</div>
```

*   **[🔥 인터랙션]**: 각 카드는 마우스를 올리면(Hover) **Glitch 효과와 함께 상세 계산 과정이 Pop-up**으로 펼쳐지거나, 전체 섹션에 Tech Blue의 미세한 빛 번짐(`glow`) 애니메이션을 적용하여 시선 집중도를 높입니다.

---

## 🚀 3. CTA 및 결론 (Action Funnel)

위기감을 최고조로 끌어올린 후, 명확하고 이득 기반의 행동 유도(CTA)를 제시합니다.
**[카피 원칙]**: '구매하기' X → **'손실 방지 계획 수립하기'** O (`[근거: Self-RAG - 카피라이팅 원칙]`)

<button class="cta-button tech-blue">
    시간 확보 25시간 돌려받고, 손실을 막으세요.
</button>
```

### [디자인 시스템 토큰 요약]
*   **Primary Color (Trust)**: Tech Blue (`#0066CC`) - CTA 및 성공 메시지.
*   **Loss Accent (Fear)**: Warning Red (`#CC3333`) - 손실 금액, 경고 영역.
*   **Background**: Pure White (`#FFFFFF`).

***