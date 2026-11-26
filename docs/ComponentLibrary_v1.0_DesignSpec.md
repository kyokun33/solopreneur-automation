# 고고플랙스 데이터 무결성 컴포넌트 라이브러리 (v1.0) [DESIGN SPEC]
## 🎯 목표 및 원칙
*   **목표:** 사용자가 자신의 '데이터 손실'을 정량적으로 인식하게 하여, 서비스 가입(Solution)으로 유도한다.
*   **톤앤매너:** Apple-style Minimalist + Anti-Loss Funnel (극도의 직관성과 불안감 조성의 결합).
*   **사용 권장 프레임워크:** React / Vue (Props 기반 재사용 필수).

## 📊 공통 디자인 시스템 변수
| 변수명 | 역할 | 컬러 코드 | 적용 범위 | 근거 |
| :--- | :--- | :--- | :--- | :--- |
| `--color-primary` | 핵심 행동 유도 (CTA) | `#0066CC` | 버튼, 성공 메시지 하이라이트 | Self-RAG - Primary Accent |
| `--color-secondary` | 배경/구분선 | `#F5F5F7` | 섹션 배경, 카드 분리용 | Apple Style Rules |
| `--color-danger` | 손실 강조 (Loss) | `#CC3333` | 게이지 경고 영역, 오류 메시지 텍스트 | Self-RAG - Loss Accent |
| `--color-text` | 기본 본문 텍스트 | `#1D1D1F` | 모든 일반 텍스트 | Apple Style Rules |

## ✨ Component 1: 스코어 게이지 위젯 (`<ScoreGauge>`)
### 📝 인터랙션 명세 (Props & Logic)
*   **Props:** `score`: Number (0-100), `unit`: String, `onHover`: Function.
*   **기본 로직:** 점수 변화에 따라 게이지 채움(Arc Progress) 애니메이션 적용.
*   **Anti-Loss 특화 로직:**
    1.  `score <= 50`일 경우: 게이지 바와 컴포넌트 주변에 `rgba(204, 51, 51, 0.1)`의 은은한 '위험 플래시'를 적용한다.
    2.  **데이터 분해 명세:** 위젯 하단에는 반드시 투명성을 확보하기 위해 작은 섹션을 할당하여 **`Loss Breakdown`**을 표시해야 한다. (Time Loss: $X / Risk Cost: $Y).

## ✨ Component 2: 데이터 오류 발생 컴포넌트 (`<SystemFailure>`)
### 📝 인터랙션 명세 (Props & Logic)
*   **Props:** `errorType`: String ('API_TIMEOUT' 등), `message`: String, `isVisible`: Boolean.
*   **발동 조건:** API 요청 실패 또는 데이터 무결성 검증 실패 시 자동 트리거된다.
*   **비주얼 스펙:**
    1.  **오버레이 효과:** 컴포넌트 전체에 `backdrop-filter: blur(2px)`를 적용한 반투명 오버레이(`rgba(0,0,0,0.1)`)를 씌운다.
    2.  **핵심 애니메이션 (Glitch):** 주기적으로 랜덤하게 위치와 방향을 갖는 수평/수직 스캔라인이 빠르게 지나가며 왜곡되는 효과를 적용한다. (`animation: glitch-effect 2s infinite linear`).
    3.  **문구 강조:** 에러 메시지(`message`)는 `color: var(--color-danger)`를 사용하여 강하게 강조하고, 원본 데이터를 대체할 때 반드시 **`[!!DATA LOST!!]`** 마스킹을 적용한다.

---