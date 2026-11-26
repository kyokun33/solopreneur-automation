// ScoreGauge.tsx
import React from 'react';
import { LossData } from '../hooks/useLossSimulation';

interface ScoreGaugeProps {
    data: LossData;
}

/**
 * 스코어 점수를 시각적으로 보여주는 게이지 컴포넌트.
 * Critical State에 따라 색상과 애니메이션이 변경됩니다.
 */
const ScoreGauge: React.FC<ScoreGaugeProps> = ({ data }) => {
    const score = data.score;
    let colorClass = 'bg-blue-600'; // Default Color (Normal Zone)

    if (data.isCritical) {
        colorClass = 'bg-[#CC3333] animate-[pulse_1s_infinite]'; // Critical Red Warning
    } else if (score < 50) {
        colorClass = 'bg-yellow-600'; // Caution Zone
    }

    // 게이지의 너비(width)를 스코어 비율에 맞게 계산합니다.
    const gaugeWidthStyle: React.CSSProperties = { width: `${score}%` };

    return (
        <div className="w-full p-4 bg-gray-100 rounded-xl shadow-inner">
            <div className="flex justify-between items-center mb-2 text-sm font-medium text-gray-600">
                <span>Loss Scorecard</span>
                <span className={`text-3xl ${data.isCritical ? 'text-[#CC3333] animate-[pulse_1s_infinite]' : 'text-blue-700'}`}>{score} / 100</span>
            </div>

            {/* 게이지 바 */}
            <div className="h-8 bg-gray-200 rounded-full relative">
                <div 
                    className={`absolute top-0 left-0 h-full rounded-l-full transition-all duration-1000 ease-out shadow-lg ${colorClass}`} 
                    style={gaugeWidthStyle}
                ></div>
            </div>
        </div>
    );
};

export default ScoreGauge;