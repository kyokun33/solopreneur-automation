from enum import Enum
import typing as t

# 상태 전이에 필요한 Enum 정의 (가정)
class LossState(Enum):
    SAFE = "Safe"          # $0 - $1,500 미만
    WARNING = "Warning"    # $1,500 ~ $15,000 사이
    CRITICAL = "Critical"  # $300 초과 또는 임계값 초과
    MITIGATED = "Mitigated" # 조치 후 안전 상태로 복귀

class LossScorecardService:
    """
    Loss Scorecard의 핵심 계산 로직 및 상태 전이를 담당하는 서비스.
    외부 API 의존성을 제거하고 순수 비즈니스 로직만 포함해야 합니다.
    """
    def __init__(self, initial_loss_amount: float):
        self.initial_loss = initial_loss_amount

    @staticmethod
    def calculate_score(raw_data: t.Dict[str, any]) -> float:
        """
        임의 데이터를 기반으로 손실 점수를 계산하는 Mock 함수입니다.
        실제로는 복잡한 리스크 산정 공식이 들어갑니다.
        """
        # 데이터 무결성 리스크를 최우선 가중치로 적용한다고 가정
        data_integrity_risk = raw_data.get("data_integrity", 0)
        loss_amount = raw_data.get("financial_loss", 0)
        return loss_amount + data_integrity_risk

    @staticmethod
    def determine_state(score: float, initial_loss: float) -> LossState:
        """
        계산된 점수와 초기 손실액을 기반으로 최종 상태를 결정합니다.
        이 함수가 테스트의 핵심 목표입니다.
        [근거: 지난 의사결정 로그 - $1,500 및 $300 임계값]
        """
        # 1. Critical Threshold Check (최우선)
        if score >= initial_loss + 300 or score > 15000: # Total loss가 높거나, 경고 상태에서 추가 리스크 발생 시
            return LossState.CRITICAL
        
        # 2. Warning Threshold Check
        elif score >= 1500 and score < initial_loss + 300:
             # 초기 손실액에 따라 경고 기준이 달라질 수 있으나, 일단 $1,500을 기준으로 잡음.
            return LossState.WARNING

        # 3. Safe State
        else:
            return LossState.SAFE


    def generate_scorecard(self, raw_data: t.Dict[str, any]) -> t.Tuple[float, LossState]:
        """
        점수 계산 및 상태 전이를 통합하여 최종 결과물을 반환합니다.
        """
        calculated_score = self.calculate_score(raw_data)
        final_state = self.determine_state(calculated_score, self.initial_loss)
        return calculated_score, final_state