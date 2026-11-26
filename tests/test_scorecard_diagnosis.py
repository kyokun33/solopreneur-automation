import pytest
from pydantic import ValidationError
from datetime import timedelta
# ⚠️ 주의: 실제 프로젝트 구조를 가정하여 스키마 파일을 임포트합니다.
from src.api.schemas import LossInputData, DiagnosisResult

# ==================================================
# Mock Service Layer (테스트의 핵심 비즈니스 로직)
# 이 함수는 실제로 별도의 서비스 파일(예: diagnosis_service.py)에 존재해야 합니다.
def calculate_diagnosis(data: LossInputData) -> DiagnosisResult:
    """
    LossInputData를 받아 최종 진단 점수와 손실 상세 분석 결과를 계산합니다.
    [근거: Designer가 확정한 스코어카드 로직]
    """
    # 1. 초기 데이터 유효성 체크 (Pydantic이 처리했지만, 여기서 추가 비즈니스 검증)
    if data.user_role not in ["developer", "manager", "executive"]:
        raise ValueError("유효하지 않은 사용자 역할입니다.")

    # 2. 핵심 로직: 시간 손실 계산 (시간당 손실률 $55/hour 적용)
    time_lost = timedelta(days=data.projected_duration_days, hours=data.estimated_hours).total_seconds() / 3600
    time_loss_cost = time_lost * 55.0  # float 타입 유지 필수

    # 3. 핵심 로직: 리스크 지수 계산 (사용자 역할과 프로젝트 크기에 따른 가중치)
    risk_factor = data.complexity_score * (1 + (data.user_role == 'executive') * 0.5) # 임원에게 추가 페널티/위기감 부여 가정

    # 4. 최종 손실 예측액 및 점수 계산
    total_estimated_loss = time_loss_cost + risk_factor * 1000.0 # 리스크 비용 가중치 적용
    
    # ScoreGauge 로직: Loss가 크면 Score는 낮아짐 (예시 공식)
    diagnosis_score = max(0, min(100, 100 - int((total_estimated_loss / 500.0))))

    return DiagnosisResult(
        final_score=float(diagnosis_score),
        estimated_cost=round(total_estimated_loss, 2),
        risk_breakdown={
            "time_loss": round(time_loss_cost, 2),
            "complexity_risk": round(risk_factor * 1000.0, 2)
        },
        is_high_risk=diagnosis_score < 50
    )

# ==================================================
# E2E 테스트 케이스 정의 (Pytest Fixture 사용 권장)

def test_e2e_successful_diagnosis():
    """
    [성공 사례] 모든 입력값이 유효하고, 로직이 정상 작동하여 고위험 진단 결과를 반환하는지 검증합니다.
    """
    # 1. Mock Input Data (실제 사용 시나리오 기반)
    mock_data = LossInputData(
        user_role="executive",
        projected_duration_days=30,  # 30일
        estimated_hours=24 * 7,     # 주당 7일 근무 가정
        complexity_score=8.5         # 높은 복잡도 점수
    )

    # 2. API 호출 및 로직 실행 (E2E 핵심 구간)
    try:
        result = calculate_diagnosis(mock_data)
    except Exception as e:
        pytest.fail(f"진단 계산 중 예상치 못한 오류 발생: {e}")
        return

    # 3. 검증 단계 (Assertion)
    assert isinstance(result, DiagnosisResult)
    # 높은 리스크 시나리오이므로 점수가 낮게 나오고 비용이 높아야 함
    assert result.final_score < 50, "고위험 데이터 입력에도 불구하고 점수가 충분히 높습니다."
    assert result.estimated_cost > 1000.0, "예상 손실액이 기준치(1000)보다 낮게 계산되었습니다."

def test_e2e_low_risk_diagnosis():
    """
    [성공 사례] 입력값이 완벽하고 복잡도가 낮아 안전한 진단 결과를 반환하는지 검증합니다. (이상적인 경우)
    """
    mock_data = LossInputData(
        user_role="manager",
        projected_duration_days=5,   # 짧은 기간
        estimated_hours=16,         # 적절한 시간
        complexity_score=2.0        # 낮은 복잡도 점수
    )

    result = calculate_diagnosis(mock_data)

    # 검증: 점수가 높고 손실액이 낮아야 함
    assert result.final_score >= 85, "낮은 리스크 데이터에도 불구하고 점수가 지나치게 낮습니다."
    assert result.estimated_cost < 300.0, "예상 손실액이 너무 크게 계산되었습니다. (이상적 상황)"

def test_e2e_validation_failure():
    """
    [실패 사례] Pydantic 스키마를 위반하는 데이터를 입력했을 때, 적절한 ValidationError가 발생하는지 검증합니다.
    (이는 가장 중요한 Guardrail 테스트입니다.)
    """
    # 1. 유효하지 않은 데이터 구조 정의 (예: complexity_score를 문자열로 전달)
    invalid_data = {
        "user_role": "developer",
        "projected_duration_days": "thirty days", # <-- Pydantic이 거부해야 하는 타입 오류
        "estimated_hours": 10,
        "complexity_score": 5.0
    }

    # 2. 예외 발생 검증 (ValidationError를 기대)
    with pytest.raises(ValidationError):
        LossInputData(**invalid_data)

def test_e2e_business_logic_failure():
    """
    [실패 사례] Pydantic은 통과했지만, 비즈니스 규칙에 위배되는 데이터를 넣었을 때 (예: Role Check).
    """
    # 1. 스키마는 통과하지만, 서비스 로직에서 거부해야 하는 데이터
    mock_data = LossInputData(
        user_role="contractor", # <--- 비즈니스 규칙 위반 역할
        projected_duration_days=10,
        estimated_hours=80,
        complexity_score=5.0
    )

    # 2. ValueError 발생 검증 (Service Layer에서 정의한 예외 처리)
    with pytest.raises(ValueError, match="유효하지 않은 사용자 역할입니다."):
        calculate_diagnosis(mock_data)