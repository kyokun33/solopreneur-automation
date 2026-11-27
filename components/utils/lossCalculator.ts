/**
 * @fileoverview Anti-Loss Funnel의 핵심 로직: 사용자의 입력값을 받아 다음 단계(Next Step)를 결정합니다.
 * [근거: 🎨 Designer Mockup Specification, CEO 지시]
 */

// 상수 정의 (Configurable Values)
export const CRITICAL_LOSS_THRESHOLD = 50000; // 임계값: 이 금액 이상이면 '보고서' 필요
export const WARNING_LOSS_THRESHOLD = 10000;  // 경고 임계값: 최소한의 진단이 필요한 수준

/**
 * 손실액을 기반으로 사용자의 현재 상태와 다음 액션(Next Step)을 진단합니다.
 * @param currentLossAmount - 사용자가 입력하거나 계산된 총 손실 금액 (원화).
 * @returns {object} 진단 결과 객체: 메시지, CTA 타입, 가이드 텍스트 등을 포함.
 */
export const diagnoseAntiLossStatus = (currentLossAmount: number): {
    status: 'SAFE' | 'WARNING' | 'CRITICAL';
    message: string;
    ctaText: string;
    details: React.ReactNode; // 실제 렌더링될 내용 (JSX)
} => {
    if (isNaN(currentLossAmount) || currentLossAmount < 0) {
        return {
            status: 'SAFE',
            message: "손실액을 입력하여 당신의 잠재적 위험을 진단해 보세요.",
            ctaText: "",
            details: null,
        };
    }

    const loss = Math.floor(currentLossAmount); // 정수화

    if (loss >= CRITICAL_LOSS_THRESHOLD) {
        // 🚨 Critical Loss Zone: 전문가의 도움이 절대적으로 필요함.
        return {
            status: 'CRITICAL',
            message: `경고! ${Math.round(loss / 1000)}만 원 이상의 손실은 단순한 우발적 사건이 아닙니다. 이는 시스템 구조적 취약성 때문입니다.`,
            ctaText: "✅ 맞춤형 진단 보고서 받기 (1:1 미팅 예약)",
            details: <p className="text-red-600 font-bold">👉 당신은 근본적인 원인 파악이 필수적입니다.</p>
        };
    } else if (loss >= WARNING_LOSS_THRESHOLD) {
        // ⚠️ Warning Loss Zone: 스스로 해결할 수 있는 범위지만, 전문가의 검토가 필요함.
        return {
            status: 'WARNING',
            message: `주의! ${Math.round(loss / 1000)}만 원 규모의 손실은 경고 신호입니다. 지금 바로 취약점을 점검해야 합니다.`,
            ctaText: "📈 무료 자가 진단 리포트 다운로드",
            details: <p className="text-yellow-600">💡 간단한 폼을 통해 잠재적 위험 요소를 먼저 파악할 수 있습니다.</p>
        };
    } else {
        // ✅ Safe Zone: 아직 임계치에 도달하지 않음. 교육/인식 확산 단계.
        return {
            status: 'SAFE',
            message: "현재까지의 손실은 관리 가능한 수준입니다. 하지만 방심할 수 없습니다.",
            ctaText: "📘 핵심 리스크 지표 학습하기",
            details: <p className="text-green-600">📚 가장 위험한 3가지 시나리오를 먼저 확인해 보세요.</p>
        };
    }
};

/**
 * 가상의 손실 계산 로직 (시간, 데이터 무결성 리스크 등을 통합)
 * 실제 구현 시에는 사용자 입력(Time Spent, Data Volume 등)을 받아 복잡한 가중치를 적용해야 합니다.
 * @param timeSpentHours - 시간당 노출 또는 작업 시간 (h).
 * @returns {number} 추정 손실 금액 (원).
 */
export const calculateEstimatedLoss = (timeSpentHours: number): number => {
    // [근거: 지난 의사결정 로그 - Loss Rate $55/hour]
    const lossRatePerHour = 55; // 시간당 예상 비용 (가장 중요한 변수)
    let estimatedLoss = timeSpentHours * lossRatePerHour;

    // 추가 리스크 계수 적용 예시: 데이터 무결성 문제 발생 시 손실 증가 (1.2배)
    if (timeSpentHours > 5) { // 작업 시간이 길수록 구조적 문제가 심각하다고 가정
        estimatedLoss *= 1.2;
    }

    return Math.round(estimatedLoss);
};