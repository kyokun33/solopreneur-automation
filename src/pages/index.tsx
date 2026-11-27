import React from 'react';
import LossScorecard from '../components/LossScorecard/LossScorecard';

// [테스트용 Mock Data] - 중간 정도의 리스크 시뮬레이션 데이터
const mockTestData = {
    'data_integrity': 2500, // 데이터 무결성 관련 손실 (가장 큰 요소)
    'compliance_risk': 300,  // 규제 준수 리스크
    'operational_lapse': 150.5, // 운영상의 실수 비용
};

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className='mb-12 text-center'>
          <h1 className="text-4xl font-bold mb-3">고고플랙스 - 법적 리스크 진단 시스템</h1>
          <p className="text-lg text-gray-600">당신의 비즈니스가 놓치고 있는 '돈으로 환산되는' 책임 영역을 측정합니다.</p>
      </header>

      {/* 핵심 컴포넌트 배치 */}
      <section className="max-w-xl mx-auto pt-10">
        <LossScorecard inputData={mockTestData} />
      </section>
    </div>
  );
};

export default HomePage;