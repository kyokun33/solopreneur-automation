from services.loss_calculator.models import CalculationInput, TotalLossReport, LossAssessment
from services.loss_calculator.financial_risk_engine import FinancialRiskEngine
from services.loss_calculator.ip_similarity_engine import IPSimilarityEngine

class LossCalculationEngine:
    """
    고고플랙스의 핵심 로스 계산 엔진 (Orchestrator). 
    모듈화된 리스크 진단 모듈들을 호출하고 최종 보고서를 종합합니다.
    """
    def __init__(self):
        # 의존성 주입(Dependency Injection) 방식으로 각 엔진을 초기화합니다.
        self._financial_engine = FinancialRiskEngine()
        self._ip_engine = IPSimilarityEngine()

    def calculate_total_loss(self, input: CalculationInput) -> TotalLossReport:
        """
        전체 Loss Report를 생성하는 메인 진입점입니다. 
        모든 계산을 하나의 트랜잭션처럼 처리하며 오류 발생 시도합니다.
        """
        print("⚙️ [Engine] Starting total loss calculation...")
        
        detailed_assessments: List[LossAssessment] = []

        # 1. 재무 리스크 진단 (가장 기본적이고 필수적인 지표)
        financial_assessment = self._financial_engine.calculate_risk(input)
        detailed_assessments.append(financial_assessment)

        # 2. IP 유사성 리스크 진단 (고차원 분석 영역)
        ip_assessment = self._ip_engine.calculate_risk(input)
        detailed_assessments.append(ip_assessment)

        # 3. 최종 종합 점수 및 손실액 계산 (가중치 부여)
        total_score = detailed_assessments[0].score * 0.4 + detailed_assessments[1].score * 0.6 # 예시 가중치
        total_loss_usd = detailed_assessments[0].estimated_loss_usd + detailed_assessments[1].estimated_loss_usd

        # 최종 보고서 반환
        return TotalLossReport(
            total_loss_score=round(total_score, 4),
            total_estimated_loss_usd=round(total_loss_usd, 2),
            detailed_assessments=detailed_assessments
        )