import unittest
from services.loss_calculator.models import CalculationInput, TotalLossReport
from services.loss_calculator.loss_engine import LossCalculationEngine

class TestLossCalculator(unittest.TestCase):
    
    def setUp(self):
        """각 테스트 전 초기화 작업 수행."""
        self.engine = LossCalculationEngine()
        # 정상적인 입력 데이터 (Moderate Risk 예상)
        self.good_input = CalculationInput(
            user_time_hours=10.0, 
            potential_revenue_usd=5000.0, # $55/hr * 10h = $550 기회비용 손실. 점수: 550/5000 = 0.11 (Moderate)
            ip_asset_name="AI-Powered Content Generator",
            comparison_assets=["Competitor A Blog", "Competitor B Site"], # 2개
            user_data_integrity_score=0.8  # 무결성 점수 높음 -> IP 리스크 감소
        )

    def test_successful_calculation(self):
        """정상적인 데이터로 전체 로스 계산이 잘 되는지 테스트합니다."""
        report: TotalLossReport = self.engine.calculate_total_loss(self.good_input)
        # 종합 점수와 손실액이 0보다 크고, 개별 평가가 담겨 있는지 확인
        self.assertTrue(report.detailed_assessments)
        self.assertGreater(report.total_estimated_loss_usd, 10.0)

    def test_extreme_risk_scenario(self):
        """모든 리스크 지표가 최고치일 때 (Critical/Max Loss) 테스트합니다."""
        # 최악의 시나리오: 시간 많이 투입, 수익 거의 없음, IP 자산명 없고 비교군도 많음, 데이터 무결성 0.0
        bad_input = CalculationInput(
            user_time_hours=100.0, # 엄청난 시간 소요
            potential_revenue_usd=10.0, # 수익 거의 없음
            ip_asset_name="High Risk IP",
            comparison_assets=["C1", "C2", "C3", "C4", "C5"], # 5개 (최대)
            user_data_integrity_score=0.0 # 무결성 바닥
        )
        report: TotalLossReport = self.engine.calculate_total_loss(bad_input)
        # 점수와 손실액이 높은 값으로 측정되는지 확인 (Critical Zone 진입 검증)
        self.assertGreater(report.total_estimated_loss_usd, 10000.0)

    def test_missing_required_data_financial_risk(self):
        """필수 입력값(Potential Revenue)이 누락되었을 때 Financial Engine에서 예외 처리되는지 테스트합니다."""
        bad_input = CalculationInput(
            user_time_hours=10.0, 
            potential_revenue_usd=None, # NULL 값 주입 -> ValueError 발생 유도
            ip_asset_name="Test",
            comparison_assets=["C1"],
            user_data_integrity_score=1.0
        )
        # 엔진이 크래시되지 않고 UNKNOWN/Safe 상태를 반환하는지 확인 (가장 중요!)
        report: TotalLossReport = self.engine.calculate_total_loss(bad_input)
        financial_assessment = report.detailed_assessments[0]
        self.assertEqual(financial_assessment.severity_level, "UNKNOWN")

    def test_missing_required_data_ip_risk(self):
        """IP Engine의 필수 입력값(Comparison Assets)이 누락되었을 때 예외 처리되는지 테스트합니다."""
        bad_input = CalculationInput(
            user_time_hours=10.0, 
            potential_revenue_usd=5000.0,
            ip_asset_name="Test",
            comparison_assets=[], # 빈 리스트 주입 -> ValueError 발생 유도
            user_data_integrity_score=1.0
        )
        report: TotalLossReport = self.engine.calculate_total_loss(bad_input)
        ip_assessment = report.detailed_assessments[1]
        self.assertEqual(ip_assessment.severity_level, "UNKNOWN")

if __name__ == '__main__':
    unittest.main()