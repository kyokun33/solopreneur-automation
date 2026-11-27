import pytest
from api.services.loss_calculator import LossCalculatorService, CalculationBreakdownItem
from typing import Dict, Any

@pytest.fixture
def calculator():
    """테스트를 위한 LossCalculatorService 인스턴스를 제공합니다."""
    return LossCalculatorService(client_id="test_user")

# 테스트 케이스 1: 가장 심각한 손실 상황 (High Risk)
def test_high_risk_scenario(calculator):
    """시간 손실과 데이터 리스크 모두 높은 경우를 테스트합니다. (CRITICAL_LOSS 예상)"""
    data = {
        "working_hours": 20, # 20시간 근무
        "hourly_loss_rate": 75.0, # 시간당 $75 상승
        "data_integrity_risk_percent": 15.0, # 데이터 리스크 15%
        "total_assets": 50000 # 자산 $50,000
    }
    result = calculator.calculate_loss(data)

    # 예상 결과 검증 (시간 손실: 20 * 75 = 1500)
    assert result['detailed_breakdown'][0]['category'] == "시간 손실"
    assert result['detailed_breakdown'][0]['value'] == pytest.approx(1500.0)

    # 예상 결과 검증 (데이터 리스크: 50000 * 0.15 * 2.0 = 1500)
    data_risk = result['detailed_breakdown'][1]
    assert data_risk['category'] == "데이터 무결성 리스크"
    assert data_risk['value'] == pytest.approx(1500.0)

    # 총 손실 점수 검증 (1500 + 1500 = 3000)
    assert result['total_loss_score'] == pytest.approx(3000.0)
    assert result['analysis_status'] == "CRITICAL_LOSS_DETECTED"

# 테스트 케이스 2: 낮은 리스크 상황 (Low Risk / Baseline)
def test_low_risk_scenario(calculator):
    """손실이 미미한, 비교적 안전한 시나리오를 테스트합니다. (MONITORING_REQUIRED 예상)"""
    data = {
        "working_hours": 5, # 5시간 근무
        "hourly_loss_rate": 50.0, # 시간당 $50 하락
        "data_integrity_risk_percent": 1.0, # 데이터 리스크 1% (최소)
        "total_assets": 20000 # 자산 $20,000
    }
    result = calculator.calculate_loss(data)

    # 예상 결과 검증 (시간 손실: 5 * 50 = 250)
    assert result['detailed_breakdown'][0]['value'] == pytest.approx(250.0)
    
    # 예상 결과 검증 (데이터 리스크: 20000 * 0.01 * 2.0 = 400) -- 오, wait. 250+400=650. 여전히 Critical이 아닐 수도 있다.
    data_risk = result['detailed_breakdown'][1]
    assert data_risk['value'] == pytest.approx(400.0)

    # 총 손실 점수 검증 (250 + 400 = 650)
    total = result['total_loss_score']
    assert total == pytest.approx(650.0)
    # 이 시나리오는 임계치(1000)보다 낮으므로, 모니터링 상태여야 함.
    assert result['analysis_status'] == "MONITORING_REQUIRED"

# 테스트 케이스 3: 입력값 유효성 검증 (Edge Case)
def test_zero_input_scenario(calculator):
    """모든 값이 최소 또는 0인 경우를 테스트하여 시스템이 깨지지 않음을 확인합니다."""
    data = {
        "working_hours": 0, # 근무 시간 없음
        "hourly_loss_rate": 55.0,
        "data_integrity_risk_percent": 0, # 데이터 리스크 0%
        "total_assets": 100000
    }
    result = calculator.calculate_loss(data)

    # 모든 손실이 0이어야 함
    assert result['total_loss_score'] == pytest.approx(0.0)
    for breakdown in result['detailed_breakdown']:
        assert breakdown['value'] == pytest.approx(0.0)
        
# 테스트 케이스 4: 필수 입력 누락 시 (실패 처리 확인)
def test_missing_input_handling(calculator):
    """필수 값이 누락되거나 숫자가 아닌 경우, 서비스가 예외를 던지지 않고 안정적으로 처리하는지 검증합니다."""
    data = {
        "working_hours": "invalid_text", # 잘못된 타입 입력 시도
        "hourly_loss_rate": 55.0,
        "data_integrity_risk_percent": 1.0,
        "total_assets": 100000
    }
    # Service 내부의 try-except 로직이 작동하여 에러를 처리하고 0을 반환해야 함.
    result = calculator.calculate_loss(data)
    assert result['total_loss_score'] == pytest.approx(400.0) # 시간 손실은 0, 데이터 리스크만 계산되어야함.