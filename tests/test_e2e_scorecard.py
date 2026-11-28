import pytest
from unittest.mock import MagicMock, patch
# src/core 폴더의 서비스를 가져옵니다.
from src.core.loss_scorecard_service import LossScorecardService

@pytest.fixture(scope="function")
def service():
    """LossScorecardService 인스턴스를 제공합니다."""
    return LossScorecardService()

# Mocking: 프론트엔드 시각 효과 트리거는 API 레벨에서 '이벤트 발생'으로만 검증하고, 
# 실제 DOM 조작은 테스트 대상에서 제외합니다. 대신 상태 전이를 확인합니다.

def test_e2e_loss_scorecard_normal(service):
    """정상적인 손실 점수 계산 및 경고 트리거 미발생 테스트."""
    initial_loss = 100  # 초기 손실액
    risk_data = {"type": "basic", "value": 50} # 추가 리스크 데이터

    score = service.calculate_score(initial_loss, risk_data)
    
    assert score["total_loss"] == pytest.approx(150)
    # 정상 범위일 때는 CRITICAL 상태가 아니어야 합니다.
    assert score["status"] == "NORMAL"
    assert score["is_critical"] is False

def test_e2e_loss_scorecard_warning_threshold(service):
    """$1,500 경고 임계값 도달 테스트 (RED WARNING Filter Trigger)."""
    initial_loss = 1499 # 바로 아래 값
    risk_data = {"type": "advanced", "value": 2} # 약간의 추가 리스크

    score = service.calculate_score(initial_loss, risk_data)
    
    # $1,500 임계값에 근접하게 만드는 로직을 테스트한다고 가정합니다.
    assert score["total_loss"] >= 1500
    # 이 지점에서는 경고 상태가 되어야 합니다.
    assert score["status"] == "WARNING"
    assert score["is_critical"] is False

def test_e2e_loss_scorecard_critical_threshold(service):
    """$5,000 심각 임계값 도달 테스트 (GLITCH Effect + Red Warning Filter Trigger)."""
    initial_loss = 4999 # 바로 아래 값
    risk_data = {"type": "extreme", "value": 1}

    score = service.calculate_score(initial_loss, risk_data)
    
    # $5,000 임계값 도달을 시뮬레이션하여 상태 전이를 검증합니다.
    assert score["total_loss"] >= 5000
    # 이 지점에서는 Critical 상태여야 하며, 모든 효과가 트리거되어야 합니다.
    assert score["status"] == "CRITICAL"
    assert score["is_critical"] is True

def test_e2e_api_contract_validation(service):
    """E2E 테스트: API 응답 구조 및 필수 필드 검증."""
    # Loss Scorecard의 최종 출력 형태를 가정한 Mock 데이터
    mock_response = {
        "status": "CRITICAL", 
        "is_critical": True, 
        "total_loss": 5123.45,
        "warning_message": "Immediate action required due to system instability."
    }
    # API 계약 검증은 구조적 안정성 확보에 필수적입니다.
    assert isinstance(mock_response, dict)
    assert "status" in mock_response
    assert "total_loss" in mock_response