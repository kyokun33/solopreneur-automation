import { RiskFactor, LossScorecardResult, BreakdownDetail } from '../types/scorecard';

/**
 * @class CalculationEngine
 * @description 핵심 비즈니스 로직을 전담합니다. UI/UX와 분리되어야 하며, 오직 계산과 데이터 구조화만 담당합니다.
 */
export class CalculationEngine {

    /**
     * 리스크 요인 배열을 받아 최종 손실 점수 및 상세 Breakdown 데이터를 계산하여 반환합니다.
     * @param factors - 분석할 리스크 요소들의 배열
     * @returns LossScorecardResult 객체
     */
    public static async calculate(factors: RiskFactor[]): Promise<LossScorecardResult> {
        // 시뮬레이션 지연 (API 호출을 가정)
        await new Promise(resolve => setTimeout(resolve, 500));

        let totalLoss = 0;
        const breakdownDetails: BreakdownDetail[] = [];
        
        // 가중치 적용 로직 예시: Severity Score가 높고 Potential Cost도 높은 것에 가중치를 줌.
        factors.forEach((factor, index) => {
            // 손실 기여도는 (Severity * WeightFactor + PotentialCost / Index)로 복잡하게 계산한다고 가정
            const calculatedLoss = factor.potentialCost * (1 + factor.severityScore / 10);
            totalLoss += calculatedLoss;

            breakdownDetails.push({
                riskFactorId: factor.id,
                factorDescription: `[${factor.id}] ${factor.description}`,
                contributionPercentage: Math.min(100, (calculatedLoss / totalLoss) * 100), // 비율 계산
                estimatedLossAmount: calculatedLoss,
                severityLevel: factor.severityScore >= 8 ? 'HIGH' : factor.severityScore >= 5 ? 'MEDIUM' : 'LOW',
            });
        });

        // 최종 보고서 문구 생성 (Funnel 구조 반영)
        const summaryText = `분석 결과, 귀사는 현재 ${totalLoss.toLocaleString()}에 달하는 예상 손실 위험을 안고 있습니다. 이 수치는 단순한 추정이 아니며, 데이터 무결성 및 AI 법규 리스크를 정량화한 점수입니다.`;

        return {
            totalLossEstimate: Math.round(totalLoss), // 최종 금액 반환 (정수형)
            calculationBreakdown: breakdownDetails,
            summaryReportText: summaryText,
        };
    }
}