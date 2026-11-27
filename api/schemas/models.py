from pydantic import BaseModel, Field
from typing import List, Dict, Any

# FastAPI 요청 본문 스키마 정의 (입력 데이터 유효성 검증)
class LossInput(BaseModel):
    """LossCalculatorService에 전달될 입력값의 구조를 정의합니다."""
    working_hours: float = Field(..., description="사용자의 추정 근무 시간 (시간 단위).")
    hourly_loss_rate: float = Field(default=55.0, description="시간당 예상 손실 비용 ($).")
    data_integrity_risk_percent: float = Field(..., gt=0, le=100, description="데이터 무결성 리스크 (%) (0~100).")
    total_assets: float = Field(default=100000.0, description="총 자산 가치 ($).")

# FastAPI 응답 본문 스키마 정의 (출력 데이터 구조 확정)
class BreakdownItem(BaseModel):
    """손실 점수 상세 내역 하나의 구조."""
    category: str
    metric: str
    value: float
    weight: float

class LossResult(BaseModel):
    """최종 손실 계산 결과의 전체 구조를 정의합니다."""
    calculation_id: str = Field(description="이번 분석 세션에 대한 고유 ID.")
    client_id: str
    total_loss_score: float = Field(description="총합계된 손실 점수 (가장 중요).")
    detailed_breakdown: List[BreakdownItem] = Field(description="각 항목별 상세 계산 과정 리스트.")
    analysis_status: str # 예: CRITICAL_LOSS_DETECTED