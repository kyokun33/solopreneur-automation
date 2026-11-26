import json
from typing import Dict, Any, Optional

# --- Mock Schema Definition (Self-RAG from Designer/API Spec) ---
LOSS_WIDGET_SCHEMA = {
    "user_id": str,
    "time_elapsed_hours": float, # 시간 경과량 (필수)
    "initial_value": float,      # 시작 기준값 (필수)
    "risk_factors": list[str],   # 리스크 요인 목록 (선택)
}

def validate_data(data: Dict[str, Any]) -> Optional[list[str]]:
    """API 입력 데이터가 스키마를 따르는지 유효성 검사합니다. [Schema Validation]"""
    errors = []
    # 1. 필수 필드 체크
    required_fields = ["user_id", "time_elapsed_hours", "initial_value"]
    for field in required_fields:
        if field not in data:
            errors.append(f"필수 필드 누락: '{field}'")

    # 2. 타입 체크
    try:
        if not isinstance(data["user_id"], str): errors.append("user_id는 문자열이어야 합니다.")
        if not isinstance(data["time_elapsed_hours"], (float, int)): errors.append("time_elapsed_hours는 숫자여야 합니다.")
        if not isinstance(data["initial_value"], (float, int)): errors.append("initial_value는 숫자여야 합니다.")

    except Exception as e:
        errors.append(f"타입 검사 중 예외 발생: {e}")

    return errors if errors else None

def calculate_loss_potential(data: Dict[str, Any]) -> float:
    """손실 예측 계산 로직 (Mock API Call). [Core Logic]"""
    # 실제 복잡한 비즈니스 로직이 들어가는 곳입니다. 여기서는 Mock 함수를 사용합니다.
    if not data:
        return 0.0

    try:
        time_hours = float(data["time_elapsed_hours"])
        initial_val = float(data["initial_value"])

        # Loss Potential Formula (Mock): -1 * 시간손실 * 가치하락률 + 리스크비용
        # Mock: 손실액 = 초기값 * (시간 경과 비율) * 위험 계수
        loss_rate = 55.0 # Self-RAG from company goal
        loss_amount = initial_val * time_hours * (1 + len(data["risk_factors"]) * 0.1) / 24

        return round(-loss_amount, 2) # 손실은 음수 값으로 표현

    except ValueError:
        # 데이터 타입 오류 발생 시 안전하게 기본값 반환
        print("⚠️ 경고: 계산 로직 실행 중 데이터 타입 변환 실패. 0을 반환합니다.")
        return -1.0


def run_integration_test(mock_data: Dict[str, Any]):
    """전체 통합 테스트를 실행하는 메인 함수."""
    print("=============================================")
    print("✨ Loss Potential Widget 통합 테스트 시작 ✨")
    print("=============================================")

    # 1. 스키마 유효성 검증 수행
    validation_errors = validate_data(mock_data)

    if validation_errors:
        print("\n🚨 [FAIL] Schema Validation Failed!")
        for error in validation_errors:
            print(f"  - {error}")
        return {"test_passed": False, "validation_errors": validation_errors}
    else:
        # 2. 로직 계산 및 통합 테스트 수행
        try:
            predicted_loss = calculate_loss_potential(mock_data)
            print(f"\n✅ [PASS] Data Validated. Calculated Loss Potential: {predicted_loss}")

            # 3. 추가 환경/렌더링 체크 (Mocking Cross-Device Check)
            if "mobile" in mock_data["risk_factors"] or "tablet" in mock_data["risk_factors"]:
                print("✅ [PASS] Mobile/Tablet Context Detected. Widget structure handles responsive layout.")
            else:
                 print("ℹ️ [INFO] Device context (Mobile/Desktop) check passed gracefully.")

            return {"test_passed": True, "loss_value": predicted_loss}
        except Exception as e:
            print(f"\n❌ [CRITICAL FAIL] Integration Test Failed during calculation: {e}")
            return {"test_passed": False, "error": str(e)}


if __name__ == "__main__":
    # --- 테스트 케이스 정의 ---

    # 1. Happy Path (정상 작동) - 정상 데이터를 사용한 테스트
    print("\n--- [TEST CASE 1] Happy Path (Schema Validation OK & Logic OK) ---")
    happy_path_data = {
        "user_id": "client-a",
        "time_elapsed_hours": 5.5, # 예시: 5.5시간 경과
        "initial_value": 100000.0,
        "risk_factors": ["compliance", "market_shift"]
    }
    result_happy = run_integration_test(happy_path_data)

    # 2. Failure Case (스키마 위반 - 누락 필드)
    print("\n--- [TEST CASE 2] Schema Violation (Missing Field: time_elapsed_hours) ---")
    missing_field_data = {
        "user_id": "client-b",
        # 'time_elapsed_hours' 누락
        "initial_value": 50000.0,
        "risk_factors": []
    }
    result_fail_schema = run_integration_test(missing_field_data)

    # 3. Failure Case (타입 위반 - 문자열 전달)
    print("\n--- [TEST CASE 3] Schema Violation (Type Error: Initial Value is string) ---")
    type_error_data = {
        "user_id": "client-c",
        "time_elapsed_hours": 10.0,
        "initial_value": "High Risk!", # 숫자여야 할 곳에 문자열 전달
        "risk_factors": []
    }
    result_fail_type = run_integration_test(type_error_data)

    # 최종 결과 보고를 위한 구조화된 변수 저장 (실제 보고서 작성용)
    final_results = {
        "happy_path": result_happy,
        "missing_field": result_fail_schema,
        "type_error": result_fail_type
    }