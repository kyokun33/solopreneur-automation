import React, { useState, useMemo } from 'react';
import { diagnoseAntiLossStatus, calculateEstimatedLoss } from './utils/lossCalculator';
// Tailwind CSS 스타일링을 사용한다고 가정하고 컴포넌트를 설계합니다.

interface AntiLossProps {}

const AntiLossLandingPage: React.FC<AntiLossProps> = () => {
    // 1. State Management: 사용자 입력값 상태 정의
    const [timeInput, setTimeInput] = useState<string>(null); // 시간(시간 단위)
    const [inputAmount, setInputAmount] = useState<number | null>(null); // 수동 손실액

    // 2. Core Logic Execution: useMemo를 사용하여 입력값이 바뀔 때만 재계산하도록 최적화합니다.
    const diagnosisResult = useMemo(() => {
        let calculatedLoss = 0;
        if (timeInput) {
            const timeHours = parseFloat(timeInput);
            calculatedLoss = calculateEstimatedLoss(timeHours); // 시간 기반 계산을 우선 적용
        }

        // 수동 입력된 손실액과 자동 계산된 손실액 중 더 큰 값을 '진짜' 손실로 간주합니다.
        const effectiveLoss = inputAmount === null ? calculatedLoss : Math.max(calculatedLoss, inputAmount);

        return diagnoseAntiLossStatus(effectiveLoss);
    }, [timeInput, inputAmount]); // 의존성 배열에 상태 변수 포함

    // 3. 핸들러 함수 정의 (User Interaction)
    const handleTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTimeInput(e.target.value);
        setInputAmount(null); // 시간이 바뀌면 수동 입력값 초기화
    };

    const handleManualLossChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = parseFloat(e.target.value) || 0;
        setInputAmount(value);
        setTimeInput(null); // 수동 값이 바뀌면 시간 입력값 초기화
    };

    return (
        <div className="min-h-screen bg-gray-50 font-sans">
            {/* ==================== A. Hero Section: 손실의 충격과 위기감 조성 ==================== */}
            <header className="py-24 md:py-36 text-center bg-white border-b border-red-100/50">
                <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-[#1D1D1F] mb-4">
                    🚨 당신의 비즈니스가 지금 놓치고 있는 '진짜' 위험 비용은 얼마입니까?
                </h1>
                <p className="max-w-3xl mx-auto text-xl text-gray-600 mb-12">
                    단순한 수익 감소가 아닙니다. 시스템 구조적 취약성(Structural Vulnerability)으로 인한 
                    **데이터 무결성 및 시간 자산의 손실**입니다. 이 비용을 놓치고 계십니다.
                </p>

                {/* 핵심 위젯: Loss Counter (시각화 강조) */}
                <div className="bg-red-50 p-8 rounded-xl shadow-2xl max-w-md mx-auto border-4 border-dashed border-red-300/70 mb-16">
                    <p className="text-sm uppercase text-red-600 tracking-widest font-semibold">추정 손실액 (Estimated Loss)</p>
                    <div className="mt-2 flex justify-center items-end gap-4">
                        <input 
                            type="number" 
                            placeholder="손실 금액 입력 (선택)" 
                            value={inputAmount ?? ''}
                            onChange={handleManualLossChange}
                            className={`w-full p-3 border-2 rounded-lg text-right ${diagnosisResult.status === 'CRITICAL' ? 'border-red-500 bg-red-100' : 'border-gray-300'}`}
                        />
                        <div className="relative pt-1">
                            <label htmlFor="time-input" className="block text-xs uppercase tracking-widest text-gray-500">시간 (h)</label>
                            <input 
                                id="time-input" 
                                type="number" 
                                placeholder="예: 10" 
                                value={timeInput ?? ''}
                                onChange={handleTimeChange}
                                className={`w-full p-3 border-2 rounded-lg text-right ${diagnosisResult.status === 'CRITICAL' ? 'border-red-500 bg-red-100' : 'border-gray-300'}`}
                            />
                        </div>
                    </div>

                    <p className="text-4xl font-bold mt-6 text-[#CC3333] transition duration-500 ease-out">
                        {Math.round(diagnosisResult.message.match(/\d+/g)?.[0] || 0)}만 원
                    </p>
                </div>
            </header>

            {/* ==================== B. Diagnostic Result Section: Funnel 핵심 로직 작동 영역 ==================== */}
            <main className="container mx-auto px-4 py-20">
                <section className="text-center mb-20 border-b pb-16">
                    <h2 className="text-3xl lg:text-4xl font-bold text-[#1D1D1F] mb-4">🚨 현재 손실 진단 결과</h2>
                    <p className="text-lg text-gray-700 mb-12 max-w-2xl mx-auto">{diagnosisResult.message}</p>

                    {/* 진단 결과 섹션 */}
                    <div className={`p-8 rounded-xl shadow-inner transition duration-500 ${diagnosisResult.status === 'CRITICAL' ? 'bg-red-50 border-4 border-red-300/70' : diagnosisResult.status === 'WARNING' ? 'bg-yellow-50 border-4 border-yellow-300/70' : 'bg-green-50 border-4 border-green-300/70'} max-w-xl mx-auto`}>
                        <h3 className="text-2xl font-bold mb-4 text-[#1D1D1F]">진단 보고서: {diagnosisResult.status === 'CRITICAL' ? '위험 단계 (Critical)' : diagnosisResult.status === 'WARNING' ? '주의 단계 (Warning)' : '안전 단계 (Safe)'}</h3>
                        <p className="text-xl mb-6 text-gray-700">{diagnosisResult.message}</p>
                        {diagnosisResult.details && <div className="mb-8">{diagnosisResult.details}</div>}

                        {/* CTA 버튼: 가장 중요한 전환 장치 */}
                        <button 
                            className={`px-12 py-4 text-lg font-bold rounded-xl shadow-md transition duration-300 ${
                                diagnosisResult.status === 'CRITICAL' 
                                ? 'bg-[#CC3333] hover:bg-red-700 text-white transform scale-105' 
                                : diagnosisResult.status === 'WARNING'
                                ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                                : 'bg-blue-600 hover:bg-blue-700 text-white'
                            }`}
                            onClick={() => alert(`CTA 클릭! ${diagnosisResult.ctaText}를 위한 폼 제출 로직 실행.`)}
                        >
                            {diagnosisResult.ctaText || "진단 리포트 받기"}
                        </button>
                    </div>
                </section>
            </main>

             {/* ==================== C. Final CTA Section: 강력한 마무리 유도 ==================== */}
            <footer className="bg-gray-900 py-24 text-center">
                 <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">더 이상 손실을 '우발적'이라고 치부하지 마세요.</h2>
                <p className="text-lg text-gray-400 mb-10 max-w-2xl mx-auto">
                    손실은 언제나 구조적인 취약점(Structural Vulnerability)에서 시작됩니다. 고고플랙스가 당신의 비즈니스를 점검합니다.
                </p>
                <button 
                    className="px-16 py-5 text-xl font-bold rounded-full shadow-lg transition duration-300 bg-[#CC3333] hover:bg-red-700 text-white transform hover:scale-105"
                    onClick={() => alert("최종 CTA 클릭! 전용 예약 폼 페이지로 리다이렉트됩니다.")}
                >
                   지금, 당신의 비즈니스를 진단받기
                </button>
            </footer>
        </div>
    );
};

export default AntiLossLandingPage;