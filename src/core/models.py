from enum import Enum
from typing import TypedDict, Literal

# ------------------------------------------
# 1. 상태(State) 정의 - State Machine의 핵심
# ------------------------------------------

class LossScorecardState(Enum):
    """손실 점수카드의 현재 비즈니스 상태를 정의합니다."""
    INITIAL = "Initial"          # 초기 진단 단계 (아무것도 모름)
    LOW_RISK = "LowRisk"         # 낮은 손실 위험 (진단 완료, 행동 필요)
    WARNING = "Warning"          # 경고 단계 ($1,500 임계값 도달)
    CRITICAL = "Critical"        # 심각 단계 ($5,000 임계값 도달)
    SECURED = "Secured"          # 해결책 구매/진행 완료 (가장 높은 수익화 지점)

# ------------------------------------------
# 2. 데이터 스키마 정의 - 타입 안정성 보장
# ------------------------------------------

class LossCalculationInput(TypedDict):
    """상태 전이 및 손실 점수 계산에 필요한 입력 데이터."""
    action_type: Literal["diagnosis", "workshop", "followup"] # 어떤 종류의 상호작용인지
    data_points_collected: int                               # 수집된 구체적인 정보 포인트 개수
    estimated_hours_at_risk: float                            # 위험에 노출된 추정 시간 (시간)

class TransitionResult(TypedDict):
    """상태 전이 로직의 최종 출력 스키마."""
    new_score: float                                        # 업데이트된 총 손실 점수 ($)
    new_state: LossScorecardState                            # 새로운 상태
    required_action: str                                    # 다음 단계에서 사용자에게 요구되는 행동 (CTA)
    mini_commitment_needed: bool                             # Mini-Commitment Loop가 필요한지 여부