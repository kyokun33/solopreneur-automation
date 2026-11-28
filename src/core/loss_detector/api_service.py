# src/core/loss_detector/api_service.py
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- 1. 데이터 모델 정의 (Pydantic) ---

class LossDataPoint(BaseModel):
    """손실 점검을 위한 단일 시점의 데이터 포인트를 정의합니다."""
    timestamp: float  # Unix Timestamp (seconds)
    total_loss: float # 누적 손실액 ($)
    current_loss_rate: float # 현재 시간당 손실률 ($/hour)

class PanicStateResponse(BaseModel):
    """API 호출 결과 응답 모델."""
    is_panic_state: bool = False
    message: str
    trigger_details: dict = {}


# --- 2. LossDetector 핵심 비즈니스 로직 (SRP 준수) ---

class LossDetector:
    """Loss Scorecard의 Peak Panic State를 감지하는 Detector 클래스."""
    
    THRESHOLD_LOSS: float = 1500.0 # 임계점 ($1,500)
    SPIKE_TIME_WINDOW: float = 30.0 # 스파이크 비교 시간 (초)
    SPIKE_MIN_INCREASE_RATE: float = 0.25 # 최소 증가율 (25%)

    @staticmethod
    def detect_panic(data_points: List[LossDataPoint]) -> PanicStateResponse:
        """
        전체 데이터 포인트 리스트를 분석하여 Peak Panic State를 감지합니다.
        가장 최근의 데이터 포인트를 기준으로 로직을 수행합니다.
        """
        if not data_points or len(data_points) < 2:
            return PanicStateResponse(is_panic_state=False, message="Insufficient data points for analysis.")

        # 가장 최신 데이터를 가져옵니다. (시간순으로 정렬되었다고 가정)
        latest_point = data_points[-1]
        
        # 1. 임계점 도달 검사 (Threshold Check)
        is_above_threshold = latest_point.total_loss >= LossDetector.THRESHOLD_LOSS

        # 2. 손실 급증(Spike) 감지 로직
        spike_detected: bool = False
        comparison_window_start_time = latest_point.timestamp - LossDetector.SPIKE_TIME_WINDOW

        # 비교 가능한 가장 오래된 데이터 포인트를 찾습니다.
        oldest_comparable_point = next((p for p in data_points if p.timestamp >= comparison_window_start_time), None)

        if oldest_comparable_point:
            # 시간당 손실률의 비교
            rate_increase = latest_point.current_loss_rate - oldest_comparable_point.current_loss_rate
            min_required_increase = oldest_comparable_point.current_loss_rate * LossDetector.SPIKE_MIN_INCREASE_RATE

            if rate_increase > min_required_increase and latest_point.timestamp - oldest_comparable_point.timestamp <= LossDetector.SPIKE_TIME_WINDOW:
                spike_detected = True
        
        # 최종 판정: 두 조건 모두 충족해야 'Peak Panic State'로 정의합니다.
        is_panic_state = is_above_threshold and spike_detected

        message = "🚨 Peak Panic State Detected! Immediate action required." if is_panic_state else "✅ System stable or warning level only."

        return PanicStateResponse(
            is_panic_state=is_panic_state,
            message=message,
            trigger_details={
                "threshold_met": is_above_threshold,
                "spike_detected": spike_detected,
                "current_loss": latest_point.total_loss,
                "latest_rate": latest_point.current_loss_rate
            }
        )


# --- 3. FastAPI 엔드포인트 구축 (API Gateway 역할) ---

app = FastAPI(title="Loss Scorecard Panic State Detector API")

@app.post("/api/v1/check_panic_state", response_model=PanicStateResponse)
async def check_state_endpoint(data: List[LossDataPoint]):
    """
    전달받은 시계열 데이터 포인트를 분석하여 Peak Panic State를 감지합니다.
    이 엔드포인트는 외부 시스템 (Frontend, Scheduler 등)에서 호출되어야 합니다.
    """
    print("--- API Call Received: Analyzing Loss Data ---")
    # 로직을 Detector 클래스에 위임하여 테스트 용이성을 높입니다.
    response = LossDetector.detect_panic(data)
    return response

# 참고: 실행 명령어는 'uvicorn src.core.loss_detector.api_service:app --reload' 입니다.