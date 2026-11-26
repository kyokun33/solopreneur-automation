import json
from typing import Dict, Any, Tuple

# [근거: Researcher가 제공한 스키마]
SCHEMA_PATH = "KnowledgeBase/LossPotentialData_API_Schema_v1.json" 

def load_schema(path: str) -> dict:
    """스키마 파일을 로드하고 기본 검증을 수행합니다."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ ERROR: 스키마 파일 경로를 찾을 수 없습니다.")
        # API 호출 실패 시나리오 1: 파일 부재
        return {}

def validate_and_process_data(raw_input: Dict[str, Any]) -> Tuple[bool, str, dict]:
    """
    입력 데이터를 스키마에 맞춰 검증하고, 손실 예측 계산을 준비합니다.
    @param raw_input: 외부에서 받은 원시 데이터 딕셔너리 (API Payload 가정)
    @return: (성공 여부, 메시지, 처리된 데이터)
    """
    schema = load_schema(SCHEMA_PATH)
    if not schema or "data_variables" not in schema:
        return False, "시스템 초기화 오류: 유효한 스키마를 로드할 수 없습니다.", {}

    processed_data = {"time": 0.0, "revenue": 0.0, "risk": 0.0}
    
    # 1. 데이터 존재 여부 및 타입 검증 (Malformed Data Edge Case)
    try:
        for var in schema["data_variables"]:
            var_id = var["variable_id"]
            if var_id not in raw_input or raw_input[var_id] is None:
                return False, f"데이터 오류: 필수 변수 '{var['name']}' ({var_id})가 누락되었습니다.", {}

        # 2. 데이터 타입 및 범위 검증 (Schema Compliance)
        if not isinstance(raw_input["V_TIME_LOSS"], (int, float)):
            return False, "데이터 오류: V_TIME_LOSS는 숫자형이어야 합니다.", {}
        processed_data["time"] = raw_input["V_TIME_LOSS"]

        if not isinstance(raw_input["V_REVENUE_LOSS"], (int, float)):
            return False, "데이터 오류: V_REVENUE_LOSS는 숫자형이어야 합니다.", {}
        processed_data["revenue"] = raw_input["V_REVENUE_LOSS"]

    except Exception as e:
        # 예상치 못한 파싱 에러 처리 (General Edge Case)
        return False, f"처리 중 예외 발생: 데이터 구조를 검증하는 과정에서 오류가 발생했습니다. ({str(e)})", {}


    # 3. 핵심 손실 예측 로직 실행 (Business Logic)
    try:
        # V_TIME_LOSS는 시간당 비용으로 가정하고, 최종적으로 총 예상 손실액을 계산합니다.
        total_loss = processed_data["time"] * 1.5 + processed_data["revenue"] * 0.02
        processed_data["risk"] = raw_input.get("V_RISK_COST", 0.0) # 리스크 비용은 누락 가능성 대비
        processed_data["final_loss_potential"] = round(total_loss + processed_data["risk"], 2)
        return True, "데이터 검증 및 계산 성공: 손실 잠재력이 계산되었습니다.", processed_data

    except Exception as e:
        # 로직 실행 실패 시나리오 (Unexpected Logic Failure Edge Case)
        return False, f"로직 처리 오류: 핵심 비즈니스 로직을 수행하는 중 예외가 발생했습니다. ({str(e)})", {}


def run_end_to_end_test_scenario(input_payload: Dict[str, Any]):
    """전체 E2E 테스트 흐름을 시뮬레이션하고 결과를 출력합니다."""
    print("\n=============================================")
    print("📈 [SYSTEM TEST] End-to-End Loss Potential 검증 시작")
    print("=============================================")

    success, message, result = validate_and_process_data(input_payload)

    if success:
        print(f"✅ 테스트 통과: {message}")
        # 이 결과가 Widget/Chart에 전달되어야 함.
        return {"status": "SUCCESS", "loss_potential": result["final_loss_potential"]}
    else:
        print(f"❌ 테스트 실패 (Edge Case Triggered): {message}")
        # 에러 메시지와 함께 시스템이 멈추지 않고 로그를 반환하는 것이 중요함.
        return {"status": "FAILURE", "error_message": message}


# --- 테스트 실행 블록 (테스트 케이스 정의) ---

if __name__ == "__main__":
    print("--- Test Case 1: Happy Path (정상 작동 시나리오) ---")
    happy_path_data = {
        "V_TIME_LOSS": 50.0, # 예시 데이터
        "V_REVENUE_LOSS": 2000.0, # 예시 데이터
        "V_RISK_COST": 150.0  # 예시 데이터
    }
    run_end_to_end_test_scenario(happy_path_data)

    print("\n\n--- Test Case 2: Malformed Data (필수 변수 누락 Edge Case) ---")
    missing_variable_data = {
        "V_TIME_LOSS": 50.0,
        # "V_REVENUE_LOSS"가 없음 -> 실패 유도
        "V_RISK_COST": 150.0
    }
    run_end_to_end_test_scenario(missing_variable_data)

    print("\n\n--- Test Case 3: Type Error (데이터 타입 오류 Edge Case) ---")
    type_error_data = {
        "V_TIME_LOSS": "fifty", # 문자열을 넣어서 실패 유도
        "V_REVENUE_LOSS": 2000.0,
        "V_RISK_COST": 150.0
    }
    run_end_to_end_test_scenario(type_error_data)

# 이 코드는 실제 시스템의 핵심 안정성 검증 로직이 될 것입니다.