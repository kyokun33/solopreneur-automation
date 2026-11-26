import React from 'react';

// API 응답 스키마와 일치하도록 정의합니다.
interface DiagnosisResult {
    score: number;
    riskLevel: string;
    estimatedLossPotential: { annual: number, daily: number };
    vulnerabilityReport: Array<{ source: string, severity: string, description: string }>;
}

const ResultDisplay: React.FC<DiagnosisResult> = ({ result }) => {
    // 리스크 레벨에 따른 색상 매핑 (Self-RAG 근거)
    const getRiskColor = (level: string) => {
        switch(level) {
            case 'CRITICAL': return 'bg-[#CC3333] text-white'; // 손실 경고색
            case 'HIGH': return 'bg-yellow-500 text-gray-800';
            case 'MEDIUM': return 'bg-blue-500 text-white';
            default: return 'bg-green-500 text-white';
        }
    };

    return (
        <div className="p-10 max-w-3xl mx-auto bg-gray-50 shadow-2xl rounded-xl mt-8">
            <h2 className="text-4xl font-extrabold mb-4 text-[#0066CC]">✅ 진단 결과 보고서</h2>
            <p className="mb-8 text-lg text-gray-700">당신의 비즈니스 데이터 무결성 스코어는 **{result.score}%** 입니다.</p>

            {/* 1. 핵심 점수 카드 */}
            <div className={`p-6 rounded-xl mb-8 shadow-inner ${getRiskColor(result.riskLevel)}`}>
                <p className="text-sm uppercase opacity-90">종합 리스크 등급</p>
                <h3 className="text-5xl font-black mt-1">{result.riskLevel}</h3>
            </div>

            {/* 2. 예상 손실 잠재력 (가장 강력한 CTA 유도 지점) */}
            <div className="border border-[#CC3333] bg-red-50 p-6 rounded-lg mb-8 shadow-md">
                <h4 className="text-xl font-bold flex items-center text-[#CC3333]">
                    ⚠️ 잠재 손실액 추정 (Loss Potential) 
                </h4>
                <p className="text-sm text-gray-600 mt-1 mb-4">현재의 취약성을 개선하지 않을 경우 발생하는 최소 예상 비용입니다. [근거: Self-RAG - Loss Accent]</p>
                <div className="flex justify-between items-end pt-2 border-t border-red-200">
                    <div>
                        <span className="text-xl font-medium text-gray-600 block">연간 예상 손실액</span>
                        <span className="text-4xl font-extrabold text-[#CC3333]">${result.estimatedLossPotential.annual.toLocaleString()}</span>
                    </div>
                     <div>
                        <span className="text-xl font-medium text-gray-600 block">일일 예상 손실액</span>
                        <span className="text-4xl font-extrabold text-[#CC3333]">${result.estimatedLossPotential.daily.toLocaleString()}</span>
                    </div>
                </div>
            </div>

            {/* 3. 취약성 보고서 */}
            <div>
                <h4 className="text-2xl font-bold mb-4 border-b pb-2">🔍 상세 진단 항목 (Vulnerability Report)</h4>
                <div className='space-y-4'>
                    {result.vulnerabilityReport.map((item, index) => (
                        <div key={index} className="p-4 bg-white border-l-4 border-[#CC3333] shadow-sm">
                            <div className="flex justify-between items-center text-sm mb-1">
                                <span className="font-bold text-gray-800">{item.source}</span>
                                <span className={`px-3 py-1 text-xs font-semibold rounded ${item.severity === 'High' ? 'bg-[#CC3333]/90 text-white' : item.severity === 'Medium' ? 'bg-yellow-200 text-yellow-800' : 'bg-green-200 text-green-800'}`}>{item.severity}</span>
                            </div>
                            <p className="text-gray-700 text-sm">{item.description}</p>
                        </div>
                    ))}
                </div>
            </div>

             {/* 4. 최종 CTA */}
            <div className="mt-10 pt-6 border-t flex justify-center">
                 <button 
                    className="px-12 py-3 bg-[#0066CC] text-white font-bold rounded-lg hover:bg-blue-700 transition duration-200 shadow-xl"
                >
                    🚀 고고플랙스 전문가와 손실 예방 전략 상담하기 (무료)
                </button>
            </div>

        </div>
    );
};

export default ResultDisplay;