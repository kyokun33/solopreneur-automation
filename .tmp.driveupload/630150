import React, { useState, useEffect, useCallback } from 'react';
import { FC } from 'react';

// --- 🛠️ Types and Constants (코드의 신뢰도를 높이기 위해 타입을 정의합니다)
interface LossScorecardProps {
    initialScore: number; // 초기 스코어 값 (예: 전체 리스크 점수)
    lossRatePerUnit: number; // 단위 시간/활동당 손실율 ($55/hour 같은 상수 사용)
    breachThreshold: number; // 경고 임계치 설정 (이 값이 넘으면 Red Alert 발동)
}

/**
 * @description LossScorecard 컴포넌트. Anti-Loss Funnel의 핵심 시각적 증거(Proof Point)를 제공합니다.
 * 스코어 카운트업 로직과, 임계치 초과 시 '데이터 브리치' 상태를 트리거하는 것이 핵심입니다.
 */
const LossScorecard: FC<LossScorecardProps> = ({ 
    initialScore, 
    lossRatePerUnit, 
    breachThreshold 
}) => {
    // [State] 현재 스코어와 브리치 상태를 관리합니다.
    const [currentScore, setCurrentScore] = useState(0);
    const [isBreached, setIsBreached] = useState(false);

    /**
     * @description 스코어를 부드럽게 카운트업하는 로직 (Animation Hook)
     * 이 함수는 단순 setState가 아니라, 사용자가 '계산 과정에 몰입'하게 만드는 것이 목적입니다. [근거: Self-RAG 64]
     */
    const animateScore = useCallback((targetValue: number) => {
        let startTime: number | null = null;

        // useEffect 내부에서 실행되도록 합니다.
        return (timestamp: number) => {
            if (!startTime) startTime = timestamp;
            const progress = Math.min(1, (timestamp - startTime) / 2000); // 2초 동안 카운트업 가정
            setCurrentScore(Math.floor(progress * targetValue));

            // 스코어 업데이트와 동시에 브리치 상태를 체크합니다.
            if (Math.floor(progress * targetValue) >= breachThreshold && !isBreached) {
                setIsBreached(true); // 임계값 도달 즉시 브리치 플래그 설정
            }

            if (progress < 1) {
                // 애니메이션을 계속 진행합니다.
                const timeout = setTimeout(() => animateScore(targetValue)(performance.now()), 16);
                return () => clearTimeout(timeout);
            } else {
                return; // 완료
            }
        };
    }, [breachThreshold, isBreached]);

    // 초기 마운트 시 애니메이션 실행 (MVP 로직)
    useEffect(() => {
        setCurrentScore(0);
        setIsBreached(false);
        const cleanup = window.requestAnimationFrame(animateScore(initialScore));
        return () => cancelAnimationFrame(cleanup);
    }, [initialScore, animateScore]);

    // 스코어에 따른 동적 클래스 적용 (CSS 연동 지점)
    const scoreColorClass = isBreached ? 'text-red-600' : 'text-gray-900'; 
    const containerAnimationClass = `transition-all duration-500 ${isBreached ? 'ring-4 ring-opacity-70 ring-[#CC3333] animate-pulse' : 'hover:shadow-xl'}`;

    return (
        <div className={`p-8 rounded-xl shadow-2xl max-w-md mx-auto border ${isBreached ? 'border-red-600' : 'border-gray-100'} ${containerAnimationClass}`}>
            {/* 🚨 핵심 위기감 조성 영역 */}
            <div className="text-center mb-6">
                <h2 className="text-sm uppercase tracking-widest text-gray-500 mb-2">
                    실시간 리스크 평가: Anti-Loss Score
                </h2>
                {/* 스코어 카운터 위젯 */}
                <div 
                    className={`relative inline-block p-4 ${isBreached ? 'bg-[#CC3333] text-white' : 'bg-gray-50'} rounded-lg`}
                    // 브리치 상태일 때 시각적 효과를 강화합니다. (CSS 애니메이션으로 구현 필요)
                >
                    <div className="relative z-10">
                        {/* 스코어 수치 */}
                        <span className={`text-6xl font-extrabold ${scoreColorClass}`}>{currentScore.toLocaleString()}</span>
                        <span className="text-lg text-gray-500 ml-2">/ 1,000 (Max)</span>
                    </div>
                    {/* 데이터 브리치 모션 오버레이 (이 부분이 핵심 애니메이션 대상입니다) */}
                    {isBreached && (
                        <div className="absolute inset-0 z-0 opacity-30 animate-glitch pointer-events-none"></div>
                    )}
                </div>
            </div>

            {/* 📊 손실 Breakdown 섹션 (스코어의 근거를 시각화) */}
            <div className="space-y-4 border-t pt-6 mt-6">
                <h3 className="text-xl font-semibold text-gray-700 mb-4">손실 원인 분석</h3>
                {/* 이 부분에 실제 차트 컴포넌트를 연결할 것입니다. */}
                <div className={`p-3 rounded ${isBreached ? 'bg-[#CC3333]/10' : 'bg-gray-50'} border border-red-200`}>
                    <p className="text-sm font-medium text-gray-700">🚨 경고: 데이터 무결성 손실 감지</p>
                    <p className={`text-xs mt-1 ${isBreached ? 'text-[#CC3333]' : 'text-gray-500'}`}>
                        현재 스코어는 임계치({breachThreshold.toLocaleString()})를 초과했습니다. 즉각적인 조치가 필요합니다!
                    </p>
                </div>
            </div>

            {/* 🚀 CTA (이득 기반) */}
             <button className={`w-full mt-8 py-3 rounded-lg font-bold transition duration-200 ${isBreached ? 'bg-red-700 hover:bg-red-800 text-white' : 'bg-indigo-600 hover:bg-indigo-700 text-white'}`}>
                손실 방지! 안전장치 자동 구현 가이드 확인하기 (예상 비용 계산)
            </button>
        </div>
    );
};

export default LossScorecard;