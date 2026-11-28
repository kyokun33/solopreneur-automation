from typing import Optional
from models import LossScorecardState, LossCalculationInput, TransitionResult
import math

class LossScorecardService:
    """
    Loss Scorecard의 상태 전이 로직을 관리하는 핵심 서비스 클래스.
    모든 비즈니스 규칙과 임계값 검증이 여기에 집중됩니다.
    [근거: CEO 지시]
    """
    # 초기 상태는 항상 Initial로 시작합니다.
    INITIAL_SCORE = 0.0

    @staticmethod
    def _calculate_loss(input_data: LossCalculationInput) -> float:
        """입력 데이터를 기반으로 손실 점수를 계산하는 순수 함수."""
        # 로직 가중치 정의 (비즈니스에 따라 조정 가능)
        DIAGNOSIS_WEIGHT = 10.0 # 진단만 해도 기본적으로 일정 리스크가 발생함
        WORKSHOP_WEIGHT = 50.0  # 워크숍 참여는 높은 정보 가치를 가지므로 점수 상승 폭이 큼
        FOLLOWUP_WEIGHT = 20.0

        if input_data['action_type'] == "diagnosis":
            base_loss = DIAGNOSIS_WEIGHT
        elif input_data['action_type'] == "workshop":
            base_loss = WORKSHOP_WEIGHT
        else: # followup
            base_loss = FOLLOWUP_WEIGHT

        # 손실 점수 계산 공식: (기본 가중치 * 데이터 포인트) + (위험 시간당 비용 * 총 시간)
        total_loss = base_loss * input_data['data_points_collected'] + \
                     (55.0 * input_data['estimated_hours_at_risk']) # $55/hour 고정값 사용

        return round(total_loss, 2)

    @staticmethod
    def calculate_and_transition(current_score: float, input_data: LossCalculationInput) -> TransitionResult:
        """
        현재 점수와 새로운 데이터를 받아 다음 상태를 계산하고 전이합니다.
        [근거: CEO 지시]
        """
        new_score = LossScorecardService._calculate_loss(input_data)
        total_score = current_score + new_score

        # 1. 임계값 기반의 상태 전이 로직 (State Transition Logic)
        if total_score >= 5000:
            new_state = LossScorecardState.CRITICAL
            required_action = "최종 진단 및 법적 자문 워크숍 예약" # 가장 비싼 상품 유도
        elif total_score >= 1500:
            new_state = LossScorecardState.WARNING
            required_action = "Mini-Commitment Loop: 무료 핵심 체크리스트 다운로드 (사전 진단)" # 중간 단계 유도
        else:
            # 초기 또는 낮은 위험 단계는 LowRisk로 간주하고 다음 단계를 제시
            new_state = LossScorecardState.LOW_RISK if total_score > 0 else LossScorecardState.INITIAL
            required_action = "Anti-Loss Funnel Stage 2 진입: 핵심 정보 제공을 위한 이메일 수집"

        # 2. Mini-Commitment Loop 검증 (강제적인 다음 행동 유도)
        mini_commitment_needed = False
        if new_state == LossScorecardState.WARNING and input_data['action_type'] != "workshop":
            mini_commitment_needed = True # 경고 단계 진입 시, 최소한의 행동(체크리스트 다운로드 등)이 필요함을 강제

        # 3. 결과 반환
        return TransitionResult(
            new_score=round(total_score, 2),
            new_state=new_state,
            required_action=required_action,
            mini_commitment_needed=mini_commitment_needed
        )

# 초기 상태 테스트 함수 (간단한 검증용)
def initialize_service() -> LossScorecardService:
    """서비스의 기본 인스턴스를 반환합니다."""
    return LossScorecardService()