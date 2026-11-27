import React, { useState } from 'react';
import DynamicDisplayWidget from '../components/DynamicDisplayWidget';
import { calculateMockLossScore, CalculationInput, LossReport } from '../services/mockLossCalculation';

// 초기 상태 정의 (전역 변수화)
const INITIAL_LOSS_SCORE = 0;

/**
 * @component LossCalculatorPage
 * @description 전체 MVP 프로토타입을 구성하며, 사용자 입력 -> 계산 로직 호출 -> 위젯 업데이트 사이클을 관리합니다.
 */
export default function LossCalculatorPage() {
  const [isLoading, setIsLoading] = useState(false);
  // 현재까지 기록된 손실 보고서와 점수
  const [currentReport, setCurrentReport] = useState<LossReport | null>(null);

  // 1. 핸들러: 리스크 계산 로직 트리거
  const handleCalculateRisk = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // 2. 입력값 추출 및 유효성 검증 (Guard Clause)
    const hoursInput = parseFloat((e.target as HTMLFormElement).elements['hoursOfVulnerability'] as HTMLInputElement)?.value || 0;
    const riskSelect = (e.target as HTMLFormElement).elements['dataIntegrityRiskLevel'] as HTMLSelectElement;
    const selectedRisk = riskSelect.value as 'low' | 'medium' | 'high';

    if (hoursInput <= 0) {
        alert("⚠️ 경고: 노출 시간을 입력해야 합니다.");
        setIsLoading(false);
        return;
    }

    // 3. Mock API 호출 및 데이터 수신
    try {
      const mockReport = await calculateMockLossScore({
        hoursOfVulnerability: hoursInput,
        dataIntegrityRiskLevel: selectedRisk,
      });

      setCurrentReport(mockReport); // 보고서 상태 업데이트
    } catch (error) {
      console.error("Calculation Failed:", error);
      alert("❌ 리스크 계산에 실패했습니다. 잠시 후 다시 시도해 주세요.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-12">
      {/* Header */}
      <header className="max-w-6xl mx-auto mb-12 text-center">
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight">
            🚨 법적 리스크 자동 진단 시스템 <span className="text-[#CC3333]">Loss Scorecard</span>
        </h1>
        <p className="mt-4 text-xl text-gray-600">
          당신의 데이터 관리 상태가 놓치고 있는 '돈으로 환산되는 법적 책임'을 즉시 확인하세요.
        </p>
      </header>

      {/* 메인 콘텐츠 영역: 입력폼과 결과 위젯 분리 */}
      <main className="max-w-6xl mx-auto grid md:grid-cols-2 gap-12 items-start">
        
        {/* Left Column: 사용자 Input Form (데이터 입력) */}
        <section className="p-8 bg-white shadow-lg rounded-xl border border-gray-200">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">1. 데이터 취약성 진단 (Input Data)</h2>
          <form onSubmit={handleCalculateRisk} className="space-y-6">
            {/* 1. 노출 시간 입력 */}
            <div>
              <label htmlFor="hoursOfVulnerability" className="block text-sm font-medium text-gray-700 mb-2">
                데이터 무방비 노출 예상 시간 (Hours of Vulnerability) *
              </label>
              <input 
                type="number" 
                id="hoursOfVulnerability" 
                name="hoursOfVulnerability" 
                required 
                min="0.1" 
                step="0.5"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-[#CC3333] focus:border-[#CC3333] transition duration-150" 
              />
            </div>

            {/* 2. 리스크 레벨 선택 */}
            <div>
              <label htmlFor="dataIntegrityRiskLevel" className="block text-sm font-medium text-gray-700 mb-2">
                데이터 무결성 리스크 수준 (Data Integrity Risk Level) *
              </label>
              <select 
                id="dataIntegrityRiskLevel" 
                name="dataIntegrityRiskLevel" 
                required
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-[#CC3333] focus:border-[#CC3333] transition duration-150 appearance-none bg-white cursor-pointer"
              >
                <option value="" disabled>리스트를 선택해 주세요</option>
                <option value="low">낮음 (Low)</option>
                <option value="medium">중간 (Medium) - 일반적인 관리 소홀 수준</option>
                <option value="high">높음 (High) - 법적 문제 발생 가능성이 높은 구조적 결함</option>
              </select>
            </div>

            {/* 3. 버튼 */}
            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-3 rounded-lg text-white font-bold transition duration-200 ${
                isLoading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-[#CC3333] hover:bg-[#b32d2d]'
              }`}
            >
              {isLoading ? '⚙️ 리스크 계산 중... (API 통신 시뮬레이션)' : '📊 손실 점수 계산 및 진단 시작'}
            </button>

          </form>
        </section>

        {/* Right Column: 동적 결과 위젯 (Dynamic Feedback) */}
        <section className="md:sticky md:top-10 h-[450px]">
           <h2 className="text-2xl font-bold mb-6 text-gray-800">2. 진단 보고서 (Calculated Loss Report)</h2>
          {/* DynamicDisplayWidget 컴포넌트 사용 */}
          <DynamicDisplayWidget 
            currentScore={INITIAL_LOSS_SCORE} // 초기값 전달
            newReport={currentReport}      // 계산된 결과물 전달
          />
        </section>
      </main>

       {/* Footer CTA (Transition to Resolution) */}
      <footer className="max-w-6xl mx-auto mt-12 pt-8 border-t text-center">
         <button 
            className="py-3 px-10 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition duration-200 shadow-md"
         >
             ➡️ [해결책 요청] 법률 전문가의 정밀 진단 리포트 받기 (CTA)
         </button>
      </footer>

    </div>
  );
}