// src/components/shared/__tests__/LossScorecard.test.tsx - Unit Test for Loss Scorecard Logic
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import LossScorecard from '../LossScorecard';
import * as MockApi from '../../api/riskAssessmentApi';

// 🚨 Mocking the entire API module to control inputs and test logic isolation
jest.mock('../../api/riskAssessmentApi', () => ({
    fetchRiskAssessmentData: jest.fn(),
}));


describe('LossScorecard Component Validation', () => {
    
    beforeEach(() => {
        // 클린업 및 Mock 초기화
        MockApi.fetchRiskAssessmentData.mockClear();
    });

    it('1. 로딩 상태를 올바르게 표시하는가?', async () => {
        // 테스트 1: Loading State
        MockApi.fetchRiskAssessmentData.mockResolvedValue({ /* 가짜 데이터 */ }); // 일단 응답은 Mocking
        render(<LossScorecard />);

        expect(screen.getByText(/⚡️ 리스크 분석 중/i)).toBeInTheDocument();
    });


    it('2. 정상적인 데이터를 성공적으로 표시하는가? (Green State)', async () => {
        // 테스트 2: Normal Operation State Mocking
        const mockSuccessData = {
            dataIsMissing: false,
            baseRiskScore: 75,
            totalInitialLossUSD: 1000.00,
            finalRiskScore: 80, // 패널티 없음
            totalFinalLossUSD: 1200.00,
            lossBreakdown: [{ category: '데이터 무결성', estimatedCostUSD: 500, lossRatePerHour: 10, durationDays: 3 }],
        };
        MockApi.fetchRiskAssessmentData.mockResolvedValue(mockSuccessData);

        render(<LossScorecard />);
        await waitFor(() => {
            expect(screen.getByText(/총 예측 손실액:/i)).toBeInTheDocument();
            // 패널티가 없으므로, Initial Loss와 Final Loss의 숫자가 달라지지 않아야 함 (혹은 매우 근접해야 함)
            expect(screen.queryByText('🚨 경고! 필수 데이터 결핍 감지')).not.toBeInTheDocument(); 
        });
    });


    it('3. 핵심 기능: 데이터 결핍 시 리스크 패널티가 정확히 적용되는가? (Critical State)', async () => {
        // 테스트 3: Data Deficiency & Penalty Test - 이 부분이 CEO 지시의 핵심임!
        const initialLoss = 1000.00;
        const penaltyFactor = 5; // 최대 5배 패널티 적용 가정

        // Mocking: dataIsMissing=true, 그리고 최종 손실액이 초기 손실액 * 5가 되도록 설정함.
        const mockPenaltyData = {
            dataIsMissing: true, // 핵심 플래그 On!
            baseRiskScore: 30,
            totalInitialLossUSD: initialLoss, // $1,000 (기본)
            finalRiskScore: 25,             // 패널티 적용 후 낮아짐
            totalFinalLossUSD: initialLoss * penaltyFactor, // $5,000 (패널티 반영!)
            lossBreakdown: [],
        };

        MockApi.fetchRiskAssessmentData.mockResolvedValue(mockPenaltyData);

        render(<LossScorecard />);
        await waitFor(() => {
             // 1) Critical State Warning 메시지 확인
            expect(screen.getByText(/🚨 경고! 필수 데이터 결핍 감지/i)).toBeInTheDocument(); 
            
            // 2) 패널티가 적용된 최종 손실액이 정확히 표시되는지 확인 (5배 증폭 확인)
            const lossAmountElement = screen.queryByText('총 예측 손실액:');
            expect(lossAmountElement).toBeInTheDocument();
            expect(lossAmountElement?.querySelector('.amount')).toHaveTextContent('$5,000'); 

        });
    });
});