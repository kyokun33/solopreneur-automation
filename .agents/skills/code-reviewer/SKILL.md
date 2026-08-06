---
name: code-reviewer
description: 코드 품질, 보안 취약점 점검, 성능 최적화, 아키텍처 및 정적 분석 기반 전문 코드 리뷰 스킬
---

# 🔍 Code Reviewer Skill (코드 리뷰어 스킬)

본 스킬은 파이썬, 자바스크립트/타입스크립트, HTML/CSS 및 백엔드 서버 코드의 정적 분석, 보안 취약점 검증, 코드 품질 평가, 성능 최적화 및 리팩토링 지침을 제공합니다.

---

## 📌 주요 리뷰 점검 항목 (Review Checklist)

### 1. 🛡️ 보안 및 안전성 (Security & Safety)
- API 키, 하드코딩된 비밀번호, 결제 비밀키 노출 여부 점검
- SQL Injection, XSS(크로스사이트 스크립팅), Path Traversal 방지
- 사용자 입력 데이터 검증 및 예외 처리(Try-Catch) 누락 여부

### 2. ⚡ 성능 및 효율성 (Performance & Efficiency)
- 불필요한 반복문(Loop) 및 복잡도(Complexity) 최소화
- 비동기(async/await) 및 논블로킹 I/O 처리 검증
- 불필요한 파일/네트워크 I/O 병목 구간 제거

### 3. 🎨 코드 가독성 및 유지보수성 (Clean Code & Readability)
- 변수/함수명의 명확성 및 직관적 Naming Convention
- 함수 단위 단일 책임 원칙(SRP) 준수 여부
- 모듈화 및 재사용 가능한 유틸리티 추출

---

## 🚀 리뷰 실행 가이드

1. **자동 검증**: `py_compile` 또는 린터 검사를 통해 문법 오류 0건 유지.
2. **리팩토링 제안**: 수정 전/후 Diff를 명확히 제시하며 부작용(Side Effect) 사전 예방.
