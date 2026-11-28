import pytest
from src.core.loss_scorecard_service import LossScorecardService, LossCalculationInput

# 테스트를 위한 헬퍼 함수
def get_input(action: str, points: int, hours: float) -> LossCalculationInput:
    return {"action_type": action, "data_points_collected": points, "estimated_hours_at_risk": hours}

@pytest.fixture(scope="module")
def service():
    """테스트를 위한 LossScorecardService 인스턴스를 제공합니다."""
    return LossScorecardService()

# =========================================================
# 테스트 케이스 1: 초기 상태 -> 경고 임계값 진입 (Mini-Commitment Loop 필수)
# 목표: $1,500에 도달하며, 다음 단계로 가기 전 Mini-Commitment를 요구하는지 검증.
@pytest.mark.parametrize("initial_score, input_data", [
    (0.0, get_input("diagnosis", 10, 20)), # 초기 $0에서 시작하여 리스크 증가
])
def test_transition_to_warning_state(service: LossScorecardService, initial_score, input_data):
    """Warning 임계값 ($1500) 근처로 도달할 때의 상태 변화 및 Mini-Commitment 요구 여부 테스트."""
    # 이 예시에서는 20시간 * $55/hr = $1100. 진단 가중치 10 * 10 = $100. 합계 약 $1200
    # 임계값 검증을 위해, 점수를 강제로 조정하여 Warning에 가까워지게 가정합니다.
    # 실제로는 여러 단계의 accumulation이 필요하지만, 테스트 목적상 이 시나리오를 검증합니다.

    # 임계값 근처로 가기 위해 더 높은 리스크가 필요하다고 보고서 상에서 가정하고, 
    # $1500 이상을 목표로 하는 데이터 입력을 만듭니다. (예: 고위험 워크숍 참여)
    high_risk_input = get_input("workshop", 30, 20) # 예상 점수 계산: 50*30 + 55*20 = 1500 + 1100 = $2600

    # 초기 스코어를 $800으로 설정하여, high_risk_input을 통해 Warning/Critical 구간 진입 시뮬레이션
    result = service.calculate_and_transition(initial_score=800.0, input_data=high_risk_input)

    assert result["new_state"] == "Warning" or result["new_state"] == "Critical", \
        f"예상 상태 (Warning/Critical)와 다른 상태: {result['new_state']}"
    assert result["mini_commitment_needed"] is True, \
        "경고 단계에 진입했음에도 Mini-Commitment Loop가 요구되지 않았습니다."


# =========================================================
# 테스트 케이스 2: Critical 임계값 진입 및 최종 CTA 확인
# 목표: $5,000 이상 도달 시 State가 Critical로 바뀌며, 명확한 최상위 상품(CTA)이 제시되는지 검증.
def test_transition_to_critical_state(service: LossScorecardService):
    """Critical 임계값 ($5000) 초과 진입 시의 상태 및 CTA 검증."""
    # $1,000 (기존) + $4,200 (새로운 워크숍) = $5,200
    critical_input = get_input("workshop", 30, 40) # 예상 점수 계산: 50*30 + 55*40 = 1500 + 2200 = $3700. (이거로는 부족하므로 점수를 조정합니다.)
    # 강제로 $5,200 이상을 만드는 입력값으로 테스트를 재구성합니다.
    high_loss_input: LossCalculationInput = {"action_type": "workshop", "data_points_collected": 50, "estimated_hours_at_risk": 100} # 50*50 + 55*100 = 2500 + 5500 = $8000

    result = service.calculate_and_transition(initial_score=2000.0, input_data=high_loss_input) # 초기 스코어 2000 + 8000 = 10000

    assert result["new_state"] == "Critical", \
        f"예상 상태 (Critical)와 다른 상태: {result['new_state']}"
    assert "워크숍 예약" in result["required_action"], \
        "최종 CTA가 '법적 자문 워크숍' 등 고가치 상품으로 유도되지 않았습니다."

# =========================================================
# 테스트 케이스 3: 정상적인 Low Risk 상태 유지 및 점진적 상승 확인 (엣지케이스)
# 목표: 임계값을 넘지 않으면서, 낮은 위험 단계에 머무를 때의 로직이 깨지지 않는지 검증.
def test_staying_in_low_risk_state(service: LossScorecardService):
    """임계값 미만에서 안정적으로 점수가 상승하며 LowRisk 상태를 유지하는 경우 테스트."""
    # $1,500 임계값에 도달하지 못할 만큼의 적절한 진단 활동을 가정합니다.
    low_risk_input = get_input("diagnosis", 20, 10) # 예상 점수: 10*20 + 55*10 = $700

    # 초기 스코어 500원에서 시작하여 Low Risk 상태를 유지하는지 검증
    result = service.calculate_and_transition(initial_score=500.0, input_data=low_risk_input) # 총점: 1200

    assert result["new_state"] == "LowRisk", \
        f"예상 상태 (LowRisk)와 다른 상태: {result['new_state']}"
    assert result["mini_commitment_needed"] is False, \
        "Low Risk 단계에서는 Mini-Commitment가 불필요하거나 다른 형태여야 합니다."