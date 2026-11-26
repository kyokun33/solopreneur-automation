# 📊 Anti-Loss Funnel 단기 KPI 명세서 (v1.0)

**작성일:** 2026. 9. 1. 오후 22:35  
**작성자:** 현빈 (비즈니스 전략가 · Head of Business)  
**수신:** 코다리 (개발팀), Designer, Researcher  
**상태:** 공유용 명세서

---

## 🎯 배경 및 목적
Anti-Loss Funnel은 사용자가 손실액 ($L$) 을 계산하고 해결책을 제시하여 전환하는 핵심 플로우입니다. 개발팀이 UI 컴포넌트 라이브러리를 구축하고 통합 테스트를 진행 중이므로, 성공적인 페이지 운영을 위한 **단기 KPI 3 가지**를 정의합니다.

---

## 📉 단기 KPI 3 가지 (1 개월 내)

### 1️⃣ KPI: 손실액 계산 완료율 (Loss Calculation Completion Rate)
- **정의:** 방문 사용자가 손실액 $L$ 입력 슬라이더를 조작하고 최종 금액을 확인한 비율
- **측정 지표:**
  - `session_count`: 총 세션 수 (Analytic스팀에서 추적)
  - `calculation_completed_sessions`: 손실액 계산이 완료된 세션 수
  - `completion_rate = (calculation_completed_sessions / session_count) * 100`
- **목표 수치:**
  - **초기 목표 (Month 1):** `60%` 이상  
    *(이유: 사용자의 페인 포인트를 명확히 인식하게 하고 계산을 유도해야 함)*
- **실행 계획:**
  - 계산 완료 시 `🎉 손실액 $L$을 확인하세요!` 애니메이션 효과 적용 (Designer)
  - 계산 과정은 `Counter-Up` 애니메이션으로 시각적 재미 부여 (Developer)

---

### 2️⃣ KPI: CTA 클릭률 (Call-to-Action Click-Through Rate, CTR)
- **정의:** 손실액 $L$ 계산 완료 후 사용자가 CTA 버튼 (예: "지금 해결하기", "무료 체험") 을 누른 비율
- **측정 지표:**
  - `calculation_completed_sessions`: 손실액 계산이 완료된 세션 수
  - `cta_clicks`: CTA 버튼 클릭 수
  - `ctr = (cta_clicks / calculation_completed_sessions) * 100`
- **목표 수치:**
  - **초기 목표 (Month 1):** `15%` 이상  
    *(이유: '시간 보호 플랜' 포지셔닝을 통해 사용자의 구매 의지를 자극해야 함)*
- **실행 계획:**
  - CTA 버튼은 `Anti-Loss Funnel UI 컴포넌트 라이브러리`의 핵심 요소로 구현 (Developer)
  - 버튼 텍스트는 `$55/시간 손실 회피` 등 구체적 이득 강조 (Writer)

---

### 3️⃣ KPI: 평균 체류 시간 (Average Time on Page)
- **정의:** 사용자가 Anti-Loss Funnel 페이지에 머문 평균 시간
- **측정 지표:**
  - `page_view_duration`: 페이지 뷰 시점과 이탈 시점의 차이 (Analytic스팀에서 추적)
  - `avg_time = sum(page_view_duration) / session_count`
- **목표 수치:**
  - **초기 목표 (Month 1):** `1 분 30 초` 이상  
    *(이유: 사용자의 페인 포인트를 충분히 인식하고 해결책을 제시하기 위한 최소 시간)*
- **실행 계획:**
  - 계산 과정의 애니메이션 효과로 시각적 몰입도 높임 (Designer)
  - 페이지 로딩 속도 최적화 및 모바일 반응형 디자인 개선 (Developer)

---

## 📌 개발팀 협업 사항

### 🛠️ Developer (코다리)
- **UI 컴포넌트 라이브러리:** 손실액 계산 카운터, 리스크 입력 슬라이더 등 핵심 시각 요소를 구현 (Designer 명서 참조).
- **Analytic스팀 연동:** 각 KPI 측정 지표에 대한 데이터 수집 로직을 Backend 에 구현.
- **테스트 계획:** 통합 테스트 시나리오에 KPI 달성 여부를 포함하여 E2E 테스트 코드 작성.

### 🎨 Designer
- **시각 요소:** 손실액 계산 카운터, CTA 버튼 등의 디자인 명세와 애니메이션 가이드라인을 개발팀과 공유.
- **사용자 경험:** 페이지 로딩 속도와 모바일 반응형 디자인 개선안을 제시.

### 📝 Writer
- **콘텐츠 전략:** CTA 버튼 텍스트 및 페이지 내 메시지 (Hook, Problem, Solution) 를 KPI 달성을 위한 방향으로 최적화.

---

## 📅 진행 일정

| 단계 | 내용 | 담당자 | 완료일 |
|------|------|--------|--------|
| 1 | UI 컴포넌트 라이브러리 구현 | Developer | 2026-09-05 |
| 2 | Analytic스팀 연동 및 데이터 수집 로직 구현 | Developer | 2026-09-08 |
| 3 | 디자인 명세 및 애니메이션 가이드라인 공유 | Designer | 2026-09-03 |
| 4 | 통합 테스트 시나리오에 KPI 달성 포함 | Developer | 2026-09-10 |
| 5 | 콘텐츠 최적화 (CTA, Hook 등) | Writer | 2026-09-07 |

---

**📊 평가: 진행중 — 개발팀과의 협업 및 데이터 수집 로직 구현을 위해 대기 중**  
**📝 다음 단계:** 코다리 개발팀에게 이 명세서를 공유하고, UI 컴포넌트 라이브러리 구현 시작 요청.