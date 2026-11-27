/**
 * @module mockLossCalculation
 * @description Designer가 정의한 Loss Scorecard의 핵심 비즈니스 로직을 모킹합니다.
 * 실제 API 호출 대신, 상태 변화와 손실 점수 계산 시퀀스를 강제합니다.
 */

import { useState } from 'react';

// --- 타입 정의 (API Contract 기반) ---
export interface CalculationInput {
  hoursOfVulnerability: number; // 노출 시간 (시간 단위)
  dataIntegrityRiskLevel: 'low' | 'medium' | 'high'; // 데이터 무결성 리스크 레벨
}

export interface LossReport {
  totalLossScore: number; // 총 손실 점수 ($)
  breakdown: {
    timeLoss: number; // 시간 기반 손실액
    riskLoss: number; // 리스크 기반 손실액
    details: Record<string, number>; // 세부 항목별 분배 (예: 법적 책임, 기회비용)
  };
}

/**
 * 시뮬레이션된 핵심 로직: 입력 값을 받아 Loss Report를 계산합니다.
 * @param input - 사용자로부터 받은 취약 시간 및 리스크 레벨.
 * @returns Promise<LossReport> - 비동기 처리를 가정하여 보고서를 반환합니다.
 */
export const calculateMockLossScore = async (input: CalculationInput): Promise<LossReport> => {
  // 1. Simulate Network Latency (API Call delay)
  await new Promise(resolve => setTimeout(resolve, 800));

  console.log(`[Mock API] Starting calculation for ${input.hoursOfVulnerability} hours and ${input.dataIntegrityRiskLevel} risk.`);

  // --- Loss Calculation Logic Simulation ---
  let baseLoss = input.hoursOfVulnerability * 55; // $55/hour (Self-RAG Source)

  let riskMultiplier: number;
  switch (input.dataIntegrityRiskLevel) {
    case 'low':
      riskMultiplier = 1.0;
      break;
    case 'medium':
      riskMultiplier = 2.5; // 중간 리스크는 2배 이상으로 가정
      break;
    case 'high':
      riskMultiplier = 4.0; // 높은 리스크는 최소 3~4배의 충격 반영
      break;
  }

  const calculatedRiskLoss = Math.round(baseLoss * riskMultiplier * 1.2); // 추가적인 법적 책임을 곱함
  const totalLossScore = Math.round(baseLoss + calculatedRiskLoss);

  // Loss Breakdown (Designer Spec 기반)
  const breakdown: { [key: string]: number } = {
    timeLoss: Math.round(baseLoss),
    riskLoss: Math.round(calculatedRiskLoss),
    'legal_responsibility': totalLossScore * 0.3, // 예시 세부 항목
    'lost_opportunity': totalLossScore * 0.7,
  };

  const report: LossReport = {
    totalLossScore: totalLossScore,
    breakdown: {
      timeLoss: Math.round(baseLoss),
      riskLoss: Math.round(calculatedRiskLoss),
      details: breakdown,
    },
  };

  return report;
};


/**
 * [Mock Utility] 전역 상태 변화 시뮬레이션 함수 (Glitch/Red Warning Trigger)
 * @param currentScore - 이전 스코어
 * @param newScore - 계산된 새 스코어
 */
export const simulateStateTransition = (currentScore: number, newScore: number): { trigger: string; intensity: number } => {
    const diff = Math.abs(newScore - currentScore);
    let triggerType = 'stable';

    if (diff > 100) {
        triggerType = 'major_spike'; // 큰 변화는 Glitch 유발
    } else if (newScore > currentScore * 1.5) {
        triggerType = 'warning_increase'; // 급격한 증가 시 경고 필터 강화
    }

    return { trigger: triggerType, intensity: Math.min(1, diff / 200) };
};

export default {
  calculateMockLossScore,
  simulateStateTransition,
};