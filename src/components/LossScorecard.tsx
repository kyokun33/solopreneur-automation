import React, { useState, useMemo } from 'react';
import './LossScorecard.css'; // CSS 파일을 분리하여 스타일링합니다.

// 1. 타입 정의 (TypeScript Strictness)
interface LossData {
  lossAmount: number; // 손실 총액 (예: $50,000)
  riskLevel: 'low' | 'medium' | 'high'; // 리스크 레벨
}

/**
 * Loss Scorecard 컴포넌트. 데이터 주입 및 상태 변화에 따른 UI 전환을 시뮬레이션합니다.
 * @param initialData - 외부에서 주입되는 초기 손실 데이터를 받습니다.
 */
const LossScorecard: React.FC<{ data: LossData }> = ({ data }) => {
  // 2. 핵심 로직: 현재 상태(State) 결정 (Memoization 활용)
  const currentState = useMemo(() => {
    if (data.lossAmount >= 100000 || data.riskLevel === 'high') {
      return 'critical'; // 임계점 초과 또는 최고 리스크
    } else if (data.lossAmount >= 20000 || data.riskLevel === 'medium') {
      return 'warning'; // 경고 구간 진입
    } else {
      return 'normal'; // 정상 상태
    }
  }, [data]);

  // 3. Red Warning Overlay 관리 로직
  const isWarningActive = currentState !== 'normal';
  
  // CSS 클래스에 따라 동적으로 스타일을 적용할 변수들
  const cardClass = `scorecard-container ${currentState}`;

  return (
    <div className="loss-wrapper">
      {/* Red Warning/Glitch 필터 오버레이 레이어 */}
      {isWarningActive && (
        <div className="red-warning-overlay" data-state={currentState}>
          {/* 실제 구현에서는 여기에 Glitch Effect CSS Animation을 적용합니다. */}
          <p className="glitch-message">⚠️ WARNING: Critical Loss Detected!</p> 
        </div>
      )}

      {/* 메인 스코어카드 컨테이너 */}
      <div className={cardClass}>
        <h2 className="scorecard-title">당신의 잠재적 손실 점수</h2>
        
        {/* 핵심 위젯: Loss Counter 시뮬레이션 */}
        <div className="loss-counter-widget">
          <span className="amount">${data.lossAmount.toLocaleString()}</span>
          <span className="unit">예상 손실액 (Estimated Cost)</span>
        </div>

        {/* 리스크 분석 결과 요약 */}
        <div className="risk-summary">
            <p>진단된 리스크 레벨: <strong className={`level-${data.riskLevel}`}>{data.riskLevel.toUpperCase()}</strong></p>
            <button className={`cta-button cta-${currentState}`}>
                {currentState === 'critical' ? '🚨 즉시 전문 진단 보고서 요청하기' : '✅ 상세 리포트 확인 및 행동 계획 받기'}
            </button>
        </div>

        {/* 상태별 안내 메시지 (UX 목표 반영) */}
        <p className="status-guide">
          {currentState === 'normal' && "현재는 안정적이지만, 놓치고 있는 잠재 리스크가 있습니다."}
          {currentState === 'warning' && "경고: 현재 활동으로 인해 손실이 발생하기 시작했습니다. 즉각적인 점검이 필요합니다."}
          {currentState === 'critical' && "CRITICAL LOSS! 심각한 수준의 손실 위험에 직면했습니다. 전문 컨설팅 없이는 회복 불가 예측됩니다."}
        </p>
      </div>
    </div>
  );
};

export default LossScorecard;