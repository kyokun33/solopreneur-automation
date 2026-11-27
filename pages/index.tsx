import React from 'react';
import LossScoreInputForm from '../components/loss-scorecard/LossScoreInputForm';
import LossScoreResultDisplay from '../components/loss-scorecard/LossScoreResultDisplay';

/**
 * 메인 페이지 컴포넌트: Loss Scorecard 전체를 통합합니다.
 */
const IndexPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <header className="mb-12 text-center">
                <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 mb-2">
                    고고플랙스 손실 점수 진단 시스템 💻
                </h1>
                <p className="text-lg text-gray-500">당신의 비즈니스에 숨어있는 '예상 비용'을 찾아냅니다.</p>
            </header>

            {/* 섹션 분리: Input (왼쪽/위) | Output (오른쪽/아래) */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
                
                {/* 1. 입력 폼 섹션 */}
                <div>
                    <LossScoreInputForm />
                </div>

                {/* 2. 결과 디스플레이 섹션 (가장 큰 영역 차지) */}
                <div>
                    <LossScoreResultDisplay />
                </div>

            </div>
        </div>
    );
};

export default IndexPage;