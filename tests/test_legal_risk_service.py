# tests/test_legal_risk_service.py

import pytest
from src.services.legal_risk_service import LegalRiskCalculator, LegalRiskInputs

@pytest.fixture(scope="module")
def calculator():
    """테스트에 사용할 LegalRiskCalculator 인스턴스를 제공합니다."""
    return LegalRiskCalculator()

# ======================================================
# 🚀 테스트 케이스 그룹 1: 성공적인 시나리오 (Happy Path)
# ======================================================

def test_low_risk_scenario(calculator):
    """가장 안정적이고 낮은 리스크를 가진 경우의 점수와 등급을 확인합니다."""
    inputs = {
        "business_type": "IT 서비스",
        "operational_years": 15.0, # 오랜 운영 연차
        "compliance_status": "Compliant",
        "data_handling_complexity": 2  # 낮은 복잡도
    }
    result = calculator.calculate_risk(inputs)
    assert result is not None
    assert result.risk_level == "Low" # 기대하는 결과 확인
    assert result.potential_fine_usd <= 1000

def test_medium_risk_scenario(calculator):
    """일반적이고 중간 수준의 리스크를 가진 경우를 테스트합니다."""
    inputs = {
        "business_type": "전자상거래",
        "operational_years": 3.0,
        "compliance_status": "Minor_Violation", # 경미한 위반
        "data_handling_complexity": 4
    }
    result = calculator.calculate_risk(inputs)
    assert result is not None
    assert result.risk_level == "Medium"
    assert 1000 < result.potential_fine_usd <= 3500 # 벌금 범위 확인

def test_critical_risk_scenario(calculator):
    """가장 위험하고 치명적인 상황을 시뮬레이션하여 최고 점수를 얻는지 검증합니다."""
    inputs = {
        "business_type": "금융",
        "operational_years": 0.5, # 신규/미숙련
        "compliance_status": "Major_NonCompliance", # 핵심 위반
        "data_handling_complexity": 5 # 최대 복잡도
    }
    result = calculator.calculate_risk(inputs)
    assert result is not None
    assert result.risk_level == "Critical" # 최고 등급 확인
    assert result.calculated_risk_score >= 90.0

# ======================================================
# 🐛 테스트 케이스 그룹 2: 에지 및 실패 시나리오 (Failure/Edge Cases)
# ======================================================

def test_input_validation_missing_field(calculator):
    """필수 입력 필드(예: compliance_status)가 누락되었을 때 API 계약이 이를 거부하는지 확인합니다."""
    invalid_inputs = {
        "business_type": "테스트",
        "operational_years": 5.0,
        # 'compliance_status' 필드가 없음 (ValidationError 발생 유도)
        "data_handling_complexity": 3
    }
    result = calculator.calculate_risk(invalid_inputs)
    assert result is None # 실패해야 함

def test_input_validation_out_of_bounds(calculator):
    """운영 연차가 비정상적으로 낮거나 높은 경우 (ge/le 제약 조건 위반)를 테스트합니다."""
    # operational_years: 0.1 미만으로 설정하여 유효성 검사 실패 유도
    invalid_inputs = {
        "business_type": "테스트",
        "operational_years": 0.0, 
        "compliance_status": "Compliant",
        "data_handling_complexity": 3
    }
    result = calculator.calculate_risk(invalid_inputs)
    assert result is None # 실패해야 함

def test_empty_input(calculator):
    """입력 자체가 빈 경우 (가장 기본적인 오류 처리)를 테스트합니다."""
    empty_inputs = {}
    result = calculator.calculate_risk(empty_inputs)
    assert result is None # 실패해야 함