/**
 * Loss Scorecard Component Types & Enums
 */

// 1. 리스크 상태 정의 (State Machine)
export type RiskLevel = 'initial' | 'warning' | 'critical';

// 2. 컴포넌트 Props 정의
export interface LossScorecardProps {
  /** 현재 사용자의 데이터 세트를 기반으로 손실 점수를 계산합니다. */
  inputData: Record<string, number>;
}

// 3. 상태 전이 결과 타입
export interface ScorecardState {
  score: number; // 최종 산출된 점수 (예: 달러 단위)
  level: RiskLevel; // 현재 리스크 레벨
  message: string; // 사용자에게 보여줄 경고 메시지
}

// 4. 시뮬레이션 API 응답 구조 (만약 백엔드에서 데이터를 받는다면 사용될 스키마)
export interface LossSimulationApiResponse {
    initialScore: number;
    finalScore: number;
    riskLevel: RiskLevel;
    breakdown: Record<string, number>; // 손실 요인별 금액
}