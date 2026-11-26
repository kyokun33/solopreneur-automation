/**
 * @description Diagnosis Service: 데이터 무결성 진단 API 통신 담당 레이어 (Client Side).
 * @module diagnosisService
 */

import { apiClient } from './axiosInstance'; // 실제 axios 인스턴스는 나중에 설정합니다.

// Mockup V3.0에서 정의된 API 응답 스키마를 기반으로 정의합니다.
export interface DiagnosticResult {
  score: number;             // 최종 진단 점수 (0~100)
  lossTotalEstimate: number; // 총 예상 손실액 (Loss Potential)
  isCriticalFailure: boolean;// 심각한 오류 발생 여부
  breakdown: LossBreakdown[]; // 세부 손실 breakdown 배열
}

export interface LossBreakdown {
  category: string;         // 손실 원인 카테고리 (예: 데이터 누락, 비일관성)
  lossPercentage: number;  // 해당 오류가 차지하는 비율 (%)
  estimatedCost: number;    // 예상 비용 ($)
}

/**
 * @async
 * @description Mock API 호출 시뮬레이션 함수. 실제로는 FastAPI 백엔드와 통신합니다.
 * @param inputData 진단에 필요한 사용자/데이터 입력값 (예: 데이터셋 ID, 기간 등)
 * @returns Promise<DiagnosticResult> 진단 결과를 담은 Promise
 */
export const runDiagnosis = async (inputData: Record<string, any>): Promise<DiagnosticResult> => {
  console.log("🚀 Running Data Integrity Diagnostic...");

  // [TODO]: 실제 환경에서는 apiClient.post('/api/v1/diagnose', inputData)를 호출해야 합니다.
  // 현재는 Mockup 스펙을 반영한 테스트 데이터로 대체합니다.
  await new Promise(resolve => setTimeout(resolve, 1500)); // 로딩 지연 시뮬레이션

  const mockResult: DiagnosticResult = {
    score: Math.floor(Math.random() * (80 - 40 + 1)) + 40, // 40~80점 사이의 점수 생성
    lossTotalEstimate: Math.round((Math.random() * 5000) + 1000), // $1000 ~ $6000 예상 손실액
    isCriticalFailure: Math.random() > 0.3, // 70% 확률로 Critical Failure가 발생하도록 설정 (위기감 조성)
    breakdown: [
      { category: "데이터 누락 (Data Gap)", lossPercentage: 45, estimatedCost: Math.round(Math.random() * 2000 + 500) },
      { category: "일관성 오류 (Inconsistency)", lossPercentage: 30, estimatedCost: Math.round(Math.random() * 1500 + 800) },
      { category: "접근성 취약점 (Vulnerability)", lossPercentage: 25, estimatedCost: Math.round(Math.random() * 1000 + 300) },
    ]
  };

  return mockResult;
};

export type DiagnosisInput = Record<string, any>;