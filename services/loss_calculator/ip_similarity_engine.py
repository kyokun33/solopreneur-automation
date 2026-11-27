from dataclasses import dataclass
import math
from typing import List, Optional
from services.loss_calculator.models import CalculationInput, LossAssessment

class IPSimilarityEngine:
    """
    지식재산권(IP) 유사성 리스크 계산 전담 엔진. 
    진단 대상과 비교 자산을 분석하여 '법적 책임 발생 가능성'을 측정합니다.
    [원칙] LLM 기반의 비정형 데이터 처리와 외부 API 호출 실패를 대비해야 합니다.
    """

    def calculate_risk(self, input_data: CalculationInput) -> LossAssessment:
        """
        IP 유사성 리스크 점수를 계산하고 LossAssessment 객체로 반환합니다.
        """
        try:
            # 1. 필수 입력값 유효성 검사 (Guard Logic)
            if not input_data.ip_asset_name or not input_data.comparison_assets:
                raise ValueError("진단 대상 IP 자산명과 비교할 경쟁/유사 자산 목록은 필수입니다.")

            # 2. 로직 구현 (예시): 유사성 점수는 비교 자산 수에 비례하고, 무결성에 반비례한다고 가정
            num_comparisons = len(input_data.comparison_assets)
            
            # IP 리스크 점수 계산: 기본값 * (비교 개수 / 5) - 데이터무결성 점수가 낮을수록 위험 증가
            base_score = num_comparisons * 0.15
            integrity_penalty = (1.0 - (input_data.user_data_integrity_score or 1.0)) * 0.2

            raw_score = base_score + integrity_penalty
            loss_score = min(1.0, raw_score) # 점수 최대 1.0 제한

            # 예상 손실 금액 (진단 서비스의 고가 컨설팅 비용을 기준으로 잡음)
            estimated_loss = loss_score * 5000.0 # 가상의 최소 벌금/컨설팅 비용 $

            # 3. 심각도 레벨 결정 로직
            if loss_score >= 0.7:
                severity = "CRITICAL"
            elif loss_score >= 0.3:
                severity = "MODERATE"
            else:
                severity = "LOW"

            return LossAssessment(
                risk_type="IP Similarity", 
                score=loss_score, 
                estimated_loss_usd=round(estimated_loss, 2), 
                severity_level=severity
            )

        except ValueError as e:
            print(f"[ERROR] IP Similarity Risk Calculation Failed (Validation): {e}")
            return LossAssessment("IP Similarity", 0.0, 0.0, "UNKNOWN")
        except Exception as e:
            print(f"[FATAL ERROR] IP Similarity Risk Calculation Failed (System): {e}")
            # 시스템 실패 시에는 일단 최악의 경우로 가정하고 사용자에게 알림.
            return LossAssessment("IP Similarity", 1.0, 9999.99, "CRITICAL_FAILURE")