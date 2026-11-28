# tests/test_api_service.py
import pytest
from src.core.loss_detector.api_service import LossDetector, LossDataPoint
from typing import List

@pytest.fixture(scope="module")
def detector():
    """테스트를 위한 Detector 인스턴스 제공."""
    return LossDetector()


# ==============================================
# 🟢 테스트 시나리오 1: 정상 상태 (Stable State) - 패닉 아님
# 임계점 미달, 스파이크 없음.
def test_scenario_normal(detector):
    """정상적인 데이터 흐름에서 패닉이 감지되지 않아야 함."""
    data_points = [
        LossDataPoint(timestamp=1600, total_loss=500, current_loss_rate=30), # 초기
        LossDataPoint(timestamp=1630, total_loss=800, current_loss_rate=40)  # 안정적 증가
    ]
    result = detector.detect_panic(data_points)
    assert result.is_panic_state is False
    print("✅ Test Passed: Normal State (Expected False)")


# ==============================================
# 🟡 테스트 시나리오 2: 임계점만 도달 (Threshold Only) - 패닉 아님
# 스파이크가 없으면 아무리 손실이 커도 'Peak'는 아니다.
def test_scenario_threshold_only(detector):
    """임계점은 넘겼으나, 급증 패턴을 보이지 않아 패닉 상태가 아니어야 함."""
    data_points = [
        LossDataPoint(timestamp=1600, total_loss=500, current_loss_rate=30),
        # 30초 전 대비 손실률 변화가 미미함. (Spike 조건 실패)
        LossDataPoint(timestamp=1630, total_loss=2000, current_loss_rate=45) 
    ]
    result = detector.detect_panic(data_points)
    assert result.is_panic_state is False
    print("✅ Test Passed: Threshold Only (Expected False)")


# ==============================================
# 🔴 테스트 시나리오 3: Peak Panic State (Full Trigger) - 패닉 발생!
def test_scenario_peak_panic(detector):
    """임계점 도달과 손실 급증이 동시에 발생하여 패닉 상태여야 함."""
    initial_rate = 30.0 # 기준 손실률
    
    data_points = [
        # 1. 초기 데이터 (기준 설정)
        LossDataPoint(timestamp=1600, total_loss=500, current_loss_rate=initial_rate),
        # 2. 시간이 흐름 (30초 전 대비 비교 기준점: T=1600)
        # 3. 패닉 발생 직전 데이터 (T=1629) - 임계점 근처
        LossDataPoint(timestamp=1629, total_loss=1450, current_loss_rate=40), # 임계점 미달
        # 4. 최종 패닉 포인트 (T=1659): 임계점 도달 + 급증 발생
        LossDataPoint(timestamp=1659, total_loss=2800, current_loss_rate=130) # 130/30 = 4.3배 증가 (>2.5배)
    ]
    result = detector.detect_panic(data_points)
    assert result.is_panic_state is True
    print("✅ Test Passed: Peak Panic State (Expected True)")


# ==============================================
# ❌ 테스트 시나리오 4: 데이터 부족/오류 처리
def test_scenario_insufficient_data(detector):
    """데이터가 부족하면 안전하게 False를 반환해야 함."""
    data_points = [LossDataPoint(timestamp=1600, total_loss=500, current_loss_rate=30)]
    result = detector.detect_panic(data_points)
    assert result.is_panic_state is False
    print("✅ Test Passed: Insufficient Data (Expected False)")