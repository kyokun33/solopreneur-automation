/**
 * Loss Scorecard State Machine API 명세서 (TypeScript Interface)
 * @description 핵심 상태 전이 및 데이터 구조를 강제하여 타입 안정성을 확보합니다.
 */

// 1. 핵심 상태 정의
export type ScorecardState = 'Apathy' | 'Warning' | 'Critical';

/**
 * LossScorecardInputData: 사용자의 행동이나 환경 변화로 인해 점수 산출에 필요한 원시 데이터입니다.
 * @param {number} timeElapsedHours - 서비스 이용 시간 (시간 단위).
 * @param {number} dataIntegrityRiskPoints - 사용자 데이터 무결성 위험 포인트.
 * @param {boolean} legalComplianceIssueDetected - 법적 리스크 이슈 감지 여부 (Boolean).
 */
export interface LossScorecardInputData {
    timeElapsedHours: number;
    dataIntegrityRiskPoints: number;
    legalComplianceIssueDetected: boolean;
}

/**
 * LossScorecardResult: 스코어링 API 호출 후 반환되는 최종 결과 데이터 구조입니다.
 */
export interface LossScorecardResult {
    currentLossState: ScorecardState; // 현재 상태 (Apathy, Warning, Critical 중 하나)
    totalEstimatedLossUSD: number;  // 총 예상 손실 금액 ($ 단위)
    riskBreakdown: {
        timeImpact: number;          // 시간적 영향 손실 금액
        dataRiskImpact: number;      // 데이터 무결성 위험 손실 금액
        legalImpact: number;         // 법적 책임 리스크 손실 금액
    };
    explanationMessage: string;   // 현재 상태에 대한 경고 메시지 (예: "경각심이 필요합니다.")
}

/**
 * ScorecardTransitionHistory: 사용자에게 보여줄 전환 이력 데이터입니다.
 */
export interface ScorecardTransitionHistory {
    timestamp: Date;
    prevState: ScorecardState;
    currentState: ScorecardState;
    triggerEvent: string; // 상태 변화를 유발한 이벤트 (예: 'Data Upload Failure', 'Long Time Gap')
}

// 2. API 명세서 타입 정의 (Mocking the backend API call)
export interface IScorecardService {
    /**
     * @description 입력 데이터를 기반으로 Loss Scorecard의 상태와 금액을 계산합니다.
     * @param data - LossScorecardInputData 객체.
     * @returns Promise<LossScorecardResult> - 비동기적으로 결과를 반환합니다.
     */
    calculate(data: LossScorecardInputData): Promise<LossScorecardResult>;

    /**
     * @description 시간 경과에 따른 누적 손실액을 업데이트하고 상태 변화를 추적합니다.
     * @param previousState - 이전 스코어카드 상태.
     * @param newTimeElapsedHours - 새로운 이용 시간.
     * @returns Promise<{result: LossScorecardResult, history: ScorecardTransitionHistory}>
     */
    trackProgress(previousState: ScorecardState, newTimeElapsedHours: number): Promise<{ result: LossScorecardResult; history: ScorecardTransitionHistory }>;
}