import React from 'react';
import { useLossCalculation } from './hooks/useLossCalculation';
import { LossScoreData } from '@/types/lossScoreCard';

/**
 * 계산된 손실 점수와 결과를 시각적으로 보여주는 컴포넌트 스캐폴딩입니다.
 */
const LossScoreResultDisplay: React.FC = () => {
    // 핵심 로직 훅을 재사용하여 현재 상태의 결과값 접근
    const { result } = useLossCalculation();

    return (
        <div className="p-6 border rounded-lg shadow-xl bg-white relative">
            <h2 className="text-2xl font-bold mb-4 text-red-700">📉 손실 점수 분석 결과</h2>
            
            {/* Red Warning 필터 로직 시각화 영역 */}
            {result.warningTriggered && (
                <div className="absolute top-0 left-0 w-full h-full bg-red-600 opacity-[0.15] pointer-events-none z-0 animate-pulse"></div>
            )}

            {/* 최종 손실액 표시 영역 - 가장 중요 */}
            <div className={`text-center py-8 ${result.warningTriggered ? 'bg-red-50 border-4 border-red-600' : ''} rounded-xl z-10`}>
                <p className="text-sm uppercase tracking-widest text-gray-500">예상 손실 총액 (Estimated Loss)</p>
                <div className={`text-7xl font-extrabold mt-2 ${result.warningTriggered ? 'text-red-800 animate-shake' : 'text-gray-900'}`}>
                    ${result.totalLossAmount.toLocaleString()}
                </div>
                <p className="text-lg text-gray-600 mt-1">USD</p>
            </div>

            {/* 손실 Breakdown 상세 정보 */}
            <div className="mt-8 space-y-4 z-10">
                <h3 className="text-xl font-semibold border-b pb-2 text-gray-700">손실 상세 내역 (Loss Breakdown)</h3>
                {Object.entries(result.lossBreakdown).map(([key, value]) => (
                    <div key={key} className="flex justify-between items-center py-2 border-b last:border-b-0">
                        <span className="text-gray-600">{key}:</span>
                        <span className="font-semibold text-lg">${value.toLocaleString()}</span>
                    </div>
                ))}
            </div>

            {/* CTA 영역 (가장 중요한 전환 지점) */}
            <div className={`mt-8 p-4 rounded-lg ${result.warningTriggered ? 'bg-red-100 border-l-4 border-red-600' : 'bg-green-50 border-l-4 border-green-600'}`}>
                <p className="font-bold text-gray-800">✅ 다음 단계:</p>
                <button 
                    className={`w-full py-3 rounded-lg font-bold transition duration-300 ${result.warningTriggered ? 'bg-red-600 hover:bg-red-700' : 'bg-indigo-600 hover:bg-indigo-700'} text-white`}
                    onClick={() => alert('진단 보고서 요청 API 호출 로직 구현 필요')}
                >
                    {result.warningTriggered ? '🔴 손실 방지 진단 보고서 요청하기 (필수)' : '🚀 자동화 시스템 구축 가이드 받기'}
                </button>
            </div>
        </div>
    );
};
export default LossScoreResultDisplay;