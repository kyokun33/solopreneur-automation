import React from 'react';

// 인터페이스 정의 (TypeScript 활용)
interface DiagnosisInputs {
    dataSilosCount: number; // 데이터 사일로 시스템 수
    manualProcessPoints: number; // 자동화되지 않은 수동 작업 포인트 수
    apiConnectionGaps: number; // API 연결이 누락된 핵심 서비스 간의 개수
}

const DiagnosisForm: React.FC = () => {
    // 실제 구현 시, 여기서 백엔드 API 호출 로직(fetch/axios)을 처리합니다.
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("--- [API Call Simulation] ---");
        const formData: DiagnosisInputs = {
            dataSilosCount: parseInt((document.getElementById('silos').value) || '0'),
            manualProcessPoints: parseInt((document.getElementById('manual').value) || '0'),
            apiConnectionGaps: parseInt((document.getElementById('gaps').value) || '0')
        };

        // [TODO] 실제 API 호출 로직 구현 (ex: axios.post('/api/v1/diagnose_data', formData))
        console.log(`진단 요청 전송: 사일로=${formData.dataSilosCount}, 수동점=${formData.manualProcessPoints}`);
        alert("데이터가 성공적으로 백엔드 API로 전송되었습니다. (실제 구현 필요)");
    };

    return (
        <div className="p-8 max-w-xl mx-auto bg-white shadow-lg rounded-xl">
            <h2 className="text-3xl font-bold mb-6 text-[#0066CC]">📊 데이터 무결성 진단</h2>
            <p className="mb-8 text-gray-600">현재 비즈니스 프로세스의 취약점을 숫자로 진단하여 잠재적 손실을 확인하세요.</p>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* 1. 데이터 사일로 */}
                <div>
                    <label htmlFor="silos" className="block text-sm font-medium text-gray-700 mb-2">
                        데이터가 분리된 시스템 개수 (예: CRM, 재무, 마케팅) * [근거: Writer Script 1]
                    </label>
                    <input id="silos" type="number" min="0" value={0} onChange={(e) => {}} className="w-full p-3 border border-gray-300 rounded-lg focus:ring-[#CC3333] focus:border-[#CC3333]" required />
                    <p className="text-xs text-gray-500 mt-1">시스템이 분리될수록 데이터 단절로 인한 손실 위험이 증가합니다.</p>
                </div>

                {/* 2. 수동 프로세스 */}
                <div>
                    <label htmlFor="manual" className="block text-sm font-medium text-gray-700 mb-2">
                        자동화되지 않은 수작업 입력 포인트 개수 * [근거: Writer Script 2]
                    </label>
                    <input id="manual" type="number" min="0" value={0} onChange={(e) => {}} className="w-full p-3 border border-gray-300 rounded-lg focus:ring-[#CC3333] focus:border-[#CC3333]" required />
                    <p className="text-xs text-gray-500 mt-1">수동 입력은 '휴먼 에러'의 가장 큰 원인입니다. 이 지점을 찾아야 합니다.</p>
                </div>

                {/* 3. API 연결 누락 */}
                <div>
                    <label htmlFor="gaps" className="block text-sm font-medium text-gray-700 mb-2">
                        핵심 서비스 간의 데이터 흐름 단절 지점 (API Gap) 개수 * [근거: 지난 의사결정 로그]
                    </label>
                    <input id="gaps" type="number" min="0" value={0} onChange={(e) => {}} className="w-full p-3 border border-gray-300 rounded-lg focus:ring-[#CC3333] focus:border-[#CC3333]" required />
                    <p className="text-xs text-gray-500 mt-1">데이터가 흐르지 않는 '틈'이 가장 위험합니다. 전방위적 연결을 확인하세요.</p>
                </div>

                <button 
                    type="submit" 
                    className="w-full py-3 bg-[#CC3333] text-white font-bold rounded-lg hover:bg-red-700 transition duration-200 mt-8 shadow-md"
                >
                    ⚠️ 데이터 무결성 진단 실행 (Scorecard)
                </button>
            </form>
        </div>
    );
};

export default DiagnosisForm;