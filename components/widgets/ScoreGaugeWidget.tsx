/**
 * @description 최종 진단 점수를 시각화하는 게이지 컴포넌트. (Mockup V3.0 반영)
 * @param score - 현재 진단 점수 (0~100).
 */
import React from 'react';

interface ScoreGaugeWidgetProps {
  score: number;
}

const ScoreGaugeWidget: React.FC<ScoreGaugeWidgetProps> = ({ score }) => {
  // Mockup 스펙에 따라 색상 및 문구를 동적으로 변경합니다.
  let statusText = "안정적";
  let colorClass = "text-green-600";

  if (score < 50) {
    statusText = "경고: 심각한 데이터 누수 위험!";
    colorClass = "text-[#CC3333]"; // Loss Accent Color 사용
  } else if (score < 70) {
    statusText = "주의: 일부 개선 필요";
    colorClass = "text-yellow-600";
  }

  return (
    <div className="p-8 bg-white shadow-xl rounded-2xl border-b-4 border-[#CC3333]">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">데이터 무결성 점수</h2>
      {/* 게이지 시각화는 CSS와 상태에 따라 구현되어야 합니다. */}
      <div className="relative w-full h-12 bg-gray-200 rounded-full overflow-hidden mb-4">
        <div 
          className={`h-full transition-all duration-1000 ease-out ${colorClass}`} 
          style={{ width: `${score}%` }}
        ></div>
      </div>
      <p className="text-6xl font-extrabold mb-2">{score}</p>
      <p className={`text-lg font-semibold ${colorClass}`}>{statusText}</p>
    </div>
  );
};

export default ScoreGaugeWidget;