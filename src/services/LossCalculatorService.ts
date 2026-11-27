/**
 * @fileoverview Loss Scorecard의 핵심 비즈니스 로직을 담당하는 순수 서비스 클래스.
 * 모든 외부 의존성(DB, HTTP 요청 등)으로부터 완전히 분리되어 단위 테스트가 가능해야 함.
 * [근거: 2026-11-27T05:57] - 핵심 비즈니스 로직은 API 프레임워크와 분리된 순수 서비스 클래스로 구현한다.
 */

import {
    RawUserInputData,
    LossScoreResult,
    ReportRequestPayload,
    ReportResponse
} from '../types/LossScorecardTypes';
import { PaymentGatewayMock } from '../utils/PaymentGatewayMock'; // Mockup 사용 가정

/**
 * 손실 점수 계산의 핵심 로직을 담당하는 서비스 클래스.
 * 이 클래스는 외부 환경(API 호출, DB 접근)에 의존하지 않고 순수한 수학적 로직만 수행해야 한다.
 */
export class LossCalculatorService {
    constructor() {} // Stateless Service

    /**
     * 1. 핵심 비즈니스 로직: 손실 점수를 산출하고 상세 Breakdown을 반환한다. (Pure Logic)
     * @param rawData - 사용자로부터 수집된 RawUserInputData.
     * @returns {LossScoreResult} 계산된 LossScore 결과 객체.
     */
    public calculateLossScore(rawData: RawUserInputData): LossScoreResult {
        // [로직 구현 가이드]: 실제 복잡한 가중치 기반의 로직이 들어갈 자리.
        // 예시를 위해 임의의 점수 산출 공식 적용.
        const dataIntegrityWeight = 0.4; // 데이터 무결성이 가장 중요하다고 가정
        const complianceWeight = 0.3;

        const score1 = rawData.dataIntegrityRiskScore * dataIntegrityWeight / 100;
        const score2 = (rawData.complianceViolationCount * 10) * complianceWeight / 10; // Violation당 가중치 부여

        // 총점 계산 및 누적 오차 처리 로직이 여기에 들어간다.
        const totalLossScore = Math.min(100, parseFloat((score1 + score2).toFixed(2)));

        /** @type {Array<{metricName: string, scoreValue: number, explanation: string}>} */
        const breakdown: any[] = [
            { 
                metricName: "Data Integrity Risk", 
                scoreValue: parseFloat(score1.toFixed(2)), 
                explanation: `데이터 무결성 점수 (${rawData.dataIntegrityRiskScore})가 높게 측정되어, 핵심 데이터 유실 리스크를 나타냅니다.` 
            },
            { 
                metricName: "Compliance Violation", 
                scoreValue: parseFloat(score2.toFixed(2)), 
                explanation: `규정 위반 횟수 (${rawData.complianceViolationCount}회)는 운영 안정성 측면에서 경고가 필요합니다.` 
            }
        ];

        return {
            totalLossScore: totalLossScore,
            lossDescription: this.determineLossDescription(totalLossScore),
            breakdown: breakdown,
            calculatedOnTimestamp: Date.now()
        };
    }


    /**
     * 2. 결제 연동 로직: 진단 보고서 요청에 대한 처리 과정 (Service Layer).
     * @param payload - ReportRequestPayload (사용자 ID 및 보고서 타입).
     * @returns {Promise<ReportResponse>} 결제 결과가 담긴 응답 객체.
     */
    public async requestDiagnosisReport(payload: ReportRequestPayload): Promise<ReportResponse> {
        console.log(`[Service] ${payload.userIdentifier} 님의 '${payload.reportType}' 보고서 요청을 처리합니다.`);

        // [핵심]: 결제 게이트웨이 서비스 호출 (Mockup 사용)
        try {
            const paymentSuccess = await PaymentGatewayMock.processPayment(payload.userIdentifier, payload.reportType);

            if (!paymentSuccess) {
                return {
                    paymentSuccess: false,
                    reportId: null,
                    message: "결제 실패: 유효한 결제 수단 또는 권한을 확인해 주세요."
                };
            }

            // 결제 성공 시, 실제 보고서 생성 및 저장 로직 호출 (여기서는 Mocking)
            const reportId = `REPORT-${payload.userIdentifier}-${Date.now()}`;

            console.log(`[Service] ✅ ${reportId}가 성공적으로 발행되었습니다.`);
            return {
                paymentSuccess: true,
                reportId: reportId,
                message: "진단 보고서 발급이 완료되었습니다. 상세 내용은 시스템에서 확인 가능합니다."
            };

        } catch (error) {
            console.error("보고서 요청 처리 중 치명적인 오류 발생:", error);
            return {
                paymentSuccess: false,
                reportId: null,
                message: "시스템 오류로 보고서를 발급할 수 없습니다. 잠시 후 다시 시도해 주세요."
            };
        }
    }

    /**
     * 내부 도우미 함수: 점수에 따른 텍스트 설명 생성 (가독성 확보)
     * @param score - 계산된 손실 점수.
     * @returns {string} 적절한 경고 메시지.
     */
    private determineLossDescription(score: number): string {
        if (score > 85) return "🚨 **극심한 리스크**: 즉각적인 법적/운영 개입이 필수입니다.";
        if (score >= 60) return "⚠️ **높은 경고 수준**: 시스템의 중요한 부분에서 개선이 필요합니다.";
        return "✅ **관리 가능 수준**: 현재로서는 큰 문제가 발견되지 않았습니다. 하지만 지속적인 모니터링을 권장합니다.";
    }
}