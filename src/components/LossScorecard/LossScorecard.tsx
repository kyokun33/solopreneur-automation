import React, { useState, useEffect, useMemo } from 'react';
import { LossScorecardProps, ScorecardState, RiskLevel } from './types';

// --- 🐛 Utility: Pure State Calculation Logic (테스트 가능 영역) ---

/**
 * @description 입력 데이터를 기반으로 리스크 레벨과 점수를 계산하는 순수 함수.
 * 이 로직은 UI와 완전히 분리되어야 합니다.
 */
const calculateScorecardState = (data: Record<string, number>): ScorecardState => {
  if (!data || Object.keys(data).length === 0) {
    // [Exception Handling]: 입력 데이터가 없을 경우 기본 상태 반환
    return { score: 0, level: 'initial', message: "데이터를 로드하여 리스크를 진단하세요." };
  }

  let totalLoss = Object.values(data).reduce((sum, val) => sum + (typeof val === 'number' ? val : 0), 0);
  let level: RiskLevel;
  let message: string;

  // [State Transition Logic]: 점수 변화에 따른 레벨 결정 로직
  if (totalLoss >= 5000) {
    level = 'critical';
    message = "🚨 치명적 리스크 감지! 즉각적인 조치가 필요합니다. 법적 책임 증명이 시급합니다.";
  } else if (totalLoss >= 1000) {
    level = 'warning';
    message = "⚠️ 주의: 데이터 무결성에 문제가 있습니다. 잠재적 손실이 발생할 수 있습니다.";
  } else {
    level = 'initial';
    message = "✅ 현재 리스크는 안정권입니다. 하지만 사소한 누락도 큰 문제로 이어질 수 있습니다.";
  }

  return { score: Math.round(totalLoss), level, message };
};


// --- 🎨 Core Component ---

const LossScorecard: React.FC<LossScorecardProps> = ({ inputData }) => {
  // [State Management]: 현재 상태를 저장하고, Props 변화에 따라 리렌더링합니다.
  const [currentState, setCurrentState] = useState<ScorecardState>(() => calculateScorecardState(inputData));
  
  /** 
   * [useEffect Hook]: Input data가 변경되거나 컴포넌트 마운트 시 스코어 계산을 트리거합니다.
   */
  useEffect(() => {
    try {
      // [Core Logic Execution]
      const newState = calculateScorecardState(inputData);
      setCurrentState(newState);
    } catch (error) {
      // [Exception Handling]: 로직 실행 중 치명적 오류 발생 시, 사용자에게 명확한 에러 메시지 표시
      console.error("Loss Scorecard Calculation Error:", error);
      setCurrentState({ 
        score: -1, 
        level: 'critical', 
        message: "❌ 시스템 오류가 감지되었습니다. 관리자에게 문의하세요." 
      });
    }
  }, [inputData]); // inputData가 변경될 때마다 재실행

  // [UI Rendering Logic]
  const { score, level, message } = currentState;

  /**
   * @description 리스크 레벨에 따른 동적 CSS 클래스를 반환합니다.
   */
  const getLevelClasses = (level: RiskLevel) => {
    switch (level) {
      case 'critical': return "bg-red-900/80 text-white border-red-600 shadow-red-700/50";
      case 'warning':  return "bg-yellow-100 text-yellow-900 border-yellow-400 shadow-yellow-300/50";
      case 'initial':  return "bg-green-50 text-green-800 border-green-200 shadow-green-100/50";
    }
  };

  // [Animation Placeholder]: 실제 애니메이션은 CSS Keyframes와 Intersection Observer를 사용해야 하므로, 
  // 여기서는 클래스 네임으로만 구현하고 주석 처리합니다.
  const containerClasses = `relative p-8 rounded-xl border-l-8 transition duration-500 transform ${getLevelClasses(level)} animate-fade-in`;


  return (
    <div className={containerClasses}>
      {/* 1. 헤드라인/경고 메시지 영역 */}
      <div className="mb-6">
        <h2 className="text-xl font-bold flex items-center">
          <span className={`mr-2 ${level === 'critical' ? 'animate-pulse' : ''}`}>🚨</span> 
          데이터 무결성 리스크 진단 결과
        </h2>
      </div>

      {/* 2. 핵심 스코어 카운터 위젯 (가장 중요) */}
      <div className="text-center mb-8">
        <p className="text-sm uppercase tracking-wider opacity-70">현재 예상 손실 비용</p>
        <h1 
            className={`text-6xl md:text-8xl font-extrabold mt-2 transition-all duration-500 ease-out ${level === 'critical' ? 'animate-glitch' : ''}`}
            // [애니메이션 지점]: 실제 구현에서는 이 숫자가 카운트업 애니메이션을 가져야 합니다.
        >
          ${score.toLocaleString()}
        </h1>
        <p className="text-xl mt-2">달러 (Estimated Cost)</p>
      </div>

      {/* 3. 상태 변화 메시지 및 CTA */}
      <div className="mb-6 p-4 border-l-4 bg-white/50 rounded-lg shadow-inner">
        <h3 className="font-semibold text-lg mb-1 flex items-center">
            {/* Red Warning 필터 효과를 시뮬레이션 */}
            <span className={`mr-2 ${level === 'critical' ? 'text-red-700' : 'text-gray-600'} transition duration-300`}>
                {level === 'critical' ? '🛑' : (level === 'warning' ? '⚠️' : '✅')}
            </span>
            진단 메시지: {message}
        </h3>
      </div>

      {/* 4. 입력 데이터 시뮬레이션 및 테스트 버튼 (즉시 테스트 가능하도록) */}
       <div className="mt-8 pt-6 border-t border-opacity-30">
           <h4 className='text-sm uppercase tracking-wider mb-3'>테스트용 리스크 요인 조정</h4>
           {/* 실제 앱에서는 이 데이터를 백엔드 API 호출로 받아와야 합니다. */}
           <button 
               onClick={() => {
                   // Critical State 시뮬레이션: 큰 값 입력 (5000달러 이상)
                   setCurrentState({ score: 6200, level: 'critical', message: "🚨 치명적 리스크 감지! 즉각적인 조치가 필요합니다. 법적 책임 증명이 시급합니다." });
               }}
               className="mr-4 px-5 py-2 bg-red-700 text-white rounded hover:bg-red-800 transition"
           >
                [테스트] Critical State (고의 손실) 💻
           </button>
            <button 
               onClick={() => {
                   // Warning State 시뮬레이션: 중간 값 입력 (1000~5000달러)
                   setCurrentState({ score: 2800, level: 'warning', message: "⚠️ 주의: 데이터 무결성에 문제가 있습니다. 잠재적 손실이 발생할 수 있습니다." });
               }}
               className="mr-4 px-5 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition"
           >
                [테스트] Warning State (중간 손실) ⚙️
           </button>
             <button 
               onClick={() => {
                   // Initial State 시뮬레이션: 낮은 값 입력 (1000달러 미만)
                   setCurrentState({ score: 450, level: 'initial', message: "✅ 현재 리스크는 안정권입니다. 하지만 사소한 누락도 큰 문제로 이어질 수 있습니다." });
               }}
               className="px-5 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
           >
                [테스트] Initial State (안정) ✅
           </button>
       </div>

    </div>
  );
};

export default LossScorecard;