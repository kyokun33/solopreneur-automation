from fastapi import FastAPI, HTTPException
from starlette import status
from typing import List

# 스키마 임포트 (방금 만든 파일)
from .schema import LossDataSetSubmission, LossPotentialEntry, PredictionData 

app = FastAPI(title="Gogoflacks Loss Potential API", version="1.0.0")

@app.post("/api/v1/submit_loss_potential", status_code=status.HTTP_201_CREATED)
async def submit_data(submission: LossDataSetSubmission):
    """
    새로운 잠재적 손실 데이터를 수신하고 유효성을 검사합니다.

    Args:
        submission: LossPotentialEntry 리스트를 포함하는 전체 데이터셋 구조체.

    Returns:
        성공적으로 처리된 데이터 목록 및 메시지.
    Raises:
        HTTPException: 입력 데이터가 스키마 또는 비즈니스 로직에 위배될 경우.
    """
    if not submission.entries:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="제출할 잠재적 손실 데이터를 최소 1개 이상 포함해야 합니다.")

    processed_entries = []
    total_loss_sum = 0.0 # 임시 합산 값 (비즈니스 로직 예시)

    # 개별 엔트리 반복 검증 및 처리
    for i, entry in enumerate(submission.entries):
        try:
            # 1. 비즈니스 유효성 검사 추가 (Example: 손실 유형이 너무 많으면 경고)
            if len(entry.loss_types) > 3:
                print(f"⚠️ Warning on Entry {i}: Too many loss types listed ({len(entry.loss_types)}). Review scope.")

            # 2. Mock DB 저장 및 합산 (실제 로직 대체)
            processed_entries.append(entry.dict())
            
            # 간단한 손실 총합 계산 시뮬레이션 (가장 큰 예측값을 기준으로 함)
            if entry.prediction_data:
                try:
                    # 실제로는 복잡한 가중치 계산이 들어가야 하지만, 여기서는 첫 번째 값을 사용한다고 가정
                    value = float(entry.prediction_data[0].raw_value.replace(',', ''))
                    total_loss_sum += value
                except ValueError:
                     print(f"⚠️ Warning on Entry {i}: Could not convert '{entry.prediction_data[0].raw_value}' to float for summation.")


        except Exception as e:
            # 엔트리 단위의 오류 처리
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                                detail=f"Entry {i} ({entry.entry_id}) 처리 중 치명적 오류 발생: {str(e)}")

    # 성공 응답
    return {
        "message": "✅ 잠재 손실 데이터셋 수신 및 유효성 검증 완료. 시스템에 정상적으로 저장되었습니다.",
        "status": "SUCCESS",
        "processed_count": len(processed_entries),
        "total_estimated_loss_simulation": round(total_loss_sum, 2) # 총합계를 반환하여 활용도를 높임
    }

@app.get("/api/v1/status")
async def get_status():
    return {"system_status": "Operational", "last_update": "N/A"}