from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time

# --- API Contract Definition (Input/Output) ---

class UserData(BaseModel):
    """진단에 필요한 최소한의 사용자 데이터 입력 모델."""
    company_name: str
    data_integrity_score: float  # 0.0 ~ 1.0 사이 점수
    regulatory_compliance_level: int # 1 (Low) ~ 5 (High)

class RiskDiagnosis(BaseModel):
    """진단 결과 및 상태 전이를 담는 출력 모델."""
    status: str # e.g., AWARENESS, WARNING, CRITICAL, READY_TO_BUY
    loss_scorecard: dict # {'total': float, 'breakdown': list}
    anti_loss_message: str
    next_cta_state: str

# --- State Machine Logic & Service Layer ---

app = FastAPI(title="Loss Scorecard API")

def calculate_risk_score(data: UserData) -> tuple[float, dict]:
    """
    데이터 기반으로 잠재적 손실 점수와 세부 Breakdown을 계산하는 핵심 로직.
    이 함수는 외부 규제/시장 데이터 피드에 의존한다고 가정합니다.
    """
    # 가상의 복잡한 리스크 산정 공식 (예: (1 - score) * compliance_penalty * time_factor)
    base_risk = 1.0 - data.data_integrity_score
    compliance_multiplier = 1.5 if data.regulatory_compliance_level < 3 else 1.0
    
    # 손실 점수 계산 (단위: $K, 예시로 $ 단위 사용)
    loss_total = max(10000.0, base_risk * compliance_multiplier * 2500000) # 최소 $10k 보장

    breakdown = [
        {"type": "Data Integrity Risk", "amount": loss_total * (base_risk * 0.7)},
        {"type": "Regulatory Gap Risk", "amount": loss_total * ((3 - data.regulatory_compliance_level) / 2.0 * 0.3)}
    ]
    
    return round(loss_total, 2), breakdown

def determine_state_and_message(score: float, breakdown: list) -> tuple[str, str]:
    """
    Loss Scorecard State Machine V2.0에 따른 상태 결정 및 카피라이팅 생성.
    $5K~$2M+ 리스크 데이터를 활용하여 위기감 극대화.
    """
    if score >= 100000: # $100k 이상 (Critical)
        state = "CRITICAL"
        message = f"🚨 경고! 현재의 미진단 상태는 {score:,.2f} 규모의 즉각적인 법적 리스크에 노출되어 있습니다. 지금 조치를 취하지 않으면 사업이 중단될 수 있습니다."
    elif score >= 5000: # $5k 이상 (Warning)
        state = "WARNING"
        message = f"⚠️ 잠재적 위험 경고. 현재 데이터 무결성 문제로 인해 최소 {score:,.2f} 규모의 재정적 손실이 예상됩니다. 진단이 필수입니다."
    else: # $5k 미만 (Awareness)
        state = "AWARENESS"
        message = f"🔍 기본적인 리스크 노출은 확인되었으나, 심층적인 구조 분석이 필요합니다. 전체 생존을 위해 전문 진단을 받으세요."

    return state, message


@app.post("/api/diagnose_risk", response_model=RiskDiagnosis)
async def diagnose_risk(user_data: UserData):
    """
    사용자 입력 데이터를 받아 리스크 점수를 계산하고, 상태 머신에 따라 최적의 Anti-Loss 메시지를 반환합니다.
    Mini-Commitment Loop가 시작되는 지점입니다.
    """
    try:
        # 1. 리스크 산정 (Core Logic)
        loss_total, breakdown = calculate_risk_score(user_data)
        
        # 2. 상태 결정 및 메시지 생성 (State Machine V2.0)
        state, message = determine_state_and_message(loss_total, breakdown)

        diagnosis_result = RiskDiagnosis(
            status=state,
            loss_scorecard={"total": loss_total, "breakdown": breakdown},
            anti_loss_message=message,
            next_cta_state="Purchase_Funnel_Entry" if state in ["CRITICAL", "WARNING"] else "Information_Gathering"
        )
        return diagnosis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"진단 과정에서 내부 오류 발생: {str(e)}")

# --- Root Endpoint (Health Check) ---
@app.get("/")
def read_root():
    return {"message": "Loss Scorecard API is operational. Ready for diagnosis."}