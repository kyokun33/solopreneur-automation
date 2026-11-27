/**
 * @description Loss Scorecard의 상태 전이 및 계산 로직을 담당하는 커스텀 훅입니다.
 * 핵심 비즈니스 로직을 UI에서 분리하여 테스트 용이성을 극대화합니다.
 */

import { useState, useEffect, useCallback } from 'react';
import { IScorecardService, LossScorecardInputData, ScorecardState, LossScorecardResult, ScorecardTransitionHistory } from '../types/LossScorecardTypes';

// Mock Service 구현 (실제 백엔드 API 호출을 대체)
// 실제 환경에서는 fetch('/api/scorecard/calculate') 등을 사용해야 합니다.
const mockScorecardService: IScorecardService = {
    async calculate(data: LossScorecardInputData): Promise<LossScorecardResult> {
        console.log("[Mock API] Calculating score with:", data);
        // 복잡한 로직을 시뮬레이션하여 임의의 결과 반환 (실제로는 백엔드에서 계산)
        let loss = 0;
        if (data.timeElapsedHours > 10) {
            loss += 500 * data.timeElapsedHours / 10; // 시간당 손실 증가
        }
        if (data.legalComplianceIssueDetected) {
            loss += 3000; // 법적 리스크 발생 시 큰 폭의 점수 상승
        }

        let state: ScorecardState = 'Apathy';
        let message = "현재 데이터 상태는 양호합니다. 하지만 방심은 위험합니다.";

        if (loss >= 2500) {
            state = 'Critical';
            message = "🚨 CRITICAL ALERT! 법적 책임 증명(Accountability Proof)에 심각한 손실 리스크가 감지되었습니다!";
        } else if (loss >= 1000) {
            state = 'Warning';
            message = "⚠️ WARNING. 데이터 무결성 및 시간 누적 위험이 증가하고 있습니다. 즉시 점검이 필요합니다.";
        }

        return {
            currentLossState: state,
            totalEstimatedLossUSD: parseFloat(Math.min(loss, 8000).toFixed(2)), // 최대 $8000 제한
            riskBreakdown: {
                timeImpact: Math.round(loss * 0.4),
                dataRiskImpact: Math.round(loss * 0.3),
                legalImpact: Math.round(loss * 0.3),
            },
            explanationMessage: message,
        };
    },

    async trackProgress(previousState: ScorecardState, newTimeElapsedHours: number): Promise<{ result: LossScorecardResult; history: ScorecardTransitionHistory }> {
        // 실제 트래킹 로직 구현 (여기서는 Mock API 호출로 대체)
        const mockData: LossScorecardInputData = {
            timeElapsedHours: newTimeElapsedHours,
            dataIntegrityRiskPoints: 10 + Math.random() * 50,
            legalComplianceIssueDetected: newTimeElapsedHours > 8 && Math.random() > 0.7 // 특정 조건에서 임의로 True
        };

        const result = await this.calculate(mockData);

        const history: ScorecardTransitionHistory = {
            timestamp: new Date(),
            prevState: previousState,
            currentState: result.currentLossState,
            triggerEvent: `Time progression to ${newTimeElapsedHours} hours`,
        };

        return { result, history };
    }
};


/**
 * @description Loss Scorecard 상태 추적 로직을 관리하는 커스텀 훅.
 * @param initialData - 컴포넌트가 초기화될 때의 기본 데이터.
 */
export const useLossScorecard = (initialData: Partial<LossScorecardInputData>) => {
    // State management for the core score card data
    const [currentState, setCurrentState] = useState<LossScorecardResult | null>(null);
    const [history, setHistory] = useState<ScorecardTransitionHistory[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    /**
     * @description 스코어카드 상태를 업데이트하고 전이를 추적하는 메인 함수.
     * 이 함수가 비즈니스 로직의 단일 진입점입니다.
     * @param inputData - 최신 입력 데이터 (시간, 리스크 포인트 등).
     */
    const updateScorecard = useCallback(async (inputData: LossScorecardInputData) => {
        setIsLoading(true);
        try {
            // 1. 현재 상태를 기반으로 다음 스코어카드 결과를 추적합니다.
            let previousState: ScorecardState = currentState?.currentLossState || 'Apathy';

            const { result, history: newHistory } = await mockScorecardService.trackProgress(previousState, inputData.timeElapsedHours);

            // 2. 상태 및 히스토리 업데이트
            setCurrentState(result);
            setHistory(prev => [...prev, newHistory]);

        } catch (error) {
            console.error("Error updating scorecard state:", error);
            // 에러 발생 시 사용자에게 경고 메시지 표시 로직 추가 가능
        } finally {
            setIsLoading(false);
        }
    }, [currentState]);


    useEffect(() => {
        // 초기 로드 시점의 계산을 수행합니다.
        if (!isLoading) {
             updateScorecard({
                timeElapsedHours: initialData?.timeElapsedHours || 0,
                dataIntegrityRiskPoints: initialData?.dataIntegrityRiskPoints || 0,
                legalComplianceIssueDetected: initialData?.legalComplianceIssueDetected || false
            });
        }

        // 클린업 함수 (필요시)
        return () => {
            console.log("Loss Scorecard Hook cleanup.");
        };
    }, [initialData, updateScorecard]);


    return {
        scorecard: currentState,
        history: history,
        isLoading,
        // 외부에서 호출할 수 있는 액션 핸들러 제공
        onInputChange: (newData: Partial<LossScorecardInputData>) => {
            updateScorecard({
                timeElapsedHours: newData.timeElapsedHours ?? 0,
                dataIntegrityRiskPoints: newData.dataIntegrityRiskPoints ?? 0,
                legalComplianceIssueDetected: newData.legalComplianceIssueDetected ?? false
            });
        }
    };
};

// TypeScript 타입 정의를 명시적으로 export하여 외부에서 사용할 수 있도록 합니다.
export type UseLossScorecardHook = ReturnType<typeof useLossScorecard>;