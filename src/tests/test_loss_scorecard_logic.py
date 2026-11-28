import unittest
from unittest.mock import MagicMock, patch

# 1단계에서 만든 서비스 모듈을 임포트한다고 가정합니다.
try:
    from src.backend.services.loss_scorecard_service import LossScorecardService, LossState
except ImportError:
    print("🚨 Warning: loss_scorecard_service.py를 먼저 실행하여 경로 설정을 확인해주세요.")


class TestLossScorecardLogic(unittest.TestCase):

    def setUp(self):
        """각 테스트 케이스마다 초기화하는 설정"""
        # 기본 시나리오 데이터 (평상시)
        self.safe_data = {"financial_loss": 500, "data_integrity": 10}
        self.initial_mock_loss = 100 # Mocking을 위해 낮은 초기 손실값 설정

    # --- [Test Case Group: Safe State (안전 상태)] ---
    def test_safe_state_no_warning(self):
        """손실 점수가 경고 임계치 미만일 때 안전 상태가 유지되는지 검증."""
        service = LossScorecardService(initial_loss=100)
        score, state = service.generate_scorecard(self.safe_data)
        # 예상 점수: 500 + 10 = 510. Safe State여야 함.
        self.assertLessEqual(score, 1500)
        self.assertEqual(state, LossState.SAFE)

    def test_safe_state_low_initial_loss(self):
        """초기 손실 자체가 적을 때도 안전 상태가 유지되는지 검증."""
        service = LossScorecardService(initial_loss=50)
        score, state = service.generate_scorecard({"financial_loss": 10, "data_integrity": 2})
        self.assertEqual(state, LossState.SAFE)

    # --- [Test Case Group: Warning State (경고 상태)] ---
    def test_warning_state_boundary_low(self):
        """손실 점수가 경고 임계치($1,500)에 도달하여 WARNING으로 전이하는지 검증."""
        # 목표 점수: 1500. 초기 손실을 낮게 설정하고 리스크를 높여서 테스트합니다.
        warning_data = {"financial_loss": 1480, "data_integrity": 20} # 총점 1500 근처
        service = LossScorecardService(initial_loss=10)
        score, state = service.generate_scorecard(warning_data)
        self.assertGreaterEqual(score, 1490)
        # $1,500 기준을 만족하는지 확인 (경계값 테스트)
        self.assertEqual(state, LossState.WARNING)

    def test_warning_state_boundary_high(self):
        """손실 점수가 WARNING 상태의 최대치 근처에 머무르는지 검증."""
        # 경고 상한선은 $15,000 (임시로 설정된 Upper Bound)을 초과하지 않아야 함.
        warning_data = {"financial_loss": 1200, "data_integrity": 30} # 총점 1230 (경고 영역 내)
        service = LossScorecardService(initial_loss=50)
        score, state = service.generate_scorecard(warning_data)
        self.assertEqual(state, LossState.WARNING)

    # --- [Test Case Group: Critical State (위험/임계 상태)] ---
    def test_critical_state_hard_threshold_violation(self):
        """총 손실 점수가 임계치($15,000 이상)를 초과했을 때 CRITICAL로 전이하는지 검증."""
        critical_data = {"financial_loss": 16000, "data_integrity": 10} # 총점 16000
        service = LossScorecardService(initial_loss=50)
        score, state = service.generate_scorecard(critical_data)
        self.assertGreaterEqual(score, 16000)
        self.assertEqual(state, LossState.CRITICAL)

    def test_critical_state_additional_risk_violation(self):
        """경고 상태에서 추가적인 리스크($300 초과)가 발생하여 CRITICAL로 전이하는지 검증."""
        # 초기 손실 1500 (WARNING 경계선). 여기에 $300 이상의 데이터 무결성 리스크가 들어오는 경우.
        critical_data = {"financial_loss": 1500, "data_integrity": 400} # 총점 1900
        service = LossScorecardService(initial_loss=1500)
        score, state = service.generate_scorecard(critical_data)
        self.assertGreaterEqual(score, 1800) # 1500 + 300 초과 확인
        self.assertEqual(state, LossState.CRITICAL)


if __name__ == '__main__':
    unittest.main()