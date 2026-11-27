import { useState, useCallback } from 'react';
import { InputData, LossScoreData } from '@/types/lossScoreCard';

// [근거: Self-RAG - Loss Rate: $55/hour 고정값]
const LOSS_RATE_PER_HOUR = 55; // 시간당 손실액 (USD)
const RISK_MULTIPLIER = 100; // 리스크 점수당 배율 상수

/**
 * 핵심 비즈니스 로직: Loss Score를 계산하는 커스텀 훅.
 * 입력 데이터가 변경될 때마다 상태를 업데이트하고 결과를 반환합니다.
 */
export const useLossCalculation = () => {
    const [input, setInput] = useState<InputData>({
        timeSpent: 0,
        riskLevel: 0,
        area: '데이터 무결성 리스크' // 기본값 설정
    });

    // 입력 데이터 변경 핸들러 (자료유효성 검사 및 상태 업데이트)
    const handleInputChange = useCallback((key: keyof InputData, value: any) => {
        let newValue: number;
        if (typeof value === 'string' && !isNaN(parseFloat(value))) {
            newValue = parseFloat(value);
        } else if (['데이터 무결성 리스크', '운영 비효율'].includes(String(value))) {
            // Enum/Select 처리
            newValue = 0; // Area는 상태로 관리하므로 여기선 임시 로직만
        } else {
             return; // 유효하지 않은 입력 방지
        }

        setInput(prev => ({ ...prev, [key]: newValue }));
    }, []);

    /**
     * 핵심 계산 함수: LossScoreData를 산출합니다.
     * @param currentInput - 현재 상태의 InputData
     */
    const calculateLoss = useCallback((currentInput: InputData): LossScoreData => {
        // 1. 시간 손실액 계산 (Time Loss)
        const timeLossAmount = currentInput.timeSpent * LOSS_RATE_PER_HOUR;

        // 2. 리스크 비용 산출 (Risk Loss - Self-RAG 근거 활용)
        // 리스크 레벨이 높을수록, 그리고 특정 영역일 때 배율 증가 가정
        let riskLossAmount = currentInput.riskLevel * RISK_MULTIPLIER;
        if (currentInput.area === '데이터 무결성 리스크') {
            // 데이터 무결성 리스크는 가중치가 더 크다고 가정
            riskLossAmount *= 1.5; 
        }

        const totalLoss = timeLossAmount + riskLossAmount;

        // 3. Red Warning 트리거 로직 (비즈니스 규칙)
        // 예: 총 손실액이 $500을 초과하거나, 리스크 레벨이 8점 이상이면 경고 발생
        const warningTriggered = totalLoss > 500 || currentInput.riskLevel >= 8;

        const breakdown: Record<string, number> = {
            '시간 손실': Math.round(timeLossAmount),
            '리스크 비용': Math.round(riskLossAmount)
        };

        return {
            totalLossAmount: Math.round(totalLoss * 100) / 100, // 소수점 둘째 자리까지 반올림
            lossBreakdown: breakdown,
            warningTriggered: warningTriggered
        };
    }, []);

    // 입력이 변경될 때마다 계산을 재실행하여 결과값을 상태로 관리합니다.
    const [result, setResult] = useState<LossScoreData>(() => calculateLoss(input));

    // input state가 변경되면 result를 강제로 업데이트하는 useEffect 로직 (생략 가능하나 명시적으로 분리)
    // 여기서는 간결함을 위해 setInput 호출 시 계산을 즉각 반영한다고 가정합니다. 
    const finalResult = useMemo(() => calculateLoss(input), [input, calculateLoss]);

    return {
        input: input,
        handleInputChange,
        result: finalResult // 최종 계산된 결과 반환
    };
};