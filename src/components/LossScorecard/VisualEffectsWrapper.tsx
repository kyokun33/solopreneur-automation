import React, { ReactNode } from 'react';
import './VisualEffectsWrapper.css'; // CSS 파일이 필요합니다.

/**
 * @component VisualEffectsWrapper.tsx
 * @description Red Warning 필터 및 Glitch 효과 등 시각적 경고 시스템을 적용하는 레이어 컴포넌트입니다.
 * 이 컴포넌트는 오직 '보여지는 방식'만을 제어해야 합니다.
 */
const VisualEffectsWrapper: React.FC<{ children: ReactNode }> = ({ children }) => {
    return (
        <div className="visual-effect-wrapper">
            {/* Red Warning 필터 클래스 적용 */}
            <div className="red-warning-filter">
                {children}
            </div>
            <p className="glitch-overlay">[SYSTEM WARNING: DATA INTEGRITY COMPROMISED]</p> {/* Glitch 효과 시각적 요소 추가 */}
        </div>
    );
};

export default VisualEffectsWrapper;