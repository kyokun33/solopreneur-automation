from fastapi.testclient import TestClient
import pytest
from backend.main import calculate_total_loss, DataPoint, LossInputData

client = TestClient()

# Mock API Call (Mocking the input data structure)
@pytest.fixture
def mock_input():
    """테스트를 위한 표준 입력 데이터셋을 제공합니다."""
    return LossInputData(
        data_points=[
            DataPoint(time_period="T+1 year", risk_score=20.0, data_availability=True),
            # High Risk/Missing Data Point (Highest impact simulation)
            DataPoint(time_period="T+3 years", risk_score=85.0, data_availability=False), 
            DataPoint(time_period="T+5 years", risk_score=45.0, data_availability=True)
        ],
        base_hourly_loss_rate=55.0 # $55/hour 고정값 (근거: 회사 공동 목표)
    )

# 테스트 1: 기본 기능 검증 및 데이터 손실 시 패널티 작동 여부 확인
def test_high_risk_missing_data_penalty(mock_input):
    """데이터 결핍이 높은 페널티를 발생시키는지 검증합니다."""
    result = calculate_total_loss(
        [DataPoint(**d) for d in mock_input.data_points], 
        mock_input.base_hourly_loss_rate
    )
    # T+3 years (85점, Missing)가 가장 큰 손실 기여를 해야 합니다.
    assert result["total_estimated_loss"] > 1000.0 # 임계값 설정: 충분히 높은 값을 기대함
    assert "T+3 years_Loss" in result["breakdown"]

# 테스트 2: 데이터가 모두 완벽할 경우 (최소 손실) 검증
def test_all_data_perfect(mock_input):
    """모든 포인트의 데이터 가용성이 True일 때, 손실이 최소화되는지 검증합니다."""
    perfect_points = [
        DataPoint(time_period="T+1 year", risk_score=10.0, data_availability=True), 
        DataPoint(time_period="T+3 years", risk_score=20.0, data_availability=True), 
        DataPoint(time_period="T+5 years", risk_score=30.0, data_availability=True)
    ]
    result = calculate_total_loss(perfect_points, mock_input.base_hourly_loss_rate)
    # 이 경우 손실액이 매우 낮아야 합니다 (Loss Potential이 낮음).
    assert result["total_estimated_loss"] < 500.0 # 임계값 설정: 낮은 값을 기대함

# 테스트 3: 에러 케이스 - 리스크 점수가 범위를 벗어날 때 처리되는지 검증 (Pydantic 연동)
def test_invalid_risk_score():
    """잘못된 범위의 데이터가 들어왔을 때 API 레벨에서 적절히 실패하는지 확인합니다."""
    # risk_score: -10.0 (Invalid input for pydantic DataPoint)
    bad_points = [DataPoint(time_period="T+1", risk_score=-10.0, data_availability=True)] 
    with pytest.raises(Exception): # FastAPI/Pydantic 레벨에서 에러가 발생해야 함
        calculate_total_loss(bad_points, 55.0)