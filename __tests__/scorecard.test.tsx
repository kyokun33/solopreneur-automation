import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import DataIntegrityScorecard from '@/app/page'; // 메인 페이지 컴포넌트 임포트

// Mocking 필수 모듈 정의 (실제 환경에서 jest.mock을 사용해야 함)
jest.mock('@/lib/api/diagnosisService', () => ({
  fetchDiagnosisData: jest.fn(),
}));

jest.mock('@/components/widgets/ScoreGaugeWidget', () => ({ __esModule: true, default: ({ score }) => <div data-testid="score-gauge">점수: {score}</div> }));
jest.mock('@/components/widgets/LossPotentialWidget', () => ({ __esModule: true, default: ({ riskFactors }) => <div data-testid="loss-potential">위험 요인 분석 완료 (Count: {riskFactors.length})</div> }));
jest.mock('@/components/widgets/AntiLossFunnelVisualization', () => ({ __esModule: true, default: ({ lossAmount }) => <div data-testid="funnel-visualization">손실 예측액 시각화 - ${lossAmount} USD</div> }));


describe('DataIntegrityScorecard E2E Integration Test Suite', () => {
  // API 호출을 Mocking하여 테스트 환경의 외부 의존성을 제거합니다.
  const mockFetchDiagnosisData = require('@/lib/api/diagnosisService').fetchDiagnosisData;

  beforeEach(() => {
    jest.clearAllMocks();
  });


  it('1. [Happy Path] 초기 로드 시 정상적으로 모든 컴포넌트가 렌더링 되는지 검증 (Initial Load Test)', async () => {
    // Mocking 성공 케이스 데이터 설정
    mockFetchDiagnosisData.mockResolvedValue({
      score: 78,
      loss_potential_usd: 15000, // $15,000 손실 가정
      risk_factors: ['API Latency', 'Poor Schema Design']
    });

    // React의 비동기 데이터 로딩을 위해 act와 await 사용
    render(<DataIntegrityScorecard />);
    await act(async () => { 
        // 컴포넌트가 마운트되면서 useEffect 내부에 있는 handleDiagnosis()를 호출하게 함.
        await new Promise(resolve => setTimeout(resolve, 10));
    });

    // 필수 요소 확인 (핵심 검증)
    expect(screen.getByText('데이터 무결성 스코어카드')).toBeInTheDocument();
    expect(mockFetchDiagnosisData).toHaveBeenCalledTimes(1); // API가 한 번 호출되었는지 확인
    
    // 렌더링된 위젯들의 데이터 기반 존재 여부 확인
    expect(screen.getByTestId('score-gauge')).toHaveTextContent('점수: 78');
    expect(screen.getByTestId('funnel-visualization')).toHaveTextContent('$15000 USD');
    expect(screen.getByTestId('loss-potential')).toHaveTextContent('(Count: 2)');

  });

  it('2. [Error Handling] API 호출 실패 시, 적절한 에러 메시지가 표시되는지 검증 (Failure Test)', async () => {
    // Mocking 실패 케이스 데이터 설정
    mockFetchDiagnosisData.mockRejectedValue(new Error("Network Timeout"));

    render(<DataIntegrityScorecard />);
    await act(async () => { 
        await new Promise(resolve => setTimeout(resolve, 10));
    });

    // 로딩 실패 후 에러 메시지가 표시되어야 함
    expect(screen.getByText(/진단 서비스 연결에 실패했습니다/i)).toBeInTheDocument();
  });

  it('3. [E2E Flow] 수동 진단 버튼 클릭 시, 상태가 정상적으로 전환되는지 검증 (User Interaction Test)', async () => {
    // 초기에는 데이터가 로드되지 않은 빈 상태로 시작한다고 가정하고 mock 설정
    mockFetchDiagnosisData.mockResolvedValue({
      score: 95,
      loss_potential_usd: 500,
      risk_factors: []
    });

    render(<DataIntegrityScorecard />);
    await act(async () => { 
        // 초기 로딩 단계 통과 후 (첫 호출은 무시하거나 재설정)
        mockFetchDiagnosisData.mockClear(); // 첫 호출 제외
        // 수동으로 버튼 클릭을 트리거합니다.
        const diagnoseButton = screen.getByRole('button', /데이터 무결성 진단 시작/i);
        fireEvent.click(diagnoseButton); 

        await new Promise(resolve => setTimeout(resolve, 10)); // 비동기 대기
    });
    
    // 버튼 텍스트와 결과가 정상적으로 바뀌었는지 확인 (상태 전환 검증)
    expect(mockFetchDiagnosisData).toHaveBeenCalledTimes(1); // 재호출 확인
    expect(screen.getByRole('button')).toHaveTextContent('진단 중'); // 로딩 상태
  });
});