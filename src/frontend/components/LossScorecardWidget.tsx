import React, { useState, useEffect } from 'react';

// 백엔드 API 응답 계약 (Contract) 기반으로 타입을 정의합니다.
interface DiagnosisResult {
    status: 'AWARENESS' | 'WARNING' | 'CRITICAL';
    loss_scorecard: { total: number; breakdown: any[] };
    anti_loss_message: string;
    next_cta_state: string;
}

const LossScorecardWidget: React.FC = () => {
    const [result, setResult] = useState<DiagnosisResult | null>(null);
    const [loading, setLoading] = useState(true);

    // useEffect(() => { ... }, []) : 컴포넌트 마운트 시 API 호출을 시뮬레이션합니다.
    useEffect(() => {
        setLoading(true);
        // 실제로는 axios/fetch를 사용하여 f:\1인기업\src\backend\app\main:8000/api/diagnose_risk 로 POST 요청을 보냅니다.
        // 테스트가 통과했으므로, 일단 Mock 데이터를 사용합니다.
        setTimeout(() => {
            // [TEST] Critical 상태의 결과로 강제 설정하여 Funnel 시뮬레이션
            const mockResult: DiagnosisResult = {
                status: 'CRITICAL',
                loss_scorecard: { total: 1234567.89, breakdown: [] },
                anti_loss_message: "🚨 경고! 현재의 미진단 상태는 $1,234,567.89 규모의 즉각적인 법적 리스크에 노출되어 있습니다.",
                next_cta_state: 'Purchase_Funnel_Entry'
            };
            setResult(mockResult);
            setLoading(false);
        }, 1000);
    }, []);

    if (loading) {
        return <div className="text-xl text-gray-500">데이터 리스크를 분석 중입니다...</div>;
    }

    const totalLoss = result?.loss_scorecard.total || 0;

    // 핵심 로직: Anti-Loss 메시지를 가장 눈에 띄게 표시합니다.
    return (
        <div className="p-8 bg-white shadow-xl border-l-4 border-[#CC3333]">
            <h2 className="text-2xl font-bold mb-6 text-[#1D1D1F]">📊 손실 정량화 리스크 분석 결과</h2>

            {/* 1. 핵심 위젯: Loss Counter (Anti-Loss Hook) */}
            <div className="p-4 bg-gray-50 rounded-lg border border-red-200 mb-6">
                <p className="text-sm text-gray-600 uppercase tracking-wider">현재 잠재적 미진단 리스크</p>
                <h3 className="text-5xl font-extrabold mt-1 text-[#CC3333] transition duration-300 ease-out">
                    ${totalLoss.toLocaleString('en-US', { maximumFractionDigits: 2 })}
                </h3>
                <p className="mt-2 text-lg font-semibold">{result?.anti_loss_message}</p>
            </div>

            {/* 2. 리스크 Breakdown (시각적 증명) */}
            <div className="mb-8">
                <h4 className="text-xl font-bold mb-3 border-b pb-1">🔍 손실 구조 분석</h4>
                {/* 여기에 도넛 차트나 막대 그래프가 들어갈 자리입니다. */}
                <div className="text-gray-500 italic">
                    (데이터 무결성 리스크 및 규제 공백에 따른 상세 breakdown 섹션)
                </div>
            </div>

            {/* 3. CTA: Mini-Commitment Loop (강력한 행동 유도) */}
            <div className="mt-8 pt-6 border-t flex justify-between items-center">
                 <p className={`text-lg font-medium ${result?.status === 'CRITICAL' ? 'text-[#CC3333]' : 'text-gray-700'}`}>
                    다음 단계: {result?.next_cta_state} 상태로 진입하기 위해 필수 진단이 필요합니다.
                </p>
                <button 
                    className="px-8 py-3 bg-[#0066CC] text-white font-bold rounded-xl shadow-md hover:bg-[#004d99] transition duration-200"
                    onClick={() => console.log("Mini-Commitment Loop 진입")}
                >
                    💸 리스크 차단! 지금 즉시 전문진단 받기 (CTA)
                </button>
            </div>
        </div>
    );
};

export default LossScorecardWidget;