# 💻 Loss Scorecard v2.0 시스템 통합 설계 명세서: 상태 전이 로직 중심

## 🎯 목표
Loss Scorecard가 단순한 정적 점수(Static Score)가 아닌, 사용자의 '리스크 인지 과정'을 추적하는 **상태 전이 기록 장치**로 작동하도록 백엔드 아키텍처를 정의합니다. 이는 트래픽 확보부터 최종 구매 전환까지의 모든 단계를 데이터베이스에 저장하고 API로 노출시키는 것을 목표로 합니다.

## 🧱 1. 데이터베이스 스키마 설계 (State Transition Tracking)
(사용: PostgreSQL, ORM: SQLAlchemy 기준)

**핵심 개념:** 사용자가 진단하는 행위 자체가 '상태 변화'이며, 이 상태를 추적해야 합니다. `DiagnosisSession` 테이블이 핵심입니다.

### 📂 Table Definitions

```python
# loss_scorecard_v2.0 스키마 정의 (SQLAlchemy Pseudo-Code)

class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

class DiagnosisSession(Base):
    """사용자의 리스크 진단 세션 전체를 기록합니다."""
    __tablename__ = 'diagnosis_sessions'
    session_id: Mapped[UUID] = Column(UUID, primary_key=True) # 고유한 세션 ID 사용 권장
    user_id: Mapped[int] = Column(ForeignKey('users.user_id'))
    start_time: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    end_time: Mapped[Optional[datetime]] = Column(DateTime)
    initial_risk_score: Mapped[float] = Column(Float) # S1 (Initial Score)
    final_state: Mapped[str] = Column(String) # 최종 상태 ('Mitigated', 'HighRisk', 'Unresolved')

class StateTransition(Base):
    """사용자의 리스크 인지 과정에서 발생하는 각 단계별 변화를 기록합니다."""
    __tablename__ = 'score_state_transitions'
    transition_id: Mapped[int] = Column(Integer, primary_key=True)
    session_id: Mapped[UUID] = Column(ForeignKey('diagnosis_sessions.session_id'), nullable=False)
    step_name: Mapped[str] = Column(String) # 예: 'Initial Diagnosis', 'Feature Review (AI Gap)', 'Pricing Inquiry'
    timestamp: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    input_data: Mapped[JSON] = Column(JSON) # 사용자가 입력한 데이터 스냅샷 (업종, 규모 등)
    score_delta: Mapped[float] = Column(Float) # 이 단계에서 변화한 점수 값 (Delta Score)
    new_risk_level: Mapped[str] = Column(String) # 새로운 리스크 레벨 ('High', 'Medium', 'Low')
    action_taken: Mapped[Optional[str]] = Column(String) # 사용자가 취한 액션 (버튼 클릭, 페이지 이동 등)

# 인덱스 최적화 필수 구간
Index('idx_session_user', DiagnosisSession.user_id, DiagnosisSession.session_id)
```

## 🔌 2. API 명세서 초안 (RESTful Endpoints & Protocol)
(사용: OpenAPI/Swagger Style JSON Schema 권장)

### A. Endpoint Structure

| Method | Path | Description | State Transition Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v2/loss/initiate` | **진단 시작.** 새로운 세션을 생성하고 초기 점수를 반환합니다. (S1) | **[Start]** 진입점. 최초의 리스크 상태를 정의. |
| `PUT` | `/api/v2/loss/{session_id}/update_state` | **상태 전이 업데이트.** 사용자가 특정 단계(예: 가격 페이지, 기능 설명서)에 도달할 때마다 호출하여 점수 변화와 이벤트를 기록합니다. (S1 $\to$ S2) | **[Transition]** 가장 중요한 엔드포인트. `StateTransition` 레코드를 생성/업데이트 합니다. |
| `GET` | `/api/v2/loss/{session_id}/history` | 세션 ID를 기반으로 전체 상태 전이 기록 목록을 조회합니다. (디버깅 및 분석용) | **[Read]** 데이터 무결성 검증 및 대시보드 구현에 활용. |
| `POST` | `/api/v2/loss/{session_id}/finalize` | **세션 종료 및 확정.** 최종 구매 또는 이탈을 기록하고 세션을 마감합니다. (S_final) | **[End]** 최종 리스크 상태와 사용자 행동을 저장합니다. |

### B. Payload Example: `PUT /api/v2/loss/{session_id}/update_state`
(이 엔드포인트는 프론트엔드가 가장 자주 사용하게 됩니다.)

```json
{
  "sessionId": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",
  "stepName": "Pricing_Tier_Review", 
  "timestamp": "2026-11-28T10:00:00Z",
  "inputData": {
    "userType": "Corporate",
    "industry": "Finance",
    "dataVolumeEstimate": "5TB+"
  },
  "scoreDelta": 7.5, // 이전 상태 대비 점수 변화 폭 (양수/음수)
  "newRiskLevel": "High_Urgency", // 이 단계에서 인식된 새로운 리스크 레벨
  "actionTaken": "Clicked CTA: Pro Plan Details" // 사용자가 취한 구체적 액션
}
```

## ✅ 3. 통합 테스트 케이스 목록 (10가지)
(테스트 목표: 시스템의 안정성과 비즈니스 로직 검증)

| No. | Test Case ID | 테스트 목적 | Pre-Condition (선행 조건) | Expected Result (예상 결과) | Failure Scenario Check |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `TC_001` | **최초 세션 생성 성공** | 유효한 User ID, 초기 입력 데이터 존재. | `POST /initiate` 호출 시, DB에 `DiagnosisSession`이 정상적으로 레코드되고 최초의 기본 점수가 반환되어야 함. (HTTP 201) | Input Data 누락 시 에러 코드 확인. |
| 2 | `TC_002` | **점수 전이 성공(Positive Delta)** | 초기 세션 존재, 사용자가 'AI Gap' 섹션을 탐색 완료함. | `PUT /update_state` 호출 시, 이전 점수 대비 합리적인 증가(`scoreDelta > 0`)가 반영되고 새로운 리스크 레벨이 확정되어야 함. (HTTP 200) | Delta Score 범위 초과 입력 시 가드 처리 확인. |
| 3 | `TC_003` | **점수 전이 성공(Negative Delta)** | 초기 세션 존재, 사용자가 '면책 조항'을 상세히 검토하여 리스크 인지도가 낮아짐. | 점수가 하락(`scoreDelta < 0`)하고, 새로운 레벨이 'Medium'으로 업데이트되어야 함. (HTTP 200) | 마이너스 점수 입력 제한 및 예외 처리 확인. |
| 4 | `TC_004` | **데이터 유효성 검증(Validation)** | 세션 ID가 존재하지 않는 경우. | API는 즉시 에러 응답을 반환하며, 404 Not Found 코드를 사용해야 함. (HTTP 404) | 잘못된 JSON 스키마를 보낼 때의 파싱 오류 처리 확인. |
| 5 | `TC_005` | **동시성 제어(Concurrency)** | 두 개의 클라이언트가 동시에 같은 세션 ID에 대해 상태 업데이트 요청을 보냄. | DB 레벨에서 마지막으로 기록된 점수만 반영되도록 낙관적 잠금(Optimistic Locking) 또는 트랜잭션 격리가 작동해야 함. (최종 점수가 일관성 유지 확인). |
| 6 | `TC_006` | **필수 필드 누락** | 상태 업데이트 요청 시, `stepName`이나 `scoreDelta` 중 하나가 누락됨. | 서버는 명확한 에러 메시지("Missing required field: stepName")와 함께 HTTP 422 Unprocessable Entity를 반환해야 함. (HTTP 422) |
| 7 | `TC_007` | **세션 종료 로직** | 모든 상태 전이가 완료되고 사용자가 구매 버튼을 누름. | `POST /finalize` 호출 시, 최종 점수와 '구매' 플래그가 기록되고 해당 세션의 상태가 영구적으로 마감되어야 함. (HTTP 200) |
| 8 | `TC_008` | **대량 데이터 조회 성능** | 특정 사용자(user\_id=1)가 수백 개의 세션을 생성하고 업데이트한 경우. | `/history` 호출 시, DB 인덱스를 통해 지연 없이 (Latency < 50ms) 모든 기록을 반환해야 함. |
| 9 | `TC_009` | **권한 제어(Authorization)** | 로그인하지 않은 사용자(Guest User)가 세션 업데이트를 시도함. | API는 즉시 인증 실패 응답(HTTP 401 Unauthorized)을 반환하며, 회원가입 유도를 하거나 강제 이탈시켜야 함. (HTTP 401) |
| 10 | `TC_010` | **비즈니스 로직 검증** | 점수 변화율이 너무 급격하게(예: -50점/초) 발생하는 비정상적 이벤트가 감지됨. | 백엔드에서 해당 데이터를 거부하고 (HTTP 429 Too Many Requests 또는 Custom Error), 경고 로그를 남겨야 함. |

---