from dataclasses import dataclass
import math
from typing import Optional
from services.loss_calculator.models import CalculationInput, LossAssessment

class FinancialRiskEngine:
    """
    재무 리스크 계산 전담 엔진. 
    사용자의 시간 투입과 잠재 수익을 기반으로 '기회비용 손실'을 측정합니다.
    [원칙] 모든 외부 입력에는 반드시 가드 로직(Guard Logic)이 적용되어야 합니다.
    """

    def calculate_risk(self, input_data: CalculationInput) -> LossAssessment:
        """
        재무 리스크 점수를 계산하고 LossAssessment 객체로 반환합니다.
        """
        try:
            # 1. 필수 입력값 유효성 검사 (Guard Logic)
            if input_data.user_time_hours is None or input_data.potential_revenue_usd is None:
                raise ValueError("시간 투입량과 잠재 수익액은 필수로 제공되어야 합니다.")

            # 2. 기본 로직 계산 (예시 공식: 손실 = 시간 * Loss Rate / 잠재수익)
            # 가상의 '기회비용 손실률'을 사용합니다.
            LOSS_RATE_PER_HOUR = 55.0 # $55/hour [근거: Self-RAG]

            if input_data.potential_revenue_usd <= 0:
                return LossAssessment(
                    risk_type="Financial", score=0.0, estimated_loss_usd=0.0, severity_level="LOW"
                )

            # 손실 계산 로직: (시간 * 시간당 손실률) / 잠재 수익
            raw_loss = input_data.user_time_hours * LOSS_RATE_PER_HOUR
            loss_score = min(1.0, raw_loss / input_data.potential_revenue_usd) # 점수 최대 1.0 제한

            # 예상 손실 금액 (원래의 기회비용을 그대로 반환)
            estimated_loss = raw_loss * loss_score

            # 3. 심각도 레벨 결정 로직
            if loss_score >= 0.5:
                severity = "CRITICAL"
            elif loss_score >= 0.1:
                severity = "MODERATE"
            else:
                severity = "LOW"

            return LossAssessment(
                risk_type="Financial", 
                score=loss_score, 
                estimated_loss_usd=round(estimated_loss, 2), 
                severity_level=severity
            )

        except ValueError as e:
            print(f"[ERROR] Financial Risk Calculation Failed (Validation): {e}")
            # 실패 시점에는 최소한의 안전값을 반환하여 전체 시스템이 무너지지 않게 함.
            return LossAssessment("Financial", 0.0, 0.0, "UNKNOWN")
        except Exception as e:
            print(f"[FATAL ERROR] Financial Risk Calculation Failed (System): {e}")
            return LossAssessment("Financial", 1.0, 9999.99, "CRITICAL_FAILURE")