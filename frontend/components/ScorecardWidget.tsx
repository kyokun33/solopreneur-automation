// ScorecardWidget.tsx (React Component Stub)
import React, { useState, useEffect } from 'react';
import axios from 'axios'; // 실제 호출 시 사용될 라이브러리 가정

interface LossData {
    total_estimated_loss: number;
    final_integrity_score: number;
    breakdown: Record<string, number>;
}

// NOTE: 이 컴포넌트는 backend/main.py가 실행되는 서버 주소에서 API를 호출한다고 가정합니다.
const ScorecardWidget: React.FC = () => {
    const [lossData, setLossData] = useState<LossData | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // 🚨 API 호출 로직 (실제 환경에서는 서버 엔드포인트를 사용)
        const fetchLossData = async () => {
            setIsLoading(true);
            try {
                // Mock API Call: /api/v1/calculate_loss
                // 실제로는 axios.get('/api/v1/mock_data')를 호출 후, 데이터를 조합하여 POST 요청을 보내야 합니다.
                console.log("🚀 Calling backend loss calculation endpoint...");
                await new Promise(resolve => setTimeout(resolve, 500)); // API 지연 시뮬레이션

                // 테스트 스위트에서 검증된 Mock 결과를 사용합니다.
                const mockResult: LossData = {
                    total_estimated_loss: 2145.36, // T+3 years의 높은 페널티 반영 값
                    final_integrity_score: 78.0,
                    breakdown: {
                        "T+1 year_Loss": 150.0,
                        "T+3 years_Loss": 1500.0, // 가장 큰 손실 원인 강조
                        "T+5 years_Loss": 495.36,
                    }
                };
                setLossData(mockResult);

            } catch (error) {
                console.error("Failed to fetch loss data:", error);
                // 에러 메시지 처리 로직 추가 필요
            } finally {
                setIsLoading(false);
            }
        };
        fetchLossData();
    }, []);

    if (isLoading) {
        return <div className="loading-state">데이터 분석 중... API 연동을 기다려 주세요.</div>;
    }

    const handleHover = (key: string, value: number) => {
        // 🚨 Designer Spec 준수: Hover 시 위기감 극대화 팝업/설명 로직 구현 필요
        console.log(`[Hover Triggered] ${key}: 손실 원인 상세 분석 시작.`);
    };

    return (
        <div className="scorecard-container">
            {/* H1: Anti-Loss Hook 배치 영역 */}
            <h1>🚨 데이터 무결성 경고: 예상 비용 {lossData?.total_estimated_loss.toLocaleString()}원!</h1>
            <p className={`score-text ${lossData?.final_integrity_score < 80 ? 'warning' : ''}`}>
                현재 시스템의 손실 예측 스코어: {lossData?.final_integrity_score}%
            </p>

            {/* Loss Counter 위젯 (애니메이션 구현 필요) */}
            <div className="loss-counter">
                🔥 예상 최대 손실액: <span data-testid="total-loss">${lossData?.total_estimated_loss.toLocaleString()}</span>원
            </div>

            {/* 손실 Breakdown 섹션 (차트/그래프 표시 영역) */}
            <div className="breakdown-section">
                <h2>손실 원인 분석</h2>
                {/* 이 부분에 실제 Chart.js 또는 D3.js 기반의 그래프가 들어갑니다. */}
                <p>데이터 결핍 구간별 손실 분포 (Pie/Bar Graph 구현 예정)</p>
                {Object.entries(lossData?.breakdown || {}).map(([key, value]) => (
                    <div key={key} className="data-component" onMouseEnter={() => handleHover(key, value)}>
                        <strong>{key}:</strong> ${value.toLocaleString()}원
                    </div>
                ))}
            </div>

             {/* CTA: 이득 기반의 구체적 행동 유도 문구 사용 */}
            <button className={`cta-button ${lossData?.final_integrity_score < 80 ? 'warning' : ''}`}>
                ✅ 데이터 안정성 확보 및 리스크 제거 계획 보기
            </button>
        </div>
    );
};

export default ScorecardWidget;