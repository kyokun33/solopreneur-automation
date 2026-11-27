import React, { useState, useCallback } from 'react';
import { LossScorecardResult, RiskFactor } from '../../types/scorecard'; // 타입 사용
import VisualEffectsWrapper from './VisualEffectsWrapper';
import CalculationEngine from './CalculationEngine';

/**
 * @component LossScorecard.tsx
 * @description 손실 정량화(Loss Scorecard)의 메인 컴포넌트입니다.
 * 이 컴포넌트는 State 관리 및 API 호출 흐름을 제어하는 '오케스트레이터' 역할을 합니다.
 */
const LossScorecard: React.FC = () => {
    // 초기 리스크 요인 데이터 (Mocking)
    const [riskFactors, setRiskFactors] = useState<RiskFactor[]>([
        { id: 'AI_BIAS', description: 'AI 편향으로 인한 의사결정 오류 위험', severityScore: 8, potentialCost: 1500 },
        { id: 'DATA_INTEGRITY', description: '데이터 무결성 문제로 인한 시스템 장애 리스크', severityScore: 9, potentialCost: 2500 },
    ]);

    // 상태 관리
    const [result, setResult] = useState<LossScorecardResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    /**
     * API 호출을 시뮬레이션하고 계산을 실행하는 핸들러.
     * @param factors - 사용자가 입력한 리스크 요인 배열
     */
    const handleCalculateScorecard = useCallback(async (factors: RiskFactor[]) => {
        setIsLoading(true);
        setError(null);

        try {
            // 1. 비즈니스 로직 수행 (CalculationEngine 호출)
            // 이 부분에서 실제 API 호출이 들어간다고 가정합니다.
            const calculatedResult = await CalculationEngine.calculate(factors); 
            
            setResult(calculatedResult);
        } catch (e) {
            console.error("Loss Scorecard Calculation Error:", e);
            setError("손실 점수 계산 중 오류가 발생했습니다. 데이터를 확인해주세요.");
            setResult(null);
        } finally {
            setIsLoading(false);
        }
    }, []);

    // 컴포넌트 렌더링 로직
    return (
        <section className="loss-scorecard-container">
            <h1>📊 당신의 비즈니스 손실 점수 진단</h1>
            
            {/* 입력 섹션 */}
            <div className="input-panel">
                {riskFactors.map(factor => (
                    <p key={factor.id}>{factor.description} - 잠재적 비용: ${factor.potentialCost.toLocaleString()}</p>
                ))}
                <button 
                    onClick={() => handleCalculateScorecard(riskFactors)}
                    disabled={isLoading}
                    className="calculate-button"
                >
                    {isLoading ? '분석 중...' : '손실 점수 진단 실행 (Free)'}
                </button>
            </div>

            {/* 결과 섹션 */}
            <div className="result-panel">
                {error && <div className="alert alert-danger">{error}</div>}
                {!result && !isLoading && <p>진단을 실행하여 잠재적 손실 점수를 확인하세요.</p>}
                
                {/* VisualEffectsWrapper를 사용하여 핵심 결과를 감싸 공포감을 조성 */}
                {result && (
                    <VisualEffectsWrapper>
                        <h2>⚠️ 최종 예상 손실 비용: ${result.totalLossEstimate.toLocaleString()}</h2>
                        <p>{result.summaryReportText}</p>

                        {/* 상세 Breakdown 섹션 */}
                        <h3>📊 손실 기여도 분석 (Breakdown)</h3>
                        <div className="breakdown-list">
                            {result.calculationBreakdown.map((detail, index) => (
                                <div key={index} className={`detail-${detail.severityLevel.toLowerCase()}`}>
                                    <h4>{detail.factorDescription}</h4>
                                    <p>기여율: {detail.contributionPercentage.toFixed(1)}%</p>
                                    <p>예상 손실액: ${detail.estimatedLossAmount.toLocaleString()} (심각도: {detail.severityLevel})</p>
                                </div>
                            ))}
                        </div>

                        {/* CTA 영역 - 가장 중요한 전환 지점 */}
                        <button className="cta-report">
                            ➡️ 상세 진단 보고서 요청하기 ($XX)
                        </button>
                    </VisualEffectsWrapper>
                )}
            </div>
        </section>
    );
};

export default LossScorecard;