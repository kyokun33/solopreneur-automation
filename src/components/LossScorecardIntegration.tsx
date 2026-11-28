import React, { useState, useEffect, useCallback } from 'react';
import './LossScorecardIntegration.css'; // CSS 파일도 필요할 것입니다.

// --- [1] Types and Constants (Self-RAG: Anti-Loss Funnel & $1500 Threshold) ---
interface LossState {
  totalLoss$: number;
  isCritical: boolean; // $1,500 임계점 도달 여부
}

const CRITICAL_THRESHOLD = 1500;
const INITIAL_LOSS = 0;

// 가상의 손실 계산 및 상태 업데이트 로직 (백엔드/Redux에서 받아와야 할 부분)
const calculateLoss = (timeElapsedHours: number): { loss$: number, critical: boolean } => {
    const hourlyRate = 55; // [근거: Self-RAG] $55/hour 고정값
    const calculatedLoss = timeElapsedHours * hourlyRate;
    return { 
        loss$: parseFloat(calculatedLoss.toFixed(2)), 
        critical: calculatedLoss >= CRITICAL_THRESHOLD 
    };
}


// --- [2] Component Implementation ---

/**
 * Loss Scorecard 통합 컴포넌트 (E2E Test Environment)
 * - 핵심 목표: Anti-Loss Funnel 로직 검증 및 Consent 게이트 구현.
 */
const LossScorecardIntegration: React.FC = () => {
    // [State] 시간 경과에 따른 손실 상태 관리
    const [timeElapsedHours, setTimeElapsedHours] = useState(0);
    const [lossState, setLossState] = useState<LossState>({ totalLoss$: INITIAL_LOSS, isCritical: false });
    
    // [State] 필수 동의 여부 (CEO 지시사항)
    const [isConsentGiven, setIsConsentGiven] = useState(false);

    // ⏰ 손실 계산 및 상태 업데이트 효과 (매초 시간 경과에 따라 로직 트리거)
    useEffect(() => {
        if (timeElapsedHours > 24) return; // 테스트 제한

        const intervalId = setInterval(() => {
            setTimeElapsedHours(prevTime => {
                const newTime = prevTime + 1/60; // 1초당 1/60 시간 경과 가정
                
                // 손실 계산 로직 실행 (핵심 비즈니스 로직)
                const calculatedLoss = calculateLoss(newTime);
                setLossState({ totalLoss$: calculatedLoss.loss$, isCritical: calculatedLoss.critical });
                return newTime;
            });
        }, 1000);

        // 클린업 함수
        return () => clearInterval(intervalId);
    }, [timeElapsedHours]);


    // 🔑 핵심 로직: CTA 활성화 여부 결정 (Consent & Critical State)
    const isReportRequestActive = isConsentGiven && lossState.isCritical;

    // --- 핸들러 함수 ---
    const handleCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setIsConsentGiven(event.target.checked);
    };

    const handleReportRequest = () => {
        if (!isReportRequestActive) {
            console.error("진단 보고서 요청은 필수 동의 및 임계점 도달 시에만 가능합니다.");
            alert("⚠️ 경고: 먼저 이용약관에 동의해주시고, 손실 리스크가 Critical State에 진입해야 보고서를 요청할 수 있습니다.");
        } else {
            console.log("✅ 최종 보고서 요청 로직 실행! (API 호출 예정)");
            // 여기에 실제 API 호출 및 데이터 전송 로직을 구현합니다.
        }
    };

    // --- UI 렌더링 ---
    return (
        <div className="scorecard-container">
            <h1>🔥 Anti-Loss Funnel 진단 대시보드</h1>
            <p className="subtitle">현재 시간 경과에 따른 예상 손실액을 실시간으로 확인하세요.</p>

            {/* 🚨 Loss Scorecard Display (Critical State & Animation Hook) */}
            <div className={`loss-display ${lossState.isCritical ? 'critical' : ''}`} aria-live="polite">
                <h2>현재 누적 예상 손실액</h2>
                <div className="loss-counter" style={{ color: lossState.isCritical ? '#CC3333' : '#1D1D1F' }}>
                    ${lossState.totalLoss$.toLocaleString()} 
                    {/* [근거: Self-RAG] Loss Accent - Red Color */}
                </div>
                <p className={`risk-message ${lossState.isCritical ? 'glitch-active' : ''}`}>
                    {lossState.isCritical ? "🚨 CRITICAL STATE 진입! 법적 리스크가 임계점을 초과했습니다." : 
                                    `위험 수준: 관찰 중 (${Math.round(timeElapsedHours * 60)}분 경과)`}
                </p>
            </div>

            {/* 🛡️ Consent Gate Component (CEO 지시사항) */}
            <div className="consent-gate">
                <h3>⚠️ 다음 단계 진행 전 필수 확인 사항</h3>
                <label className="checkbox-container">
                    <input 
                        type="checkbox" 
                        checked={isConsentGiven} 
                        onChange={handleCheckboxChange} 
                        id="termsConsent"
                    />
                    <span htmlFor="termsConsent">
                         저는 고고플랙스가 제시하는 모든 진단 서비스의 이용약관 및 개인정보 수집에 동의합니다.
                    </span>
                </label>
            </div>

            {/* ✨ 최종 CTA 버튼 (Activation Gate) */}
            <button 
                className={`cta-button ${isReportRequestActive ? 'active' : 'disabled'}`}
                onClick={handleReportRequest}
                disabled={!isReportRequestActive}
            >
                {isReportRequestActive ? "✅ 리스크 진단 보고서 요청 (클릭)" : 
                                  (isConsentGiven ? "⚠️ 동의 필요: 임계점 도달 대기" : "⏳ 이용약관에 먼저 동의해주세요")}
            </button>

        </div>
    );
};

export default LossScorecardIntegration;