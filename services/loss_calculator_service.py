import typing as t
from dataclasses import dataclass, field
from datetime import datetime

# --- 1. 데이터 구조 정의 (API Contract) ---

@dataclass
class LossBreakdownItem:
    """개별 손실 항목의 상세 내역을 담는 데이터 클래스."""
    category: str  # 예: TimeLoss, DataBiasRisk, ComplianceRisk
    description: str # 이 항목이 왜 손실인지 설명 (UX/카피라이팅에 활용)
    raw_value: float # 사용자가 입력한 원본 값 (시간, 빈도수 등)
    weight: float  # 적용된 가중치 또는 계수
    calculated_loss: float # 최종 계산된 손실 점수

@dataclass
class LossScoreResult:
    """손실 점수 산출의 최종 결과물 구조."""
    total_score: float # 총 손실 점수 (Loss Scorecard의 메인 숫자)
    breakdown: t.List[LossBreakdownItem] = field(default_factory=list) # 계산 과정 전체
    summary_message: str = "손실 위험이 감지되었습니다."

# --- 2. 순수 서비스 클래스 정의 (Pure Service Class) ---

class LossCalculatorService:
    """
    고고플랙스의 핵심 비즈니스 로직: 손실 점수를 산출하는 순수 서비스 클래스.
    모든 외부 의존성(API 호출, DB 접근 등)으로부터 분리되어 테스트 용이성을 극대화합니다.
    """

    # 상수 정의 (근거 기반 고정값)
    TIME_LOSS_RATE = 55.0  # $55/hour [근거: 2026-08-30]
    DEFAULT_RISK_MULTIPLIER = 1.5 # 기본 리스크 가중치

    def __init__(self):
        pass

    def calculate_loss(
        self,
        time_spent_hours: float,
        data_bias_risk_score: float, # 0.0 ~ 1.0 사이의 점수 (예시)
        compliance_failure_count: int, # 법규 위반 건수 등 정수 카운트
    ) -> LossScoreResult:
        """
        사용자가 제공한 여러 리스크 데이터를 기반으로 총 손실 점수를 계산하고,
        각 항목별 상세 Breakdown을 포함하여 결과를 반환합니다.

        Args:
            time_spent_hours: 시간 손실에 사용된 누적 시간 (시간 단위).
            data_bias_risk_score: 데이터 편향 위험도 (0.0 ~ 1.0).
            compliance_failure_count: 법규 또는 운영 리스크 발생 건수.

        Returns:
            LossScoreResult 객체 - 총 점수와 상세 Breakdown 포함.
        """
        breakdown = []
        total_score = 0.0

        # 1. 시간 손실 계산 (Time Loss)
        time_loss_amount = time_spent_hours * self.TIME_LOSS_RATE
        breakdown.append(LossBreakdownItem(
            category="TimeLoss",
            description=f"총 {time_spent_hours:.2f}시간의 비효율적 시간 사용으로 인한 기회비용 손실.",
            raw_value=time_spent_hours,
            weight=self.TIME_LOSS_RATE,
            calculated_loss=time_loss_amount
        ))
        total_score += time_loss_amount

        # 2. 데이터 편향 리스크 계산 (Data Bias Risk)
        data_bias_loss = data_bias_risk_score * self.DEFAULT_RISK_MULTIPLIER * 1000 # 가중치 적용 및 스케일링
        breakdown.append(LossBreakdownItem(
            category="DataBiasRisk",
            description="데이터 편향으로 인해 잘못된 비즈니스 의사결정이 내려질 확률 (가정).",
            raw_value=data_bias_risk_score,
            weight=self.DEFAULT_RISK_MULTIPLIER * 1000,
            calculated_loss=data_bias_loss
        ))
        total_score += data_bias_loss

        # 3. 법규/운영 리스크 계산 (Compliance Risk)
        compliance_loss = compliance_failure_count * 5000 # 건당 고정 패널티 적용
        breakdown.append(LossBreakdownItem(
            category="ComplianceRisk",
            description=f"{compliance_failure_count}건의 운영 미흡/법규 위반으로 인한 잠재적 벌금 리스크.",
            raw_value=float(compliance_failure_count),
            weight=5000,
            calculated_loss=compliance_loss
        ))
        total_score += compliance_loss

        # 최종 결과 반환
        return LossScoreResult(
            total_score=round(total_score, 2),
            breakdown=breakdown,
            summary_message=f"총 예상 손실액은 ${round(total_score, 2)}입니다. 즉각적인 데이터 무결성 점검이 필요합니다."
        )

# --- 3. 단위 테스트 예시 (Unit Test Example - 필수 검증) ---
def run_unit_test():
    """서비스 클래스의 핵심 로직을 검증하는 함수."""
    print("="*50)
    print("⚙️ [UNIT TEST] LossCalculatorService 실행 중...")
    calculator = LossCalculatorService()

    # Case 1: 표준 테스트 케이스 (모든 리스크 존재)
    test_result = calculator.calculate_loss(
        time_spent_hours=5,          # 시간 손실: $275
        data_bias_risk_score=0.8,    # 데이터 편향: 0.8 * Multiplier * 1000
        compliance_failure_count=2   # 법규 리스크: 2 * 5000 = $10000
    )

    expected_min_score = 275 + (0.8 * 1.5 * 1000) + 10000 # 최소 점수 예측
    print(f"✅ 테스트 실행 완료. 총 예상 손실액: ${test_result.total_score:.2f}")

    # 실제 계산된 값이 기대 범위 내에 있는지 검증하는 로직을 추가해야 함 (실제 테스트 프레임워크 사용 권장)
    if test_result.total_score > 12000 and test_result.breakdown:
        print(f"✅ Breakdown 항목 개수 확인 완료: {len(test_result.breakdown)}개.")
        # 첫 번째 breakdown의 데이터 타입까지 검증하는 코드를 추가할 수 있음
    else:
        print("⚠️ 테스트 경고: 예상되는 손실 점수 범위를 벗어났을 수 있습니다. 로직 재검토 필요.")

if __name__ == "__main__":
    run_unit_test()
print("="*50)