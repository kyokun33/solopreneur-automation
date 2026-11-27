/**
 * @description Loss Scorecard의 시각적 표현을 담당하는 컴포넌트입니다.
 * 핵심 로직은 useLossScorecard 훅에 위임하여 Pure Component로 유지합니다.
 */
import React from 'react';
import { UseLossScorecardHook } from '../hooks/useLossScorecard';

interface LossScorecardProps {
    initialData: Partial<{ timeElapsedHours: number, dataIntegrityRiskPoints: number, legalComplianceIssueDetected: boolean }>;
}

const LossScorecard: React.FC<LossScorecardProps> = ({ initialData }) => {
    // 훅을 통해 상태 로직 관리
    const { scorecard, history, isLoading, onInputChange } = useLossScorecard(initialData);

    if (isLoading && !scorecard) {
        return <div className="loading-state">⚙️ 스코어카드 데이터 분석 중... 잠시만 기다려 주세요.</div>;
    }

    if (!scorecard) {
         // 초기 로딩 후에도 결과가 없을 경우의 Fallback UI
        return <div className="error-state">데이터를 불러올 수 없습니다. 설정을 확인해 주세요.</div>;
    }

    const { currentLossState, totalEstimatedLossUSD, explanationMessage } = scorecard;

    // 상태에 따른 동적 스타일링 (Red Warning / Glitch Effect 시뮬레이션)
    const stateClass = `state-${currentLossState.toLowerCase()}`;
    const isCritical = currentLossState === 'Critical';

    return (
        <div className={`scorecard-container ${stateClass} ${isCritical ? 'glitch-active' : ''}`}>
            {/* 1. 핵심 지표: Loss Counter 위젯 */}
            <div className="loss-counter">
                <h2 className="main-title">{`예상 손실액:`}</h2>
                <p className={`total-loss ${isCritical ? 'critical' : ''}`}>
                    ${new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(totalEstimatedLossUSD)}
                </p>
            </div>

            {/* 2. 현재 상태 및 경고 메시지 */}
            <div className="status-alert">
                <h3>현재 리스크 레벨: <span className={`state-${currentLossState.toLowerCase()}`}>{currentLossState}</span></h3>
                <p className="explanation">{explanationMessage}</p>
                {/* 이 부분에 Red Warning Filter와 Glitch Effect를 시각적으로 적용합니다. */}
            </div>

            {/* 3. 상세 손실 Breakdown (시각화 요소) */}
            <div className="loss-breakdown">
                <h4>손실 원인 분석 (Loss Breakdown)</h4>
                <p>시간적 위험: ${totalEstimatedLossUSD * 0.4} | 데이터 리스크: ${totalEstimatedLossUSD * 0.3} | 법적 책임: ${totalEstimatedLossUSD * 0.3}</p>
            </div>

             {/* 4. 상태 전이 시뮬레이션 버튼 (테스트 용) */}
            <div className="input-control">
                <h4>시나리오 테스트</h4>
                <button onClick={() => onInputChange({ timeElapsedHours: 20, dataIntegrityRiskPoints: 50, legalComplianceIssueDetected: true })}>
                    [Max Risk] 최대 리스크 시뮬레이션 (Critical)
                </button>
                 <button onClick={() => onInputChange({ timeElapsedHours: 3, dataIntegrityRiskPoints: 10, legalComplianceIssueDetected: false })}>
                    [Low Risk] 최소 리스크 시뮬레이션 (Apathy)
                </button>
            </div>

             {/* 5. 상태 전이 이력 */}
            <div className="history-log">
                <h5>최근 스코어카드 변화 로그 ({history.length}회 기록):</h5>
                <ul>
                    {history.slice(-3).map((item, index) => (
                        <li key={index}>
                            [{item.timestamp.toLocaleTimeString()}] {item.prevState} $\\rightarrow$ <strong>{item.currentState}</strong> ({item.triggerEvent})
                        </li>
                    ))}
                </ul>
            </div>

        </div>
    );
};

export default LossScorecard;