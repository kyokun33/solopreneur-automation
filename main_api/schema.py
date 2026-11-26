from typing import List, Optional
from pydantic import BaseModel, Field, validator
import re

class LossType(str):
    """손실 유형 정의: T (시간), V (가치 하락), R (리스크 비용)"""
    TIME = "T"
    VALUE_DECLINE = "V"
    RISK_COST = "R"

class PredictionData(BaseModel):
    """구체적인 손실 금액 또는 비율 데이터를 담는 모델"""
    # '1억 5천만원'과 같은 자연어 형태도 받을 수 있도록 문자열로 받고, 내부에서 변환할 여지를 남김.
    raw_value: str = Field(..., description="정량화된 값 (예: 150,000,000원 또는 20%)")
    is_percentage: bool = Field(False, description="값이 백분율인지 여부.")

class LossPotentialEntry(BaseModel):
    """잠재 손실액 데이터의 단일 엔트리 스키마"""
    # 필수 필드 (데이터를 특정할 수 있게 함)
    entry_id: str = Field(..., description="고유 식별자 (UUID 권장)")
    industry: str = Field(..., min_length=3, max_length=50, description="분석된 산업군 (예: 제조업, 병원/의료)")
    pain_point: str = Field(..., description="핵심 페인 포인트 정의")

    # 손실 유형 및 계산 모델 (논리적 구조화)
    loss_types: List[LossType] = Field(..., description="관련된 모든 손실 유형 리스트.")
    calculation_model: str = Field(..., description="손실액 산출에 사용된 공식 또는 논리 (예: T*V + R)")

    # 정량화 데이터 (핵심)
    prediction_data: List[PredictionData] = Field(..., min_length=1, description="산출 근거가 되는 구체적인 수치 목록.")

    # 출처 및 검증 (신뢰도 확보)
    source_verification: str = Field(..., description="데이터의 근거 자료 (예: 고용노동부 통계 / 고객사 인터뷰)")


    @validator('entry_id')
    def check_id_format(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("Entry ID는 알파벳, 숫자, 하이픈(-)만 포함해야 합니다.")
        return v

    @validator('industry')
    def check_industry_length(cls, v):
        if not v:
             raise ValueError("산업군은 필수 항목입니다.")
        return v

# 전체 데이터셋을 담는 모델 (API 요청 바디용)
class LossDataSetSubmission(BaseModel):
    """최종적으로 API가 받을 수 있는 손실 잠재력 데이터 배열."""
    entries: List[LossPotentialEntry] = Field(..., description="검증을 요청할 Loss Potential Entry들의 리스트.")

# -------------------------------------------------
# [Mock DB 시뮬레이션] - 실제로는 이 데이터를 저장합니다.
MOCK_DATABASE = {}