import { PaymentGatewayMock } from '../utils/PaymentGatewayMock';
// 가상의 API 서비스 레이어입니다. 실제 프로젝트 구조에 맞게 수정 필요합니다.
const mockApiService = {
    /**
     * @description 결제 성공 후, 보고서 생성 및 리스크 점수를 계산하는 핵심 로직을 시뮬레이션합니다.
     * @param transactionId - 결제 게이트웨이가 반환한 트랜잭션 ID
     * @returns Promise<{ reportUrl: string; finalScore: number }>
     */
    async generateReport(transactionId: string): Promise<{ reportUrl: string; finalScore: number }> {
        console.log(`[API Service] Report generation initiated for ${transactionId}.`);
        // 실제로는 여기서 DB 저장, PDF 생성 워크플로우가 트리거 됩니다.
        await new Promise(resolve => setTimeout(resolve, 100)); // 보고서 생성 지연 시뮬레이션
        return {
            reportUrl: `/download/report/${transactionId}.pdf`,
            finalScore: Math.floor(Math.random() * 100) + 50 // 임의 점수 부여
        };
    }
};

describe('E2E Payment Funnel Test Suite (Loss Scorecard CTA)', () => {
    let paymentGateway: PaymentGatewayMock;
    const MOCK_REPORTING_COST = 97.00; // $97 Tier 기준
    
    beforeEach(() => {
        // 각 테스트 시작 전 Mock 객체 초기화
        paymentGateway = new PaymentGatewayMock();
    });

    /**
     * @description 성공적인 결제 및 보고서 수신까지의 전체 파이프라인을 검증합니다. (Happy Path)
     */
    it('✅ Should successfully process payment and retrieve the diagnostic report.', async () => {
        const mockToken = "mock-success-token";

        // 1. Payment Gateway 호출 시뮬레이션
        let transactionResult;
        try {
            transactionResult = await paymentGateway.processPayment(MOCK_REPORTING_COST, mockToken);
        } catch (error) {
            throw new Error("Payment API call failed unexpectedly.");
        }

        // 2. 성공 여부 검증 및 다음 로직 분기
        expect(transactionResult.success).toBe(true);
        expect(transactionResult.message).toContain("Report generation started");
        const transactionId = transactionResult.transactionId!;

        let reportDetails;
        try {
            // 3. API 서비스 호출 (보고서 생성)
            reportDetails = await mockApiService.generateReport(transactionId);
        } catch (error) {
             throw new Error("Report generation failed after successful payment.");
        }

        // 4. 최종 검증: 성공적으로 보고서 URL과 점수를 받았는지 확인
        expect(reportDetails.reportUrl).toMatch(/\/download\/report\/.+\.pdf/);
        expect(typeof reportDetails.finalScore).toBe('number');
    });


    /**
     * @description 자금 부족(Insufficient Funds) 시나리오를 검증합니다. (Failure Path A)
     */
    it('❌ Should handle Insufficient Funds error gracefully and prevent resource leakage.', async () => {
        const mockToken = "mock-insufficient-funds";

        // 1. Payment Gateway 호출
        let transactionResult;
        transactionResult = await paymentGateway.processPayment(MOCK_REPORTING_COST, mockToken);

        // 2. 실패 여부 검증 및 오류 메시지 확인
        expect(transactionResult.success).toBe(false);
        expect(transactionResult.message).toContain("Insufficient funds");

        // *핵심 검증*: 결제 실패 시 보고서 생성 API가 호출되지 않았는지 (Mocking Context) 확인해야 합니다. 
        // 실제 테스트에서는 mockApiService의 호출 카운터를 이용해 이 부분을 확정합니다.
    });


    /**
     * @description 유효하지 않은 토큰(Invalid Token)으로 인한 게이트웨이 오류를 검증합니다. (Failure Path B)
     */
    it('❌ Should handle Gateway Error due to invalid credentials.', async () => {
        const mockToken = "mock-invalid-token";

        // 1. Payment Gateway 호출
        let transactionResult;
        transactionResult = await paymentGateway.processPayment(MOCK_REPORTING_COST, mockToken);

        // 2. 실패 여부 검증 및 오류 메시지 확인
        expect(transactionResult.success).toBe(false);
        expect(transactionResult.message).toContain("Invalid token");
    });
});