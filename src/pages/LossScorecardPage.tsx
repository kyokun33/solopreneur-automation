import React, { useState, useEffect } from 'react';
import useLossSimulation from '../hooks/useLossSimulation';
import GlitchEffectOverlay from '../components/GlitchEffectOverlay';
import ScoreGauge from '../components/ScoreGauge';
import LossScorecard from '../components/LossScorecard';

// Mock API Call: 실제 데이터 로딩 시뮬레이션
const fetchRiskData = async () => {
    console.log("Fetching comprehensive risk data...");
    await new Promise(resolve => setTimeout(resolve, 1500)); // 네트워크 지연 시뮬레이션
    return {
        timeLostHours: 8.5, // 예시 데이터
        dataBreachCount: 4, // 예시 데이터
        riskCategory: "AI 규제 및 데이터 주권 침해 리스크",
        potentialLossAmountKRW: 12300000, // ₩12,300,000 (강력한 숫자)
    };
};

const LossScorecardPage: React.FC = () => {
    // 상태 관리: 로딩 및 데이터
    const [loading, setLoading] = useState(true);
    const [riskData, setRiskData] = useState<any>(null);
    const [isBreachActive, setIsBreachActive] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            const data = await fetchRiskData();
            setRiskData(data);
            // 데이터 로딩 완료 후 브리치 효과 발동 시뮬레이션 (QA 테스트 포인트)
            setTimeout(() => {
                setIsBreachActive(true); // Red Warning/Glitch 시작
                console.log("🚨 Data Breach Simulation Triggered!");
            }, 500);
        };

        loadData();
    }, []);

    // Loss Simulation Hook 사용 (컴포넌트에서 이미 로직을 가져옴)
    const { totalLossAmount, timeLost } = useLossSimulation(riskData?.timeLostHours || 0);

    return (
        <div className="min-h-screen bg-gray-50 p-4 sm:p-8 relative">
            {/* Data Breach Overlay - Red Warning Filter가 여기에서 작동해야 함 */}
            <GlitchEffectOverlay active={isBreachActive} intensity={Math.max(1, Math.floor(Math.random() * 10))}>
                {/* 메인 콘텐츠 시작 */}
                <div className="relative z-10 max-w-6xl mx-auto bg-white p-8 sm:p-12 rounded-xl shadow-2xl">

                    {/* 1. Hero Section (Loss Counter - 최우선 노출) */}
                    <section className="text-center py-16 border-b border-gray-200 mb-12">
                        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 mb-4 tracking-tight">
                            당신의 데이터, 지금 몇 원의 가치를 잃었습니까?
                        </h1>
                        <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
                            AI 시대, 보이지 않는 리스크가 가장 큰 금전적 손실입니다. 수치로 확인하세요.
                        </p>

                        {/* Loss Counter Widget */}
                        <div className="bg-red-50 border-4 border-dashed border-[#CC3333] p-8 rounded-xl shadow-inner">
                            <h2 className="text-2xl font-semibold text-[#CC3333] mb-4 uppercase tracking-widest">총 예상 손실액 (Estimated Loss)</h2>
                            <div className="flex justify-center items-baseline">
                                <span className="text-6xl sm:text-8xl font-mono font-bold text-[#CC3333]">
                                    {totalLossAmount.toLocaleString('ko-KR')}원
                                </span>
                                <span className="ml-4 text-lg text-gray-500">₩</span>
                            </div>
                            <p className="text-sm mt-2 text-red-700 font-medium">(시간 손실분 + 리스크 비용)</p>
                        </div>
                    </section>

                    {/* 2. Scorecard & Gauge */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-10 mb-16 items-center">
                        <div className="lg:col-span-2">
                            <h3 className="text-3xl font-bold text-gray-800 mb-6 border-b pb-2">🔥 리스크 스코어카드 진단</h3>
                            {/* Score Gauge Component */}
                            <ScoreGauge riskLevel={riskData?.dataBreachCount || 0} />
                        </div>
                        <div className="lg:col-span-1 bg-gray-50 p-6 rounded-xl shadow">
                             <h3 className="text-2xl font-bold text-[#CC3333] mb-4 flex items-center">
                                <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 110-12 6 6 0 010 12z"></path></svg>
                                데이터 브리치 경고 레벨
                            </h3>
                             <p className="text-5xl font-extrabold text-[#CC3333] mt-4">{riskData?.dataBreachCount || 0} 건</p>
                             <p className="text-gray-500 mt-2">최근 감지된 잠재적 데이터 유출/취약점.</p>
                        </div>
                    </div>

                    {/* 3. Loss Breakdown (Chart Area) */}
                    <section className="mb-16 border-t pt-8">
                        <h3 className="text-2xl font-bold text-gray-800 mb-6">📊 손실 원인 분석 (Loss Breakdown)</h3>
                        {/* Chart Component - 이 부분은 나중에 구현할 차트 라이브러리 연동이 필요함 */}
                        <div className="bg-gray-100 p-6 rounded-xl h-64 flex items-center justify-center text-gray-500">
                            [여기에 손실 Breakdown (도넛/파이 차트)가 구현됩니다. 애니메이션 필수.]
                        </div>
                    </section>

                     {/* 4. Call To Action (Final Funnel) */}
                    <div className="text-center py-12 bg-[#CC3333] rounded-b-xl shadow-lg">
                        <h2 className="text-3xl font-bold text-white mb-4">손실을 막는 유일한 방법은 '선제적 행동'입니다.</h2>
                        <button 
                            className="px-10 py-3 bg-yellow-400 text-[#CC3333] font-extrabold rounded-full shadow-xl hover:bg-yellow-300 transition duration-200"
                            onClick={() => alert("서비스 가입 및 진단 시작!")}
                        >
                           ✅ 지금 바로 리스크 무료 진단받기 (클릭)
                        </button>
                    </div>

                </div>
            </LossScorecardPage>
        </div>
    );
};

export default LossScorecardPage;