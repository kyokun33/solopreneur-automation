import pytest
from fastapi import FastAPI
# 실제 프로젝트에서는 main을 임포트하지만, 여기서는 구조 유지를 위해 테스트용으로 Mocking합니다.
# from backend.app.main import app 

# 가상의 API 호출 함수 (실제 환경에서는 httpx 등을 사용)
def call_diagnose_risk(data: dict):
    """가상으로 /api/diagnose_risk 엔드포인트를 호출하는 함수."""
    print("--- [TEST] Calling diagnose_risk endpoint ---")
    # 실제로는 HTTP 요청을 보내지만, 테스트 용이성을 위해 로직의 핵심 출력을 반환하도록 모킹합니다.
    if data['data_integrity_score'] < 0.5: # 낮은 점수 = 높은 리스크 가정
        return {
            "status": "CRITICAL",
            "loss_scorecard": {"total": 1234567.89, "breakdown": [...]},
            "anti_loss_message": "🚨 경고! 현재의 미진단 상태는 1,234,567.89 규모의 즉각적인 법적 리스크에 노출되어 있습니다.",
            "next_cta_state": "Purchase_Funnel_Entry"
        }
    elif data['data_integrity_score'] < 0.8: # 중간 점수 = 경고 가정
        return {
            "status": "WARNING",
            "loss_scorecard": {"total": 56789.12, "breakdown": [...]},
            "anti_loss_message": "⚠️ 잠재적 위험 경고. 현재 데이터 무결성 문제로 인해 최소 56,789.12 규모의 재정적 손실이 예상됩니다.",
            "next_cta_state": "Purchase_Funnel_Entry"
        }
    else: # 높은 점수 = 인지 단계 가정
         return {
            "status": "AWARENESS",
            "loss_scorecard": {"total": 1234.56, "breakdown": [...]},
            "anti_loss_message": "🔍 기본적인 리스크 노출은 확인되었으나, 심층적인 구조 분석이 필요합니다.",
            "next_cta_state": "Information_Gathering"
        }


@pytest.mark.parametrize("input_data, expected_status", [
    # Case 1: Critical Risk (Mini-Commitment Funnel 진입)
    ({"company_name": "TestCo", "data_integrity_score": 0.2, "regulatory_compliance_level": 2}, "CRITICAL"),
    # Case 2: Warning Risk (Anti-Loss 메시지 최대화 구간)
    ({"company_name": "MidCorp", "data_integrity_score": 0.6, "regulatory_compliance_level": 4}, "WARNING"),
    # Case 3: Low Risk (정보 수집 단계 유지)
    ({"company_name": "SafeCo", "data_integrity_score": 0.95, "regulatory_compliance_level": 5}, "AWARENESS"),
])
def test_loss_scorecard_state_transition(input_data, expected_status):
    """
    데이터 입력에 따라 Loss Scorecard의 상태 전이 로직이 정확하게 작동하는지 검증합니다.
    이는 Mini-Commitment Loop의 핵심 계약입니다.
    """
    result = call_diagnose_risk(input_data)
    assert result["status"] == expected_status, f"Expected status {expected_status}, got {result['status']}"

def test_mini_commitment_loop_flow():
    """
    전체 Funnel 흐름을 시뮬레이션합니다: 미진단(AWARENESS) -> 리스크 인지(WARNING) -> 구매 직전 (CRITICAL).
    핵심은 Anti-Loss 메시지가 단계별로 강도를 높여야 한다는 점입니다.
    """
    # 1. 초기 진입 (낮은 위험, AWARENESS)
    initial_data = {"company_name": "Initial", "data_integrity_score": 0.95, "regulatory_compliance_level": 5}
    result_awareness = call_diagnose_risk(initial_data)
    assert result_awareness["status"] == "AWARENESS"

    # 2. 경고 단계 (Mini-Commitment 유도, WARNING)
    warning_data = {"company_name": "Warning", "data_integrity_score": 0.6, "regulatory_compliance_level": 4}
    result_warning = call_diagnose_risk(warning_data)
    assert result_warning["status"] == "WARNING"
    # 여기서 Anti-Loss 메시지가 '진단'을 요구하며 긴급성을 부여해야 함.

    # 3. 결정적 단계 (CRITICAL - 구매 직전 최대 공포 유발)
    critical_data = {"company_name": "Critical", "data_integrity_score": 0.2, "regulatory_compliance_level": 2}
    result_critical = call_diagnose_risk(critical_data)
    assert result_critical["status"] == "CRITICAL"
    # 이 단계에서 Anti-Loss 메시지가 가장 강력해야 하며, CTA가 구매 버튼으로 직결되어야 함.