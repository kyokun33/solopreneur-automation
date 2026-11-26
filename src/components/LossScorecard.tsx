// LossScorecard.tsx
import React from 'react';
import ScoreGauge from './ScoreGauge';
import GlitchEffectOverlay from './GlitchEffectOverlay';
import { useLossSimulation } from '../hooks/useLossSimulation';

/**
 * Anti-Loss Funnel의 핵심 장치인 Loss Scorecard 프로토타입.
 * 데이터 시뮬레이션을 통해 위기감과 손실 인지를 극대화합니다.
 */
const LossScorecard: React.FC = () => {
    // 훅을 사용하여 현재 상태와 스코어 업데이트 기능을 가져옵니다.
    const [lossData, setScore] = useLossSimulation();

    return (
        <div className="max-w-4xl mx-auto p-8 bg-white shadow-2xl rounded-xl border border-gray-100 relative">
            
            {/* 🔴 Glitch Effect Overlay: Critical State 감지 시 전체 레이어 오버레이 */}
            <GlitchEffectOverlay isActive={lossData.isCritical} />

            <header className="text-center mb-12 z-10 relative">
                <h1 className={`text-5xl font-extrabold ${lossData.isCritical ? 'text-[#CC3333]' : 'text-gray-900'} transition-colors duration-500`}>
                    데이터 무결성 리스크 점검: Loss Scorecard 📉
                </h1>
                <p className="mt-4 text-xl text-gray-600">
                    현재 귀사의 데이터 시스템이 규제 및 보안 위협에 얼마나 노출되어 있는지 실시간으로 진단합니다.
                </p>
            </header>

            {/* 1. 스코어 게이지 섹션 */}
            <section className="mb-12 z-10 relative">
                <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b pb-2">🚨 핵심 리스크 점수</h2>
                {/* ScoreGauge 컴포넌트가 스코어와 애니메이션을 담당 */}
                <ScoreGauge data={lossData} /> 
            </section>

            {/* 2. 위기감 경고 및 설명 섹션 (Loss Breakdown) */}
            <section className="mb-16 z-10 relative bg-red-50 p-8 rounded-xl border-l-4 border-[#CC3333] shadow-md">
                <h3 className="text-2xl font-bold mb-3 text-[#CC3333]">🚨 시스템 경고 발생!</h3>
                <p className={`text-lg ${lossData.isCritical ? 'font-semibold' : 'text-gray-700'}`}>
                    {/* 위기감 메시지 표시 */}
                    {lossData.riskDescription}
                </p>
                <div className="mt-4 p-3 bg-red-100 text-[#CC3333] rounded">
                    ⚠️ **진단:** 현재 점수는 산업 평균 대비 ${Math.round(100 - lossData.score) / 5}배의 잠재적 손실을 의미합니다. 즉각적인 조치가 필요합니다.
                </div>
            </section>

            {/* 3. Call To Action (Anti-Loss Funnel CTA) */}
            <div className="text-center z-10 relative pt-8">
                <p className="text-xl mb-6 text-gray-700">
                    이 손실을 방지하고 데이터 주권을 확보하는 가장 확실한 방법은 시스템적 진단입니다.
                </p>
                {/* CTA: '구매하기' 대신 이득 기반의 구체적 행동 유도 문구 사용 */}
                <button 
                    className="w-full max-w-sm py-4 text-xl font-bold rounded-2xl bg-[#CC3333] hover:bg-red-700 transition duration-300 shadow-lg transform hover:scale-[1.02]"
                >
                    👉 15분 무료 규제 리스크 진단 예약하기 (지금 행동하여 손실 방지)
                </button>
            </div>
        </div>
    );
};

export default LossScorecard;