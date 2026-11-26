/**
 * @description Loss Potential 위젯: 사용자의 불안감을 극대화하는 핵심 인터랙션 컴포넌트. (Mockup V3.0 반영)
 * @param totalEstimate - 총 예상 손실액 ($).
 */
import React, { useState } from 'react';

interface LossPotentialWidgetProps {
  totalEstimate: number;
}

const LossPotentialWidget: React.FC<LossPotentialWidgetProps> = ({ totalEstimate }) => {
  // 초기에는 로딩 상태를 시뮬레이션하고, 데이터가 들어오면 숫자가 카운트업되는 애니메이션이 필요합니다.
  const [displayValue, setDisplayValue] = useState(0);

  React.useEffect(() => {
    // Mockup 스펙에 맞춰 '카운트업' 로직을 적용합니다.
    let current = 0;
    const interval = setInterval(() => {
      current += Math.round(totalEstimate / 20); // 부드러운 증가 시뮬레이션
      setDisplayValue(current);

      if (current >= totalEstimate) {
        clearInterval(interval);
      }
    }, 50);
    return () => clearInterval(interval);
  }, [totalEstimate]);


  // Mockup 스펙에 따라 손실 금액은 가장 강조되어야 합니다.
  const formattedLoss = `$${displayValue.toLocaleString()}`;

  return (
    <div className="bg-red-50 border-l-4 border-[#CC3333] p-6 shadow-inner">
      <h3 className="text-xl font-bold mb-2 text-[#CC3333]">🚨 당신의 잠재적 손실 위험</h3>
      <p className="text-sm text-gray-600 mb-4">현재 데이터 상태로만 예측 가능한, 미확인된 리스크 비용입니다.</p>
      
      {/* 핵심 값 강조 */}
      <div className="flex items-baseline space-x-2">
        <span className="text-5xl font-extrabold text-[#CC3333] transition duration-500">{formattedLoss}</span>
        <span className="text-lg font-semibold text-gray-700"> (예상 비용)</span>
      </div>

      {/* Hover 시 상세 설명 팝업 로직이 이 영역에 추가되어야 합니다. */}
    </div>
  );
};

export default LossPotentialWidget;