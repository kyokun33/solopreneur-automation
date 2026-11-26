from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np
from typing import List, Dict

# --- Pydantic Schema 정의 (데이터 무결성 및 유효성 검증) ---
class DataPoint(BaseModel):
    """단일 데이터 포인트의 구조를 정의합니다. (예: 시간/리스크 레벨)"""
    time_period: str = Field(..., description="시간 구간 (e.g., T+1 year)")
    risk_score: float = Field(..., ge=0.0, le=100.0, description="데이터 리스크 스코어 (0-100)")
    data_availability: bool = Field(..., description="데이터가 실제로 존재하는지 여부")

class LossInputData(BaseModel):
    """전체 손실 분석에 필요한 입력 데이터 셋."""
    data_points: List[DataPoint]
    base_hourly_loss_rate: float = Field(..., ge=0.0, description="기본 시간당 예상 손실률 (USD/hour)")

app = FastAPI(title="GogoFlex Data Integrity API")

# --- 비즈니스 로직: 손실 정량화 함수 ---
def calculate_total_loss(data_points: List[DataPoint], hourly_rate: float) -> Dict:
    """
    입력 데이터셋을 기반으로 총 예상 손실액 및 스코어를 계산합니다.
    손실은 '데이터 결핍'에 비례하여 가중치를 부여합니다.
    """
    total_risk_score = 0.0
    weighted_loss_components: Dict[str, float] = {}

    for point in data_points:
        # 1. 데이터 존재 여부 기반 손실 가중치 계산 (핵심 로직)
        if not point.data_availability:
            # 데이터가 없는 경우, 리스크 점수와 시간 비율을 곱해 높은 패널티 부여
            loss_weight = (point.risk_score / 100.0) * 5.0 # 최대 5배 가중치
        else:
            loss_weight = 0.0

        # 2. 누적 리스크 스코어 계산
        total_risk_score += point.risk_score

        # 3. 개별 손실 컴포넌트 기록
        component_name = f"{point.time_period}_Loss"
        weighted_loss_components[component_name] = (
            hourly_rate * loss_weight * 10 # 임의 상수: 시간당 비용 * 가중치 * 기간 보정 상수
        )

    # 총 손실액 계산 (간단화된 합산 방식)
    total_estimated_loss = sum(weighted_loss_components.values())
    final_score = max(0, 100 - total_risk_score / len(data_points)) # 리스크 점수가 높을수록 스코어 하락

    return {
        "total_estimated_loss": round(total_estimated_loss, 2),
        "final_integrity_score": round(min(100.0, max(0.0, final_score)), 2),
        "breakdown": weighted_loss_components
    }

@app.post("/api/v1/calculate_loss")
async def calculate_loss_endpoint(input_data: LossInputData):
    """손실 분석 API 엔드포인트."""
    try:
        result = calculate_total_loss(
            [DataPoint(**d) for d in input_data.data_points], 
            input_data.base_hourly_loss_rate
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation Error: {str(e)}")

# --- 테스트용 초기 데이터 (Mocking the input data structure) ---
@app.get("/api/v1/mock_data")
async def get_mock_data():
    """API 테스트를 위한 Mock 데이터를 제공합니다."""
    return {
        "base_hourly_loss_rate": 55.0, # Self-RAG 근거: $55/hour 고정값
        "data_points": [
            {"time_period": "T+1 year", "risk_score": 20.0, "data_availability": True},
            {"time_period": "T+3 years", "risk_score": 85.0, "data_availability": False}, # High Risk/Missing Data Point
            {"time_period": "T+5 years", "risk_score": 45.0, "data_availability": True}
        ]
    }