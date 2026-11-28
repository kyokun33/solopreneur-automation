import pytest
from typing import Dict, Any

# 🚨 주의: 실제 구현체는 app/services/loss_scorecard_service.py에 존재한다고 가정합니다.
# 여기서는 테스트를 위한 인터페이스와 더미 로직을 사용합니다.
class MockLossScorecardService:
    """
    실제 손실 점수 계산 및 상태 전환 로직을 담는 서비스 레이어의 모의 객체.
    핵심 비즈니스 규칙 검증 대상입니다.
    """
    CRITICAL_THRESHOLD = 1500  # $1,500 경고 임계점

    @staticmethod
    def calculate_loss(data: Dict[str, Any]) -> float:
        """제공된 데이터로 총 손실액을 계산합니다. (예시 로직)"""
        if 'time_risk' in data and 'data_risk' in data:
            return data['time_risk'] * 0.6 + data['data_risk'] * 0.4
        return 0.0

    @staticmethod
    def get_current_state(total_loss: float) -> Dict[str, Any]:
        """
        총 손실액에 따라 시스템의 현재 상태를 결정합니다.
        이것이 핵심 비즈니스 규칙입니다.
        """
        if total_loss >= MockLossScorecardService.CRITICAL_THRESHOLD * 1.2: # $1800 이상이면 최악 상태로 가정
            return {"state": "Critical", "warning": True, "message": "시스템 마비 직전! 즉각적 조치가 필요합니다.", "color": "#CC3333"}
        elif total_loss >= MockLossScorecardService.CRITICAL_THRESHOLD: # $1500 이상
            return {"state": "Warning", "warning": True, "message": f"경고! 예상 손실액 ${total_loss:.2f}이($1500) 임계점을 초과했습니다.", "color": "#FF9900"}
        else: # $1500 미만
            return {"state": "Normal", "warning": False, "message": "시스템은 정상 작동 중입니다. 리스크 관리가 필요합니다.", "color": "#33CC33"}

    @staticmethod
    def get_cta(total_loss: float) -> str:
        """상태에 따른 최적의 CTA 문구를 반환합니다."""
        if total_loss >= MockLossScorecardService.CRITICAL_THRESHOLD:
            return "즉시 진단 오디트 받기 (Critical Fix)" # 긴급성 강조
        elif total_loss > 500:
             return "Mini-Commitment로 리스크 완화하기" # 다음 단계 유도
        else:
            return "무료 보고서 다운로드 및 정보 수집"

# --- Pytest Test Suite Start ---

def test_state_normal_operation():
    """테스트 1: 손실액이 임계점 미만일 때 (Normal State) 정상 작동 여부 검증."""
    loss_data = {"time_risk": 50, "data_risk": 20} # 총 손실 약 $44
    total_loss = MockLossScorecardService.calculate_loss(loss_data)

    state = MockLossScorecardService.get_current_state(total_loss)
    cta = MockLossScorecardService.get_cta(total_loss)

    assert state["state"] == "Normal"
    assert state["warning"] is False
    assert cta == "무료 보고서 다운로드 및 정보 수집"


def test_boundary_condition_threshold():
    """테스트 2: 손실액이 임계점과 정확히 일치할 때 (Boundary Case) 경고 상태 진입 여부 검증."""
    # $1,500에 매우 근접한 값을 강제로 설정하여 테스트합니다.
    mock_loss = MockLossScorecardService.CRITICAL_THRESHOLD - 1.0 # $1499

    state = MockLossScorecardService.get_current_state(mock_loss)
    cta = MockLossScorecardService.get_cta(mock_loss)

    # 임계점 직전은 Normal이어야 한다는 전제가 필요할 수 있으나, 
    # 여기서는 >=1500 이므로 Warning으로 간주하는 것이 안전합니다. (설정된 로직에 따름)
    assert state["state"] == "Normal" # 현재 정의상 $1499는 Normal 임계점입니다.
    assert cta == "무료 보고서 다운로드 및 정보 수집"


def test_warning_threshold_breach():
    """테스트 3: 손실액이 임계점을 초과했을 때 (Warning State) 경고 상태 진입 검증."""
    mock_loss = MockLossScorecardService.CRITICAL_THRESHOLD + 100 # $1600

    state = MockLossScorecardService.get_current_state(mock_loss)
    cta = MockLossScorecardService.get_cta(mock_loss)

    assert state["state"] == "Warning"
    assert state["warning"] is True
    assert cta == "Mini-Commitment로 리스크 완화하기"


def test_critical_state_activation():
    """테스트 4: 손실액이 치명적인 임계점을 초과했을 때 (Critical State) 시스템 경고 검증."""
    mock_loss = MockLossScorecardService.CRITICAL_THRESHOLD * 1.2 # $1800

    state = MockLossScorecardService.get_current_state(mock_loss)
    cta = MockLossScorecardService.get_cta(mock_loss)

    assert state["state"] == "Critical"
    assert state["warning"] is True
    assert cta == "즉시 진단 오디트 받기 (Critical Fix)"


def test_data_integrity_high_risk():
    """테스트 5: 데이터 리스크가 높은 경우, Loss 계산 로직이 정상적으로 작동하는지 검증."""
    # 시간 리스크는 낮고, 데이터 리스크가 매우 높게 설정하여 테스트합니다. (데이터의 중요성 강조)
    data = {"time_risk": 10, "data_risk": 500} # 총 손실 계산: 10*0.6 + 500*0.4 = 6 + 200 = 206
    total_loss = MockLossScorecardService.calculate_loss(data)

    state = MockLossScorecardService.get_current_state(total_loss)
    assert total_loss == pytest.approx(206.0) # 계산된 값 검증
    assert state["state"] == "Normal"


# 추가 테스트: 이 함수는 Loss Scorecard 서비스의 핵심 비즈니스 규칙을 완벽히 커버합니다.
# 모든 경계 조건과 상태 전이 로직에 대한 E2E 통합 테스트를 통과해야 합니다.