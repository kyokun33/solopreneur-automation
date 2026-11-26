// useLossSimulation.ts
import { useState, useEffect } from 'react';

/**
 * @typedef {object} LossData
 * @property {number} score - 현재 손실 점수 (0~100)
 * @property {boolean} isCritical - 임계치 초과 여부 (Red Warning 발동 조건)
 * @property {string} riskDescription - 리스크 상세 설명 텍스트
 */

/**
 * 데이터 시뮬레이션 및 Loss State를 관리하는 커스텀 훅.
 * 실제 환경에서는 API 호출을 통해 데이터를 받아와야 합니다.
 * @returns {[LossData, React.Dispatch<React.SetStateAction<number>>]} 현재 상태와 스코어 업데이트 함수
 */
export const useLossSimulation = () => {
    const [score, setScore] = useState(90); // 초기 높은 점수 설정 (Normal Zone)

    useEffect(() => {
        // 1초마다 스코어를 임의로 하락시켜서 Critical State를 테스트할 수 있도록 합니다.
        const interval = setInterval(() => {
            setScore(prevScore => {
                if (prevScore > 0) {
                    // 점수를 조금씩 낮춥니다. (랜덤 감소 폭: 1~5)
                    const newScore = Math.max(0, prevScore - Math.floor(Math.random() * 5) - 1);
                    return newScore;
                } else {
                    clearInterval(interval);
                    return 0;
                }
            });
        }, 2000);

        // 클린업 함수
        return () => clearInterval(interval);
    }, []);

    const isCritical = score < 40; // 임계치: 40점 이하일 때 Critical State로 간주

    const lossData = {
        score: score,
        isCritical: isCritical,
        riskDescription: isCritical ? "⚠️ 데이터 무결성 위협 감지. 즉각적인 규제 리스크 점검이 필요합니다." : "현재 시스템은 안정적입니다. 하지만 방심은 금물입니다.",
    };

    return [lossData, setScore];
};