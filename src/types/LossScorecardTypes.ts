/**
 * @fileoverview Loss Scorecard 시스템 전체에 사용되는 핵심 데이터 타입 및 API Contract 정의.
 * [근거: 2026-11-27T05:57] - 백엔드 개발은 정의된 API 계약(Contract)을 유일한 진실의 원천으로 사용한다.
 */

/**
 * @typedef {Object} RawUserInputData
 * @description 사용자로부터 입력받는 비구조화된 리스크 데이터 묶음.
 * @param {string} rawUserInputData.userIdentifier - 고유 사용자 ID (예: UUID).
 * @param {number} rawUserInputData.dataIntegrityRiskScore - 데이터 무결성 관련 점수 (0~100).
 * @param {number} rawUserInputData.complianceViolationCount - 규정 위반 횟수 (Count).
 * @param {string} rawUserInputData.industrySector - 산업 섹터 (예: Finance, HealthTech 등).
 */

/**
 * @typedef {Object} LossBreakdownItem
 * @description 손실 점수를 구성하는 개별 항목의 상세 정보.
 * @property {string} metricName - 측정 지표 이름 (예: "Data Integrity Risk", "Compliance Violation").
 * @property {number} scoreValue - 해당 지표가 기여한 점수 값.
 * @property {string} explanation - 이 점수가 왜 높은지 설명하는 카피라이팅(Writer Copy 활용).
 */

/**
 * @typedef {Object} LossScoreResult
 * @description 손실 정량화의 최종 결과물. Unit Test의 목표 객체.
 * @property {number} totalLossScore - 계산된 총 손실 점수 (소수점 2자리까지 허용).
 * @property {string} lossDescription - 사용자가 이해하기 쉬운 요약 문구 (예: "매우 높은 수준의 리스크 감지").
 * @property {LossBreakdownItem[]} breakdown - LossScore를 구성하는 상세 Breakdown 목록.
 * @property {number} calculatedOnTimestamp - 점수 산출 시점 타임스탬프.
 */

/**
 * @typedef {Object} ReportRequestPayload
 * @description 진단 보고서 요청을 위한 API 요청 페이로드.
 * @param {string} userIdentifier - 요청하는 사용자 ID.
 * @param {string} reportType - 원하는 보고서 종류 (예: 'Basic', 'Premium').
 */

/**
 * @typedef {Object} ReportResponse
 * @description 결제 게이트웨이를 거쳐 발행된 진단 보고서 응답.
 * @property {boolean} paymentSuccess - 결제 성공 여부.
 * @property {string | null} reportId - 발급된 보고서의 고유 ID (성공 시).
 * @property {string} message - 상태 메시지 (성공/실패 이유 포함).
 */

/**
 * API Contract: LossScoreCalculationService
 * Input: RawUserInputData
 * Output: Promise<LossScoreResult>
 */