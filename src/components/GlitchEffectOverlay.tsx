// GlitchEffectOverlay.tsx
import React from 'react';

interface GlitchProps {
    isActive: boolean; // Red Warning이 발동되었는지 여부
}

/**
 * 임계치 도달 시 시스템 오류를 연출하는 글리치 효과 컴포넌트.
 * CSS 애니메이션과 결합하여 강한 위기감을 조성합니다.
 */
const GlitchEffectOverlay: React.FC<GlitchProps> = ({ isActive }) => {
    if (!isActive) return null;

    return (
        <div className="absolute inset-0 z-50 pointer-events-none opacity-75" style={{ 
            // Red Warning 색상을 배경으로 오버레이하여 시스템 오류 느낌을 강화합니다.
            backgroundColor: 'rgba(204, 51, 51, 0.3)' 
        }}>
            <div className="absolute top-0 left-0 w-full h-full animate-[glitch_animation_0.8s_infinite]"></div>
            <style jsx global>{`
                /* CSS Keyframes for the Glitch Effect */
                @keyframes glitch {
                    0% { transform: translate(0); opacity: 1; }
                    20% { transform: translate(-4px, -4px); opacity: 0.8; }
                    40% { transform: translate(-3px, 3px); opacity: 1; }
                    60% { transform: translate(3px, -3px); opacity: 0.9; }
                    80% { transform: translate(2px, 2px); opacity: 0.7; }
                    100% { transform: translate(0); opacity: 1; }
                }

                @keyframes glitch_animation {
                    0%, 100% { clip-path: inset(0%); transform: skewX(0deg); }
                    25% { clip-path: inset(40% 0 30% 0); transform: skewX(-1deg); opacity: 0.9; }
                    75% { clip-path: inset(60% 0 10% 0); transform: skewX(1deg); opacity: 0.8; }
                }
            `}</style>
        </div>
    );
};

export default GlitchEffectOverlay;