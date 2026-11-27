from fastapi import FastAPI, HTTPException
from api.schemas.models import LossInput, LossResult
from api.services.loss_calculator import LossCalculatorService
import os

# FastAPI 인스턴스 초기화 (메인 진입점)
app = FastAPI(title="고고플랙스 손실 점수 계산 API", version="1.0.0")

@app.post("/v1/calculate-loss", response_model=LossResult, summary="손실 점수를 계산하고 상세 내역을 반환합니다.")
async def calculate_loss_endpoint(input_data: LossInput):
    """
    사용자가 제공한 근무 시간 및 자산 정보를 바탕으로 손실 점수를 계산합니다. 
    반드시 상세 Breakdown과 함께 결과를 반환하여 신뢰도를 확보해야 합니다.
    """
    try:
        # 1. 서비스 초기화 (client_id는 실제 사용자 인증 과정에서 가져와야 함)
        client_id = "user_" + str(hash(input_data.model_dump_json()))[-8:] # 임시 ID 생성
        service = LossCalculatorService(client_id=client_id)

        # 2. 로직 실행 및 결과 받기
        calculation_result = service.calculate_loss(input_data.dict())

        # 3. Pydantic 스키마에 맞게 최종 구조화하여 반환 (타입 강제)
        detailed_breakdown_list = []
        for item in calculation_result['detailed_breakdown']:
            detailed_breakdown_list.append(BreakdownItem(
                category=item['category'], 
                metric=item['metric'], 
                value=item['value'], 
                weight=item['weight']
            ))

        return LossResult(
            calculation_id=calculation_result['calculation_id'],
            client_id=calculation_result['client_id'],
            total_loss_score=calculation_result['total_loss_score'],
            detailed_breakdown=detailed_breakdown_list,
            analysis_status=calculation_result['analysis_status']
        )

    except Exception as e:
        print(f"API 처리 중 오류 발생: {e}")
        raise HTTPException(status_code=500, detail="손실 계산 API 처리에 실패했습니다. 로직을 검토해주세요.")