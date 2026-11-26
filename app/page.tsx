// Next.js App Router의 서버 컴포넌트 기반으로 작성됩니다.
"use client"; // 클라이언트 측 상호작용이 많으므로 'use client'를 선언합니다.

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { fetchDiagnosisData } from '@/lib/api/diagnosisService'; // API 서비스 레이어 임포트
import { AntiLossFunnelVisualization } from '@/components/widgets/AntiLossFunnelVisualization'; // 가상 컴포넌트

// 동적 임포트를 사용하여 클라이언트 측에서만 작동하는 위젯을 로드합니다. (SSR 방지)
const ScoreGaugeWidget = dynamic(() => import('@/components/widgets/ScoreGaugeWidget'), { ssr: false });
const LossPotentialWidget = dynamic(() => import('@/components/widgets/LossPotentialWidget'), { ssr: false });

interface DiagnosisResult {
  score: number;
  loss_potential_usd: number; // 손실 예측 금액 (Anti-Loss Funnel의 핵심)
  risk_factors: string[]; // 진단된 위험 요인들
}

export default function DataIntegrityScorecard() {
  // 초기 상태 설정. 로딩 및 에러 처리를 위한 State 관리 필수.
  const [diagnosis, setDiagnosis] = useState<DiagnosisResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * 서버 액션 또는 클라이언트 측 API 호출을 시뮬레이션하는 함수.
   * 실제 환경에서는 이 로직이 서버 컴포넌트나 Server Action으로 분리되어야 안정적입니다.
   */
  const handleDiagnosis = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // 1. API 호출 및 데이터 수신 (핵심 로직)
      // fetchDiagnosisData는 서버 측에서 안전하게 실행되어야 합니다.
      const result: DiagnosisResult = await fetchDiagnosisData();
      setDiagnosis(result);
      console.log("✅ [Success] Data diagnosis completed:", result);

    } catch (e) {
      console.error("❌ [Error] API 호출 중 치명적 오류 발생:", e);
      setError("진단 서비스 연결에 실패했습니다. 잠시 후 다시 시도해주세요.");
      setDiagnosis(null);
    } finally {
      setIsLoading(false);
    }
  };

  // 컴포넌트 마운트 시 초기 진단 실행 (테스트를 위해 자동 호출)
  useEffect(() => {
    handleDiagnosis();
  }, []);


  return (
    <div className="p-8 max-w-7xl mx-auto bg-white shadow-lg rounded-xl">
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold tracking-tight mb-3" style={{ color: '#1D1D1F' }}>
          데이터 무결성 스코어카드 <span className="text-[#CC3333]">Diagnostic</span>
        </h1>
        <p className="text-lg text-gray-600">
          잠재적인 데이터 손실을 정량적으로 진단하고, 시스템 신뢰성을 측정하세요.
        </p>
      </header>

      {/* 1. API 호출 및 Funnel 시작 지점 */}
      <div className="mb-12 p-6 border border-dashed rounded-lg bg-gray-50">
          <h2 className="text-xl font-semibold mb-4">진단 스코어카드 실행</h2>
          {!diagnosis && (
            <button 
              onClick={handleDiagnosis} 
              disabled={isLoading}
              className={`px-12 py-3 text-lg rounded-full transition duration-300 ${isLoading ? 'bg-gray-400 cursor-not-allowed' : 'bg-[#CC3333] hover:bg-[#A82D2D]'} text-white shadow-md`}
            >
              {isLoading ? '진단 중... 데이터를 분석하는 중입니다 ⚙️...' : '데이터 무결성 진단 시작 (클릭)'}
            </button>
          )}
          <p className="mt-4 text-sm text-gray-500">
             * API 호출은 서버 측에서 실행되어야 데이터 유효성이 보장됩니다.
          </p>
      </div>

      {/* 2. 결과 및 Anti-Loss Funnel (진단 성공 시 표시) */}
      {diagnosis && !error && (
        <div className="space-y-16">
            
            {/* [Anti-Loss Visualization] - 가장 강력한 공포 자극 영역 */}
            <section className="mb-12 pt-8 border-t border-gray-200">
                <h2 className="text-3xl font-bold mb-4 flex items-center">
                    🚨 잠재적 손실 위험 시각화 
                    <span className="ml-3 text-[#CC3333] text-xl">(Loss Potential)</span>
                </h2>
                {/* AntiLossFunnelVisualization 컴포넌트가 데이터에 따라 애니메이션을 처리해야 합니다. */}
                <AntiLossFunnelVisualization lossAmount={diagnosis.loss_potential_usd} /> 
            </section>

            {/* [Widgets 통합] - 스코어 및 위험 요인 표시 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* ScoreGaugeWidget (진단 점수) */}
                <div className="lg:col-span-2">
                    <ScoreGaugeWidget score={diagnosis.score} /> 
                </div>

                {/* LossPotentialWidget (위험 요인 상세 분석) */}
                <div>
                    <LossPotentialWidget riskFactors={diagnosis.risk_factors} />
                </div>
            </div>
        </div>
      )}
      
      {/* 3. 에러 메시지 처리 */}
      {error && (
        <div className="p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          ⚠️ {error}
        </div>
      )}

    </div>
  );
}