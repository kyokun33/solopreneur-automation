import sys
import os
import pypdf

BASE_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "report_generator"))

from report_generator.schemas import ReportRequest
from report_generator.generator import generate_business_report, build_pdf_file

req = ReportRequest(
    title="개인 맞춤형 건강 다이어트 관리 서비스",
    category="government",
    program_type="packages_15p",
    target_customer="체중 관리·건강 개선이 필요한 20~40대 남녀",
    core_features="개인별 체성분·생활패턴 분석 기반 맞춤 식단·운동 코칭",
    budget="초기 예산 1,000만 원 / 월 목표 매출 500만 원",
    access_key="KM849201"
)

md_text, html_text = generate_business_report(req)
pdf_path = os.path.join(BASE_DIR, "scratch", "fix_markdown_test.pdf")
build_pdf_file(req, pdf_path)

reader = pypdf.PdfReader(pdf_path)
page_count = len(reader.pages)

print("=== [마크다운 HTML 파싱 및 부록 1페이지 수용 테스트 결과] ===")
print("PDF 총 페이지 수:", page_count, "페이지")

p_last = reader.pages[-1].extract_text()
p_prev = reader.pages[-2].extract_text()

print("HTML 변환 텍스트에 파싱 실패 문자(## 또는 |---|) 포함 여부 (포함 안 되어야 성공):", "## [정부지원사업" in html_text or "| :-" in html_text)
print("이전 페이지 본문 완결 여부:", "정부지원사업 지원 제외" not in p_prev)
print("마지막 페이지에 100% 부록 내용 수용 여부:", "정부지원사업 지원 제외" in p_last and "사업계획서 원본" in p_last)
