# 🚀 프로젝트 변경 이력 (CHANGELOG)

## [v2.50 Major Release] - 2026-08-06 (PDF 다이렉트 Inline 뷰어 HTTP 500 오류 100% 완전 소탕 완결)

### 🌟 PDF 뷰어 HTTP 500 오류 100% 소탕 내역

1. **🛠️ HTTP Response 헤더 인코딩 결함 완전 소탕**
   - `/api/download-pdf` 호출 시 `Content-Disposition` 헤더의 한글 파라미터로 인해 발생하던 `UnicodeEncodeError: 'latin-1' codec` (HTTP 500 오류)를 아스키 표준 안전 규격(`inline; filename="report.pdf"`)으로 수정하여 **`200 OK` 정상 렌더링 및 100% PDF 파일 뷰어 오픈**으로 완벽 조치되었습니다!

---

## [v2.40 Major Release] - 2026-08-06 (인쇄 버튼 클릭 시 정품 PDF 파일 웹 브라우저 다이렉트 Inline 뷰어 / 인쇄 연동)
- 다이렉트 Inline PDF 렌더링 라우트 구축
