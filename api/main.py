from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import time

app = FastAPI(title="Data Integrity Scorecard API")

# --- Pydantic Models for Data Contract ---
class DiagnosisRequest(BaseModel):
    """클라이언트가 진단에 필요한 핵심 데이터를 전송하는 스키마."""
    data_silos_count: int = 0 # 데이터 사일로 시스템 수 (예: CRM, ERP 등)
    manual_process_points: int = 0 # 자동화되지 않은 수동 작업 포인트 수
    api_connection_gaps: int = 0 # API 연결이 누락된 핵심 서비스 간의 개수

class DiagnosisResult(BaseModel):
    """진단 결과로 반환되는 스코어카드 데이터 구조."""
    score: float # 최종 무결성 점수 (0.0 ~ 100.0)
    risk_level: str # 리스크 레벨 (LOW, MEDIUM, HIGH, CRITICAL)
    estimated_loss_potential: dict # 예상 손실 상세 분석
    vulnerability_report: list # 발견된 취약성 목록

@app.post("/api/v1/diagnose_data", response_model=DiagnosisResult)
async def diagnose_data(request: DiagnosisRequest):
    """
    클라이언트가 입력한 데이터를 기반으로 데이터 무결성을 진단하고 점수와 손실을 계산합니다.
    [진단 로직: 더미 구현] - 실제 비즈니스 로직이 들어갈 자리입니다.
    """
    # 1. 가중치 부여 및 리스크 계산 (더미 로직)
    base_risk = (request.data_silos_count * 20) + \
                (request.manual_process_points * 15) + \
                (request.api_connection_gaps * 30)

    # 리스크가 클수록 점수는 낮고, 예상 손실은 커집니다. (예시 공식)
    score = max(0.0, 100.0 - base_risk)
    loss_potential_estimate = round((base_risk * 55 / 10), 2) # $55/hour 기준
    
    # 2. 결과 구조화
    if score < 30:
        risk_level = "CRITICAL"
    elif score < 60:
        risk_level = "HIGH"
    elif score < 85:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # 3. 취약성 보고서 생성 (더미 데이터)
    vulnerability_report = [
        {"source": "데이터 사일로", "severity": "High", "description": f"{request.data_silos_count}개 이상의 시스템 간의 비연동성 확인."},
        {"source": "수동 프로세스", "severity": "Medium", "description": f"{request.manual_process_points}건의 수작업 입력 지점이 데이터 오류를 유발할 가능성이 높음."}
    ]

    # 4. 최종 결과 반환 (API 계약 준수)
    return DiagnosisResult(
        score=round(score, 2),
        risk_level=risk_level,
        estimated_loss_potential={"annual": round(loss_potential_estimate * 10, 0), "daily": round(loss_potential_estimate * 1.5, 0)},
        vulnerability_report=vulnerability_report
    )

# 테스트용 루트 경로 (API 작동 확인 목적)
@app.get("/")
def read_root():
    return {"status": "Data Integrity Scorecard API is running successfully."}