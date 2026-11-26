import pytest
from fastapi.testclient import TestClient
# src/api/schemas.py에서 정의된 스키마를 가정하고 임포트합니다.
# 실제 프로젝트에서는 이 경로가 정확해야 합니다.
from src.api.schemas import ScorecardDiagnosisRequest, LossInputData

# Mock API Client Setup (실제 라우터와 연동될 클라이언트 객체)
client = TestClient("http://testserver") 

def test_successful_diagnosis_happy_path():
    """[1/3] 테스트 케이스: 모든 입력이 유효하며, 정상적인 스코어카드 진단 결과가 반환되는 경우."""
    # Happy Path 예시 데이터 (모든 값이 유효해야 함)
    valid_data = LossInputData(
        company_name="고고플랙스", 
        industry="AI SaaS", 
        current_user_count=150.0, 
        average_conversion_rate=0.03,
        data_retention_days=90,
        api_call_frequency=12.5
    )
    request_body = {"user_id": "test-user-1", "input_data": valid_data}

    # 🚨 실제 API 호출 (이 부분이 테스트의 핵심입니다.)
    response = client.post("/api/v1/diagnosis", json=request_body)

    assert response.status_code == 200 # 성공 코드 확인
    data = response.json()
    assert "score_value" in data # 필수 필드 존재 여부
    # 손실액이 0보다 크다는 비즈니스 로직 검증까지 포함해야 함.
    assert data["estimated_loss_amount"] > 0.0

@pytest.mark.parametrize("invalid_input, expected_status", [
    # 🚨 데이터 유효성 실패 경로 테스트 (Pydantic Validation Fail)
    ({"user_id": "test-fail", "input_data": {"company_name": "", "industry": "Test", "current_user_count": -5.0, "average_conversion_rate": 1.5}}, 422), # 사용자 수 음수, 전환율 초과
    ({"user_id": "test-fail", "input_data": {"company_name": "TooShort", "industry": "", "current_user_count": 0.0, "average_conversion_rate": 0.01}}), # 사용자 수 0, 산업명 누락
    # 추가적인 모든 실패 케이스가 여기에 와야 합니다.
])
def test_validation_failure_path(invalid_input: dict, expected_status: int):
    """[2/3] 테스트 케이스: Pydantic 유효성 검사 실패 시, 정확한 422 응답과 에러 상세 메시지가 반환되는지 확인."""
    # FastAPI는 보통 422를 반환하며, response.json()에서 'detail' 키에 오류 목록이 담깁니다.
    response = client.post("/api/v1/diagnosis", json=invalid_input)

    assert response.status_code == expected_status # 예상된 에러 코드와 일치하는지 확인
    # 응답 본문에 어떤 필드가 왜 실패했는지 상세 정보가 있는지 검증
    assert "detail" in response.json() and isinstance(response.json()["detail"], list)

def test_business_logic_edge_case():
    """[3/3] 테스트 케이스: 데이터는 유효하지만, 비즈니스 로직상 예외적인 상황을 처리하는지 확인 (예: 낮은 활성 사용자 수)."""
    # 사용자가 거의 없고, API 호출도 전무한 극단적 시나리오. 시스템은 패닉하지 않고 '위험' 경고와 함께 적정 가이드를 제공해야 함.
    edge_case_data = LossInputData(
        company_name="스타트업A", 
        industry="서비스 기획", 
        current_user_count=1.0, # 최소값
        average_conversion_rate=0.001,
        data_retention_days=30,
        api_call_frequency=0.1
    )
    request_body = {"user_id": "edge-case", "input_data": edge_case_data}

    response = client.post("/api/v1/diagnosis", json=request_body)

    assert response.status_code == 200 # 여전히 성공적으로 응답해야 함 (단지 경고 메시지가 포함될 뿐)
    data = response.json()
    # 비즈니스 로직에 의해 risk_level이 'High'로 설정되는지 확인하는 등 구체적 검증 필요
    assert data["risk_level"] == "High"