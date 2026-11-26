// src/components/shared/LossScorecard.tsx - The core component responsible for displaying risk analysis
import React, { useState, useEffect } from 'react';
import { LossScorecardData, fetchRiskAssessmentData } from '../../api/riskAssessmentApi';

interface LossScorecardProps {} // 현재는 Props가 필요 없습니다. 전역 API 호출을 가정합니다.

/**
 * @description 사용자의 데이터 무결성 리스크를 시각화하고 Anti-Loss 메시지를 전달하는 핵심 컴포넌트.
 */
const LossScorecard: React.FC<LossScorecardProps> = () => {
    // 1. State Management
    const [data, setData] = useState<LossScorecardData | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // 2. Data Fetching 및 로직 처리 (가장 중요한 부분)
        const loadData = async () => {
            setIsLoading(true);
            try {
                // API 호출을 통해 모든 데이터와 패널티 적용 결과를 받습니다.
                const fetchedData = await fetchRiskAssessmentData();
                setData(fetchedData);

            } catch (error) {
                console.error("Failed to load scorecard data:", error);
                // 실패 시, 에러 상태를 로깅하고 기본 데이터 구조로 설정합니다.
                setData(null); 
            } finally {
                setIsLoading(false);
            }
        };

        loadData();
    }, []);


    // 3. Render Logic (데이터가 준비되었을 때만 실행)
    if (isLoading) {
        return <div className="loading-state">⚡️ 리스크 분석 중... 데이터 로드를 기다려주세요.</div>;
    }

    if (!data) {
         // API 호출 실패 또는 심각한 에러 발생 시 fallback UI 제공
        return <div className="error-state">⚠️ 시스템 오류: 리스크 데이터를 불러올 수 없습니다. 관리자에게 문의해주세요.</div>;
    }


    // 4. 비즈니스 로직 기반의 조건부 렌더링 (Anti-Loss Funnel 핵심)
    const isCritical = data.finalRiskScore < 30 || data.dataIsMissing;

    return (
        <div className={`loss-scorecard ${isCritical ? 'critical' : ''}`}>
            {/* Hero Section: Headline and Score Visualization */}
            <section className="score-gauge">
                <h1>데이터 무결성 리스크 보고서</h1> 
                <p>현재 시스템의 예상 손실 비용을 지금 확인하세요.</p>

                {/* Loss Counter 위젯 Placeholder (Animation Logic) */}
                <div data-testid="loss-counter">
                    총 예측 손실액: <span className={`amount ${isCritical ? 'warning' : ''}`}>${data.totalFinalLossUSD.toLocaleString()}</span>
                </div>
            </section>

            {/* Warning/Action Section: Anti-Loss 메시지 */}
            <section className="action-panel">
                <h2>🚨 경고! {data.dataIsMissing ? "필수 데이터 결핍 감지" : ""}</h2>
                <p>{isCritical 
                    ? `현재 리스크 점수(${Math.round(data.finalRiskScore)}점)는 심각한 수준입니다. 데이터를 보강하지 않으면, ${data.totalFinalLossUSD.toLocaleString()}의 손실을 초래할 수 있습니다.`
                    : `시스템은 안정적입니다. 그러나 잠재적인 데이터 결핍 리스크를 항상 염두에 두어야 합니다.`
                }</p>
            </section>

            {/* Detailed Breakdown Section */}
            <section className="breakdown-details">
                <h3>손실 원인 분석 (Loss Breakdown)</h3>
                {data.lossBreakdown.map((item, index) => (
                    <div key={index} style={{ borderLeft: `3px solid ${item.category === '데이터 무결성' ? '#CC3333' : '#0066CC'}` }}>
                        <strong>{item.category}:</strong> 예상 손실액 ${item.estimatedCostUSD.toLocaleString()} (기간: {item.durationDays}일)
                    </div>
                ))}
            </section>
        </div>
    );
};

export default LossScorecard;