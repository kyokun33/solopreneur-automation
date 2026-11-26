import React, { useState, useEffect, useMemo } from 'react';
import './LossScorecard.css'; // Assuming CSS file exists for animations/styling

// TypeScript Interface for strong typing
interface ScoreGaugeProps {
  initialScore: number;
  lossValue: float | null; // Must handle float and potential missing data (NaN)
}

const LossScorecard: React.FC<ScoreGaugeProps> = ({ initialScore, lossValue }) => {
  const [currentScore, setCurrentScore] = useState(initialScore);
  const [isBreached, setIsBreached] = useState(false);

  // 1. Score Calculation and State Update Logic (Memoized for performance)
  useEffect(() => {
    if (lossValue === null || isNaN(lossValue)) {
      setCurrentScore(initialScore);
      setIsBreached(true); // Data missing or invalid triggers breach state
      return;
    }

    // Assume a simple loss calculation: Score = Initial - Loss * Factor
    const calculatedLossFactor = 0.5; // Example factor for demonstration
    let newScore = initialScore - (lossValue * calculatedLossFactor);
    
    if (newScore < 0) {
        newScore = 0;
    }

    // Check if the loss is critical (e.g., > 30% of initial score)
    const breachThreshold = initialScore * 0.3;
    if (lossValue > breachThreshold / calculatedLossFactor) {
        setIsBreached(true);
    } else {
        setIsBreached(false);
    }

    setCurrentScore(newScore);

  }, [lossValue, initialScore]);


  // 2. Render Logic
  return (
    <div className={`score-gauge ${isBreached ? 'breach' : ''}`}>
      {/* Breaching Effect Overlay */}
      {isBreached && (
        <div className="data-breach-effect">
            ⚠️ DATA BREACH DETECTED. CRITICAL RISK LEVEL. ⚠️
        </div>
      )}

      <div className="score-display">
        <h1>{Math.floor(currentScore).toLocaleString()}</h1> {/* Displaying integer for readability */}
        <p>Current Data Integrity Score</p>
      </div>

      {/* Graph Visualization Placeholder */}
      <div className="graph-container">
        {/* In a real implementation, this would be an SVG or Canvas drawing the loss curve. */}
        <p>{isBreached ? '--- ERROR: DATA CORRUPTION ---' : '📊 Score Degradation Curve (Simulated)'}</p>
      </div>

      {/* Error Message / Warning Indicator */}
      <div className={`warning-indicator ${isBreached ? 'red' : 'yellow'}`}>
        {isBreached 
          ? `[ERROR] 데이터 손실 분석 실패. 근본 원인 확인 필요.` 
          : `${(100 - currentScore).toFixed(1)}% Loss Detected`}
      </div>
    </div>
  );
};

export default LossScorecard;