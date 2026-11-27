/**
 * @module PaymentGatewayMock
 * @description 실제 결제 API와 통신하는 대신, 비즈니스 로직 테스트를 위한 가상 게이트웨이 모킹 클래스입니다.
 * 이 Mock은 성공/실패 시나리오별로 일관된 페이로드를 반환합니다.
 */

type TransactionResult = {
    success: boolean;
    transactionId?: string;
    message: string;
};

/**
 * @class PaymentGatewayMock
 * 가짜 결제 트랜잭션을 시뮬레이션하는 클래스.
 * 실제 환경에서는 여기에 Stripe, PayPal SDK 호출이 들어갈 것입니다.
 */
export class PaymentGatewayMock {
    private readonly API_KEY = process.env.PAYMENT_MOCK_API_KEY || "mock-key";

    /**
     * 가상 결제를 시도합니다. 테스트 목적으로 사용됩니다.
     * @param amount - 요청 금액 (Loss Scorecard 기반 계산된 최종 비용)
     * @param token - 클라이언트가 전송한 가상 토큰
     * @returns Promise<TransactionResult>
     */
    public async processPayment(amount: number, token: string): Promise<TransactionResult> {
        console.log(`[Mock Payment] Processing ${amount} with token: ${token}`);

        // 1. 성공 시나리오 (Happy Path)
        if (token === "mock-success-token" && amount > 0) {
            await new Promise(resolve => setTimeout(resolve, 50)); // 네트워크 지연 시뮬레이션
            return {
                success: true,
                transactionId: `txn_${Date.now()}_SUCCESS`,
                message: "Payment successful. Report generation started.",
            };
        }

        // 2. 실패 시나리오 A: 자금 부족 (Insufficient Funds)
        if (token === "mock-insufficient-funds") {
             await new Promise(resolve => setTimeout(resolve, 50));
            return {
                success: false,
                message: "Transaction failed: Insufficient funds. Please check your payment method.",
            };
        }

        // 3. 실패 시나리오 B: 유효성 검사 실패 (Invalid Token/Gateway Error)
        if (token === "mock-invalid-token") {
             await new Promise(resolve => setTimeout(resolve, 50));
            return {
                success: false,
                message: "Payment gateway error: Invalid token or credentials provided.",
            };
        }

        // 기본 실패 케이스
        await new Promise(resolve => setTimeout(resolve, 50));
        return {
            success: false,
            message: "An unknown payment processing error occurred.",
        };
    }
}