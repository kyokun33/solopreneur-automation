/**
 * LossScorecard Component Types (TypeScript)
 * @description 백엔드에서 전달받을 손실 점수 계산 결과 및 상세 Breakdown에 대한 데이터 계약 정의
 */

// --------------------------------------------------
// 1. Input Schema: 사용자가 입력할 리스크 요인 정보
// --------------------------------------------------
export interface RiskFactor {
    id: string; // 예: 'AI_BIAS', 'DATA_INTEGRITY'
    description: string; // 위험 요소 설명
    severityScore: number; // (0~10) 심각도 점수
    potentialCost: number; // 이 요인으로 인한 잠재적 금전적 손실 예상액
}

// --------------------------------------------------
// 2. Output Schema: 계산 결과 전체 구조
// --------------------------------------------------
export interface LossScorecardResult {
    totalLossEstimate: number; // 최종 추정 손실 비용 (가장 중요)
    calculationBreakdown: BreakdownDetail[]; // 상세 계산 과정 리스트
    summaryReportText: string; // 보고서 요약 텍스트 (CTA용)
}

// --------------------------------------------------
// 3. Detailed Breakdown Schema: 개별 분석 항목의 상세 정보
// --------------------------------------------------
export interface BreakdownDetail {
    riskFactorId: string; // 어느 위험 요소에서 발생했는지
    factorDescription: string; // 요인 설명 (예: "데이터 무결성 문제")
    contributionPercentage: number; // 전체 손실 대비 기여율 (%)
    estimatedLossAmount: number; // 이 요인이 기여하는 예상 손실액 ($)
    severityLevel: 'LOW' | 'MEDIUM' | 'HIGH'; // 경고 레벨
}

// --------------------------------------------------
// 4. State Management Type (Optional but good practice)
// --------------------------------------------------
export type ScorecardStatus = 'IDLE' | 'LOADING' | 'CALCULATING' | 'SUCCESS' | 'ERROR';