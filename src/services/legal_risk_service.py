# src/services/legal_risk_service.py

import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

class LegalRiskInputs(BaseModel):
    """
    법적 리스크 계산을 위한 표준화된 입력 데이터 모델 (API Contract).
    모든 호출은 이 스키마를 통해 검증되어야 합니다.
    """
    business_type: str = Field(..., description="사업의 주요 유형 (예: 금융, 의료, IT 서비스)")
    operational_years: float = Field(..., ge=0.1, le=50, description="운영 연차 (최소 0.1년 이상 필수)")
    compliance_status: str = Field(..., description="규제 준수 상태 (예: Compliant, Minor_Violation, Major_NonCompliance)")
    data_handling_complexity: int = Field(..., ge=1, le=5, description="데이터 처리 복잡도 점수 (1~5점). 5점이 가장 높음.")

class LegalRiskResult(BaseModel):
    """
    법적 리스크 계산 결과물의 표준화된 출력 모델.
    모든 성공적인 API 호출은 이 구조를 반환해야 합니다.
    """
    calculated_risk_score: float = Field(..., description="종합 법적 리스크 점수 (0.0 ~ 100.0)") # 100이 최고 위험
    potential_fine_usd: float = Field(..., description="예상되는 최대 벌금 규모 (USD).")
    risk_level: str = Field(..., description="리스크 등급 (Low, Medium, High, Critical)")

class LegalRiskCalculator:
    """
    고고플랙스의 핵심 법적 리스크 계산 엔진.
    외부 입력에 대한 견고한 검증과 예측 가능한 결과를 보장합니다.
    """
    def calculate_risk(self, inputs: Dict[str, Any]) -> Optional[LegalRiskResult]:
        """
        제공된 입력을 기반으로 법적 리스크 점수를 계산하고 결과를 반환합니다.

        Args:
            inputs (Dict[str, Any]): LegalRiskInputs 스키마를 따르는 딕셔너리 형태의 입력값.

        Returns:
            Optional[LegalRiskResult]: 계산 성공 시 결과 모델, 실패 시 None.
        """
        try:
            # 1. API 계약 기반 유효성 검사 (가드)
            validated_inputs = LegalRiskInputs(**inputs)
        except ValidationError as e:
            print(f"🚨 [Input Validation Error] 입력값이 스키마를 위반했습니다: {e}")
            return None

        # 2. 핵심 로직 실행
        try:
            score = self._calculate_core_score(validated_inputs)
            fine, level = self._determine_severity(score)
            return LegalRiskResult(
                calculated_risk_score=round(score, 2),
                potential_fine_usd=round(fine, 0),
                risk_level=level
            )
        except Exception as e:
            # 예측하지 못한 내부 오류 처리
            print(f"🐛 [Internal Error] 리스크 계산 중 치명적 오류 발생: {e}")
            return None

    def _calculate_core_score(self, inputs: LegalRiskInputs) -> float:
        """
        실제 법적 리스크 점수를 산출하는 순수 로직. (핵심 비즈니스 지식 포함)
        """
        # 기본점 설정 (Baseline Score): 20점
        base_score = 20.0

        # 가중치 계산: 데이터 복잡도 (최대 +30점)
        complexity_weight = inputs.data_handling_complexity * 5.0
        
        # 운영 연차에 따른 안정성 감점/가산점 (-10~+20점)
        tenure_adjustment = min(inputs.operational_years / 5, 1.0) * 15.0 # 최대 15점 가산

        # 컴플라이언스 상태에 따른 치명적 감점/가산점 (핵심!)
        compliance_score: float
        if inputs.compliance_status == "Major_NonCompliance":
            compliance_score = 40.0 # 매우 높음
        elif inputs.compliance_status == "Minor_Violation":
            compliance_score = 15.0 # 중간 정도 위험
        else: # Compliant 등
            compliance_score = 5.0 # 안정적

        total_score = base_score + complexity_weight + tenure_adjustment + compliance_score
        return min(max(total_score, 0), 100.0) # 점수 범위 제한 (0~100)


    def _determine_severity(self, score: float) -> tuple[float, str]:
        """
        계산된 최종 점수를 기반으로 벌금과 위험 등급을 결정합니다.
        """
        if score >= 85.0:
            risk_level = "Critical"
            potential_fine = score * 1200 # 가장 치명적일 때 높은 가중치 적용
        elif score >= 60.0:
            risk_level = "High"
            potential_fine = score * 750
        elif score >= 30.0:
            risk_level = "Medium"
            potential_fine = score * 200
        else:
            risk_level = "Low"
            potential_fine = 0.0

        return potential_fine, risk_level

# --- 테스트용 예시 실행 (실제 서비스 환경에서는 제거) ---
if __name__ == "__main__":
    calculator = LegalRiskCalculator()
    print("==========================================")
    print("✅ [테스트 1] 최악의 상황 시뮬레이션:")
    worst_case = {
        "business_type": "금융",
        "operational_years": 0.5,
        "compliance_status": "Major_NonCompliance",
        "data_handling_complexity": 5
    }
    result1 = calculator.calculate_risk(worst_case)
    print("결과:", result1.model_dump() if result1 else "실패")

    print("\n==========================================")
    print("[테스트 2] 최적의 상황 시뮬레이션:")
    best_case = {
        "business_type": "IT 서비스",
        "operational_years": 10.0,
        "compliance_status": "Compliant",
        "data_handling_complexity": 2
    }
    result2 = calculator.calculate_risk(best_case)
    print("결과:", result2.model_dump() if result2 else "실패")

    print("\n==========================================")
    print("[테스트 3] 유효성 검사 실패 시뮬레이션 (에러 핸들링):")
    invalid_case = {
        "business_type": "의료",
        # operational_years를 음수로 넣어 강제 오류 발생
        "operational_years": -1.0, 
        "compliance_status": "Compliant",
        "data_handling_complexity": 3
    }
    result3 = calculator.calculate_risk(invalid_case)
    print("결과:", result3.model_dump() if result3 else "실패 (예상됨)")
# =========================================="