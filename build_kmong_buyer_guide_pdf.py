import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
OUTPUT_PDF = os.path.join(ROOT_DIR, "static", "크몽_구매고객_전용_AI보고서생성기_이용가이드.pdf")

# 폰트 지정
FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\malgunbd.ttf"

MAIN_FONT = "Helvetica"
BOLD_FONT = "Helvetica-Bold"

if os.path.exists(FONT_PATH):
    try:
        pdfmetrics.registerFont(TTFont("Malgun", FONT_PATH))
        MAIN_FONT = "Malgun"
    except Exception:
        pass

if os.path.exists(FONT_BOLD_PATH):
    try:
        pdfmetrics.registerFont(TTFont("Malgun-Bold", FONT_BOLD_PATH))
        BOLD_FONT = "Malgun-Bold"
    except Exception:
        BOLD_FONT = MAIN_FONT
else:
    if MAIN_FONT == "Malgun":
        BOLD_FONT = "Malgun"

def build_kmong_buyer_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=35,
        rightMargin=35,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title', fontName=BOLD_FONT, fontSize=20, leading=26,
        textColor=colors.HexColor("#1e1b4b"), spaceAfter=15, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'SubTitle', fontName=MAIN_FONT, fontSize=11, leading=16,
        textColor=colors.HexColor("#4338ca"), spaceAfter=20, alignment=1
    )
    h2_style = ParagraphStyle(
        'H2', fontName=BOLD_FONT, fontSize=13, leading=18,
        textColor=colors.HexColor("#1e293b"), spaceBefore=15, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'Body', fontName=MAIN_FONT, fontSize=10, leading=16,
        textColor=colors.HexColor("#334155"), spaceAfter=8
    )
    code_style = ParagraphStyle(
        'Code', fontName=BOLD_FONT, fontSize=11, leading=16,
        textColor=colors.HexColor("#0f172a"), spaceBefore=5, spaceAfter=5, alignment=1
    )

    story = [
        Spacer(1, 10),
        Paragraph("🎉 [크몽 구매 고객 전용] AI 보고서 생성기 이용 안내서", title_style),
        Paragraph("구매해 주셔서 감사합니다! 아래 접속 주소를 통해 3초 만에 사업계획서를 완결하세요.", subtitle_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#6366f1"), spaceAfter=15),

        Paragraph("📌 1. 라이브 웹 서비스 전용 접속 주소", h2_style),
        Paragraph("아래 주소를 클릭하여 브라우저에서 접속해 주세요:", body_style),
        Paragraph("<b>https://solopreneur-automation.onrender.com</b>", code_style),
        Spacer(1, 10),

        Paragraph("⚡ 2. 3초 완결 보고서 생성 및 인증 방법", h2_style),
        Paragraph("<b>STEP 1:</b> 라이브 웹사이트 접속 후 🔑 <b>1회용 인증 코드 입력란에 [크몽 주문번호]</b> 입력", body_style),
        Paragraph("<b>STEP 2:</b> 보고서 유형 선택 (정부지원사업용 / IR 투자유치용 / 시장분석용)", body_style),
        Paragraph("<b>STEP 3:</b> 사업 프로젝트명, 타겟 고객, 예산 및 핵심 기능 입력", body_style),
        Paragraph("<b>STEP 4:</b> [🚀 AI 보고서 3초 자동 생성하기] 버튼 클릭 (1회 생성 시 주문번호 자동 소멸)", body_style),
        Paragraph("<b>STEP 5:</b> 완성된 마크다운(.md) 보고서 1초 다운로드 및 클립보드 복사", body_style),
        Spacer(1, 10),

        Paragraph("💡 3. 고객 지원 및 유의 사항", h2_style),
        Paragraph("• 본 플랫폼은 24시간 365일 무인 자동 구동됩니다.", body_style),
        Paragraph("• 무제한 보고서 재생성이 가능하며 다운로드 횟수에 제한이 없습니다.", body_style),
        Paragraph("• 수정 및 추가 문의 사항은 크몽 메시지 문의하기를 이용해 주세요.", body_style),
        Spacer(1, 20),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=10),
        Paragraph("© 고고플렉스 AI 연구소 - Solopreneur SaaS Automation", ParagraphStyle('Foot', fontName=MAIN_FONT, fontSize=8, textColor=colors.HexColor("#94a3b8"), alignment=1))
    ]

    doc.build(story)
    print(f"[SUCCESS] Kmong Buyer PDF Generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_kmong_buyer_pdf()
