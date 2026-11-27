import React from 'react';
import { useLossCalculation } from './hooks/useLossCalculation';

/**
 * 손실 점수 계산에 필요한 사용자 입력 폼 컴포넌트의 스캐폴딩입니다.
 * 실제 API 호출 대신, 로컬 상태를 사용해 로직 검증을 목적으로 합니다.
 */
const LossScoreInputForm: React.FC = () => {
    // 핵심 로직 훅을 사용하여 state와 핸들러 접근
    const { input, handleInputChange } = useLossCalculation();

    return (
        <div className="p-6 border rounded-lg shadow-md bg-white">
            <h2 className="text-xl font-semibold mb-4">🔎 손실 요인 진단 (Input)</h2>
            {/* 시간 손실 입력 */}
            <div className="mb-4">
                <label htmlFor="timeSpent" className="block text-sm font-medium text-gray-700">시간 손실분 (누적 예상 시간, Hour)</label>
                <input
                    id="timeSpent"
                    type="number"
                    value={input.timeSpent || ''}
                    onChange={(e) => handleInputChange('timeSpent', e.target.value)}
                    className="mt-1 block w-full border p-2 rounded-md focus:ring-red-500 focus:border-red-500"
                />
            </div>

            {/* 리스크 레벨 입력 */}
            <div className="mb-6">
                <label htmlFor="riskLevel" className="block text-sm font-medium text-gray-700">리스크 수준 (1~10점, 10점이 가장 높음)</label>
                <input
                    id="riskLevel"
                    type="number"
                    min="1"
                    max="10"
                    value={input.riskLevel || ''}
                    onChange={(e) => handleInputChange('riskLevel', parseInt(e.target.value))}
                    className="mt-1 block w-full border p-2 rounded-md focus:ring-red-500 focus:border-red-500"
                />
            </div>

            {/* 손실 영역 선택 (Select/Radio) */}
            <div className="mb-4">
                <label htmlFor="lossArea" className="block text-sm font-medium text-gray-700 mb-2">가장 큰 손실 유발 영역</label>
                <select
                    id="lossArea"
                    value={input.area}
                    onChange={(e) => handleInputChange('area', e.target.value as any)}
                    className="mt-1 block w-full border p-2 rounded-md focus:ring-red-500 focus:border-red-500"
                >
                    <option value="데이터 무결성 리스크">🚨 데이터 무결성 리스크</option>
                    <option value="운영 비효율">⚙️ 운영 비효율 (프로세스 문제)</option>
                </select>
            </div>

        </div>
    );
};
export default LossScoreInputForm;