from pydantic import BaseModel, Field, PositiveFloat
from typing import Dict, Any

class LossInputData(BaseModel):
    """
    스코어카드 진단을 위해 사용자로부터 입력받는 핵심 데이터 모델.
    모든 필드는 누락되거나 유효하지 않으면 Pydantic에서 에러를 발생시킵니다.
    [근거: CEO 지시 - API 입력 유효성 검증]
    """
    # 사용자의 기본적인 비즈니스 개요 (필수)
    company_name: str = Field(..., min_length=3, description="진단 대상 기업의 이름")
    industry: str = Field(..., max_length=50, description="산업 분류 코드 또는 명칭")

    # 데이터 손실 위험 관련 핵심 지표 (필수)
    current_user_count: PositiveFloat = Field(..., ge=1, description="현재 활성 사용자 수. 0은 안 됨.")
    average_conversion_rate: float = Field(..., gt=0, le=1, description="평균 전환율 (0 < rate <= 1).")

    # 위험 요소를 정량화하기 위한 추가 데이터 (선택적이지만 권장)
    data_retention_days: int | None = Field(None, ge=1, description="데이터 유지 기간 (일).")
    api_call_frequency: PositiveFloat | None = Field(None, gt=0, description="API 호출 빈도 (횟수/시간).")

class ScorecardDiagnosisRequest(BaseModel):
    """
    진단 실행을 위한 모든 요청 바디를 묶는 최상위 Request 모델.
    """
    user_id: str = Field(..., description="요청 사용자 고유 ID.")
    input_data: LossInputData # 상위 데이터 객체를 포함

class ScorecardDiagnosisResponse(BaseModel):
    """
    API가 성공적으로 계산하여 반환해야 할 최종 응답 모델.
    [근거: Designer Design System (v1.0)의 결과 구조]
    """
    score_value: float = Field(..., ge=0, le=100, description="데이터 무결성 점수 (0~100).")
    estimated_loss_amount: PositiveFloat = Field(..., gt=0, description="예상되는 재정적 손실액 ($).")
    risk_level: str = Field(..., description="위험 수준 ('Low', 'Medium', 'High').")
    breakdown: Dict[str, Any] = Field(..., description="손실 발생 요인별 세부 분석 (파이 차트 데이터 등).")