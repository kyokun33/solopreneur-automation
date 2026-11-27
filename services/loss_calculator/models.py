from dataclasses import dataclass
from typing import List, Optional

@dataclass
class LossAssessment:
    """단일 리스크 영역의 평가 결과."""
    risk_type: str          # 예: "Financial", "IP Similarity"
    score: float            # 0.0 ~ 1.0 사이의 점수 (1.0이 최고 위험)
    estimated_loss_usd: float # 예상 손실 금액 ($)
    severity_level: str     # LOW, MODERATE, CRITICAL

@dataclass
class CalculationInput:
    """Loss Engine에 필요한 모든 입력 파라미터."""
    user_time_hours: Optional[float] = None  # 사용 시간 (가장 기본적 지표)
    potential_revenue_usd: Optional[float] = None # 최대 잠재 수익
    ip_asset_name: Optional[str] = None      # 진단 대상 IP 자산명
    comparison_assets: List[str] = None       # 비교 분석할 경쟁/유사 자산 목록
    user_data_integrity_score: Optional[float] = None # 데이터 무결성 점수 (0.0 ~ 1.0)

@dataclass
class TotalLossReport:
    """전체 진단 보고서의 최종 결과물."""
    total_loss_score: float     # 종합 리스크 점수
    total_estimated_loss_usd: float # 총 예상 손실 금액
    detailed_assessments: List[LossAssessment] # 개별 평가 목록
    is_calculation_successful: bool = True