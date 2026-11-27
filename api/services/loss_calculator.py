# LossCalculatorService 구현: 순수 비즈니스 로직만 담당하는 서비스 레이어
from typing import Dict, Any, List
import uuid

class CalculationBreakdownItem(Dict):
    """손실 계산의 개별 항목을 정의합니다."""
    def __init__(self, category: str, metric: str, value: float, weight: float):
        super().__init__()
        self['category'] = category  # 예: 시간 손실, 데이터 무결성 리스크
        self['metric'] = metric    # 예: $55/시간, 10% 확률
        self['value'] = value      # 실제 계산된 금액 또는 비율
        self['weight'] = weight    # 해당 항목의 중요도(가중치)

class LossCalculatorService:
    """
    손실 점수 및 상세 분석 보고서를 생성하는 핵심 서비스 로직.
    API 프레임워크로부터 완전히 분리되어 있어 테스트 용이성이 극대화됩니다.
    """
    def __init__(self, client_id: str):
        self.client_id = client_id

    def calculate_loss(self, data_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        제공된 데이터를 기반으로 전체 손실 점수와 상세 내역을 계산합니다.
        반드시 '시간'과 '데이터/규정 리스크' 두 가지 핵심 요소를 포함해야 합니다.
        :param data_input: 사용자가 입력한 데이터 (예: 작업 시간, 관리 현황 등)
        :return: 최종 손실 점수 및 상세 Breakdown 정보가 담긴 딕셔너리.
        """
        
        # --- [1] 시간 기반 손실 계산 (Time Loss - 필수 요소) ---
        try:
            hours = float(data_input.get("working_hours", 0)) # 예시: 근무시간
            rate_per_hour = data_input.get("hourly_loss_rate", 55.0) # $55/hr (Self-RAG 근거)
            time_loss = hours * rate_per_hour
            
            time_breakdown = CalculationBreakdownItem(
                category="시간 손실", 
                metric=f"${rate_per_hour}/시간", 
                value=time_loss, 
                weight=0.6 # 시간적 리스크가 가장 큰 비중을 차지한다고 가정
            )
        except ValueError:
            time_breakdown = CalculationBreakdownItem("오류", "데이터 형식 오류", 0.0, 0.1)
        
        # --- [2] 데이터/규정 리스크 계산 (Data Integrity Risk - 필수 요소) ---
        try:
            data_risk_percentage = float(data_input.get("data_integrity_risk_percent", 0)) # 예시: 5%
            base_asset_value = data_input.get("total_assets", 100000) # 총 자산가치 (임의값 설정)
            
            # 리스크 점수 계산 로직: 자산 가치 * 위험 비율 * 위기 계수(2.0) 적용
            data_loss = base_asset_value * (data_risk_percentage / 100) * 2.0
            
            data_breakdown = CalculationBreakdownItem(
                category="데이터 무결성 리스크", 
                metric=f"{data_risk_percentage}% 위험", 
                value=data_loss, 
                weight=0.4 # 데이터 관리가 매우 중요하지만 시간 손실보다는 비중을 낮게 설정 (가정)
            )
        except ValueError:
            data_breakdown = CalculationBreakdownItem("오류", "데이터 형식 오류", 0.0, 0.1)


        # --- [3] 최종 점수 합산 및 구조화 ---
        total_loss = time_loss + data_loss

        detailed_breakdown: List[Dict[str, Any]] = [
            time_breakdown.dict(),
            data_breakdown.dict()
        ]

        return {
            "calculation_id": str(uuid.uuid4()), # 추적 가능한 ID 부여 (재현성 확보)
            "client_id": self.client_id,
            "total_loss_score": round(total_loss, 2),
            "detailed_breakdown": detailed_breakdown,
            "analysis_status": "CRITICAL_LOSS_DETECTED" if total_loss > 1000 else "MONITORING_REQUIRED" # 상태값 추가 (UX 활용)
        }