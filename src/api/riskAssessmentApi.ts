// src/api/riskAssessmentApi.ts - Loss Scorecard Data Schema Definition
/**
 * @description Loss Scorecard 컴포넌트가 필요로 하는 모든 데이터 구조 정의
 */

export interface FinancialLossDetail {
    category: string; // 예: '데이터 무결성', '운영 중단', '인력 부족' 등
    estimatedCostUSD: number; // 손실액 (미화 통일)
    lossRatePerHour: number;  // 시간당 예상 손실률 ($/hour)
    durationDays: number;     // 영향을 받는 기간 (일)
}

export interface LossScorecardData {
    /** 🚨 핵심 플래그: 필수 데이터가 누락되었는지 여부 */
    dataIsMissing: boolean; 
    
    /** 📈 초기 분석된 손실액 및 리스크 점수 (1차 계산 결과) */
    baseRiskScore: number; // 0 ~ 100점 (정규화된 스코어)
    totalInitialLossUSD: number; // 기본 손실 총합 ($)

    /** 📉 데이터 결핍 시 패널티를 적용한 최종 리스크 점수 및 손실액 */
    finalRiskScore: number; // Penalty가 반영된 최종 스코어 (최대 5배 반영 가능)
    totalFinalLossUSD: number;  // Penalty가 반영된 최종 손실 총합 ($)

    /** 📊 Loss Breakdown에 사용될 상세 리스트. 시각화 데이터의 근거가 됩니다. */
    lossBreakdown: FinancialLossDetail[];
}


/**
 * @description API 엔드포인트 정의 및 fetch 함수 골격 (Mocking 포함)
 */
const API_ENDPOINT = "/api/v1/risk-assessment";

export async function fetchRiskAssessmentData(): Promise<LossScorecardData> {
    // 실제 환경에서는 axios 또는 fetch를 사용하여 비동기 호출을 수행합니다.
    console.log(`Fetching risk assessment data from ${API_ENDPOINT}...`);
    
    try {
        const response = await fetch(API_ENDPOINT, { method: 'GET' });
        if (!response.ok) {
            throw new Error('Failed to fetch risk assessment data.');
        }
        // 실제 응답 타입을 LossScorecardData로 가정하고 파싱합니다.
        return (await response.json()) as LossScorecardData; 

    } catch (error) {
        console.error("API Fetching Error:", error);
        // 에러 발생 시, 기본값으로 데이터를 반환하여 컴포넌트가 크래시되는 것을 방지합니다.
        return {
            dataIsMissing: true, // API 오류는 곧 '데이터 결핍' 상태로 간주함
            baseRiskScore: 0,
            totalInitialLossUSD: 0,
            finalRiskScore: 0,
            totalFinalLossUSD: 0,
            lossBreakdown: [],
        };
    }
}