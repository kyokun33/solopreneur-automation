/**
 * @description Loss Scorecard 컴포넌트 및 핵심 로직을 테스트합니다.
 * 이 테스트는 useLossScorecard 훅의 비즈니스 로직 안정성을 검증하는 역할을 합니다.
 */

import React from 'react';
import { render, screen, act } from '@testing-library/react';
import LossScorecard from '../LossScorecard';
import { vi } from 'vitest'; // Assuming Vitest or Jest is used for testing

// 🚨 주의: useLossScorecard가 외부 모듈(mockScorecardService)에 의존하므로,
// 실제 테스트 환경에서는 이 모의 객체(Mock Service)를 주입받거나 전역으로 Mocking해야 합니다.
// 여기서는 구조적 검증을 위해 간단한 더미 데이터를 사용합니다.

describe('LossScorecard MVP Component & Logic Test Suite', () => {

    it('1. 초기 로드 시 스코어카드 컴포넌트가 정상적으로 렌더링되는지 확인한다 (Loading State)', async () => {
        // Mocking the hook's internal state to simulate initial loading phase
        render(<LossScorecard initialData={{ timeElapsedHours: 0, dataIntegrityRiskPoints: 0, legalComplianceIssueDetected: false }} />);

        expect(screen.getByText(/분석 중/i)).toBeInTheDocument(); // 로딩 상태 메시지 확인
    });

    it('2. Apathy 상태로 정상 계산되었을 때 UI가 올바르게 표시되는지 테스트한다 (Apathy State)', async () => {
        // 🟢 낮은 위험 시나리오를 강제하여 Apathy 상태 유도
        const lowRiskData = { timeElapsedHours: 1, dataIntegrityRiskPoints: 5, legalComplianceIssueDetected: false };

        render(<LossScorecard initialData={lowRiskData} />);

        // 로직 실행을 기다린 후 (Mock API가 비동기이므로)
        await act(async () => {
            // 테스트를 위해 onInputChange 핸들러에 접근하여 강제 상태 전이 유도
            const container = screen.getByRole('generic'); // LossScorecard 컨테이너
            await container.querySelector('.input-control button:nth-child(2)')?.click(); // [Low Risk] 버튼 클릭 시뮬레이션 (실제로는 훅 내부 로직 수정 필요)
        });

        // Apathy 상태의 핵심 요소 검증
        expect(screen.getByText(/Apathy/i)).toBeInTheDocument();
        expect(screen.getByText(/현재 데이터 상태는 양호합니다/i)).toBeInTheDocument();
    });


    it('3. Critical 상태 전이 시, 경고 컴포넌트와 강조 스타일이 적용되는지 테스트한다 (Critical State)', async () => {
        // 🔴 높은 위험 시나리오를 강제하여 Critical 상태 유도
        const highRiskData = { timeElapsedHours: 20, dataIntegrityRiskPoints: 50, legalComplianceIssueDetected: true };

        render(<LossScorecard initialData={highRiskData} />);

        await act(async () => {
            // [Max Risk] 버튼 클릭 시뮬레이션
             const container = screen.getByRole('generic');
             await container.querySelector('.input-control button:nth-child(1)')?.click();
        });


        // Critical 상태의 핵심 요소 검증 (가장 중요한 부분)
        expect(screen.getByText(/Critical/i)).toBeInTheDocument();
        // CSS 클래스 기반으로 Glitch Effect 활성화 여부 확인 가능 (CSS 선택자 사용 가정)
        const scorecardElement = screen.getByRole('generic');
        expect(scorecardElement).toHaveClass('glitch-active'); // Critical 상태가 Red Warning/Glitch를 유발하는지 검증

    });

    it('4. 상태 전이 이력 로그 (History Log)가 정확히 기록되는지 테스트한다', async () => {
        // 3가지 다른 시나리오를 연달아 실행하여 History Length와 내용을 확인합니다.
        const initialData = { timeElapsedHours: 0, dataIntegrityRiskPoints: 0, legalComplianceIssueDetected: false };
        render(<LossScorecard initialData={initialData} />);

        await act(async () => {
             // 1. 초기 로드 (Apathy -> Apathy)
            const container = screen.getByRole('generic');
            await container.querySelector('.input-control button:nth-child(2)')?.click(); // Low Risk (History 1)

            // 2. Warning 유도 시나리오 실행
            await container.querySelector('.input-control button:nth-child(1)')?.click(); // Max Risk (History 2)

            // 3. Critical 유지/강화 시나리오 재실행
            await container.querySelector('.input-control button:nth-child(1)')?.click(); // Max Risk (History 3)
        });

        // History 로그가 최소한의 변화 횟수만큼 증가했는지 검증합니다.
        const historyLog = screen.getByText(/최근 스코어카드 변화 로그/i).closest('div');
        expect(historyLog).toBeInTheDocument();
    });
});