import os
import sys
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak, Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PDF_FILENAME = "0원_무제한_웹배포_및_크몽_자동응답_설정가이드.pdf"
LOCAL_PDF_PATH = os.path.abspath(f"static/{PDF_FILENAME}")

desktop_paths = [r'C:\Users\sude3\OneDrive\바탕 화면', r'C:\Users\sude3\Desktop']
target_desktop = desktop_paths[0]
for d in desktop_paths:
    if os.path.exists(d):
        target_desktop = d
        break

DESKTOP_PDF_PATH = os.path.join(target_desktop, PDF_FILENAME)

# 폰트 등록
FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\malgunbd.ttf"

pdfmetrics.registerFont(TTFont("Malgun", FONT_PATH))
if os.path.exists(FONT_BOLD_PATH):
    pdfmetrics.registerFont(TTFont("Malgun-Bold", FONT_BOLD_PATH))
else:
    pdfmetrics.registerFont(TTFont("Malgun-Bold", FONT_PATH))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.saveState()
                self.setFont("Malgun", 8)
                self.setFillColor(colors.HexColor("#64748b"))
                self.drawRightString(200 * 2.83, 280 * 2.83, "0원 무제한 웹배포 및 크몽 0초 자동응답 설정 가이드북")
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(15 * 2.83, 278 * 2.83, 200 * 2.83, 278 * 2.83)
                
                page_text = f"- {self._pageNumber} / {num_pages} -"
                self.drawCentredString(105 * 2.83, 12 * 2.83, page_text)
                self.restoreState()
            super().showPage()
        super().save()

def make_box(text, style, bg_color="#f8fafc", border_color="#6366f1"):
    clean_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
    p = Paragraph(clean_text, style)
    t = Table([[p]], colWidths=[520])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor(border_color)),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def generate_pdf():
    os.makedirs("static", exist_ok=True)
    doc = SimpleDocTemplate(
        LOCAL_PDF_PATH,
        pagesize=A4,
        leftMargin=35,
        rightMargin=35,
        topMargin=45,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Malgun-Bold',
        fontSize=18,
        leading=26,
        textColor=colors.HexColor("#1e1b4b"),
        alignment=1,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Malgun',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Malgun-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#4338ca"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Malgun-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Malgun',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=5
    )

    prompt_style = ParagraphStyle(
        'Prompt_Custom',
        fontName='Malgun',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title
    story.append(Spacer(1, 5))
    story.append(Paragraph("🌐 0원 무료 무제한 웹배포 &<br/>크몽 0초 자동응답 설정 가이드북", title_style))
    story.append(Paragraph("<b>[ 100% 무인 0초 세일즈 자동화 연동 3단계 매뉴얼 ]</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4338ca"), spaceAfter=14))

    # Intro Callout Box
    intro_p = Paragraph(
        "<b>📌 무인 자동화 핵심 구조</b><br/>"
        "1. <b>24시간 무료 웹 배포</b>: Render.com / PythonAnywhere를 통한 0원 무제한 호스팅 주소 생성<br/>"
        "2. <b>크몽 0초 자동 안내 메시지</b>: 결제 즉시 크몽이 고객에게 자동 링크 및 사용법 발송<br/>"
        "3. <b>고객 100% 셀프 다운로드</b>: 대표님 관여도 0%로 결제 및 서비스 제공 완결!",
        body_style
    )
    intro_table = Table([[intro_p]], colWidths=[520])
    intro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0e7ff")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#6366f1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(intro_table)
    story.append(Spacer(1, 10))

    # Section 1: Render.com 0-won free hosting
    story.append(Paragraph("1. Render.com 0원 무료 클라우드 웹 배포 3단계", h1_style))
    
    render_steps = (
        "STEP 1. Render.com 무료 회원가입 (render.com)\n"
        "- GitHub 로그인 또는 이메일 1분 가입 후 [New +] ➔ [Web Service] 선택\n\n"
        "STEP 2. report_generator 폴더 연동\n"
        "- 프로젝트 내 준비된 'report_generator' 소스 폴더 연결\n"
        "- Build Command: pip install -r requirements.txt\n"
        "- Start Command: gunicorn main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT\n\n"
        "STEP 3. 0원 전용 웹주소 발급 완료\n"
        "- 3분 후 https://ai-report-saas.onrender.com 전용 무제한 HTTPS 주소 생성!"
    )
    story.append(make_box(render_steps, prompt_style, bg_color="#f8fafc", border_color="#6366f1"))
    story.append(Spacer(1, 10))

    # Section 2: Kmong Auto Response Message
    story.append(Paragraph("2. 크몽 0초 자동 안내 메시지 설정방법", h1_style))
    story.append(Paragraph("크몽 마이페이지 ➔ [서비스 관리] ➔ [자동 안내 메시지] 설정 메뉴에 아래 문구를 복사해서 등록해 둡니다.", body_style))

    kmong_auto_msg = (
        "안녕하세요, 대표님! [Antigravity AI 연구소]입니다. 결제해 주셔서 감사드립니다. 😊\n\n"
        "아래 전용 자동 생성기 웹 링크로 접속하시면 3초 만에 나만의 사업계획서 PDF가 완결됩니다!\n\n"
        "👉 무인 자동 생성기 웹 접속: https://ai-report-saas.onrender.com (전용 배포 주소)\n\n"
        "[사용 방법]\n"
        "1. 위 링크 접속 후 [사업 아이템명], [타겟 고객], [핵심 기능] 입력\n"
        "2. [✨ 사업계획서 자동 생성하기] 클릭 ➔ 3초 만에 완성!\n"
        "3. [🖨️ PDF 발급] 또는 [.MD 다운로드] 누르면 바로 사용 가능합니다.\n\n"
        "이용 중 문의사항은 메시지 남겨주시면 친절히 안내해 드리겠습니다. 감사합니다! 🙏"
    )
    story.append(make_box(kmong_auto_msg, prompt_style, bg_color="#f0fdf4", border_color="#10b981"))
    story.append(Spacer(1, 10))

    # Section 3: Littly Alternative
    story.append(Paragraph("3. 리틀리(Littly.is) 마켓 무인 연동 대안", h1_style))
    story.append(Paragraph("크몽 외에 카카오톡/블로그 프로필 링크로 판매할 때는 리틀리(Littly) 무료 마켓에 상품을 올려두면 결제 즉시 리틀리 시스템이 0초 만에 카카오톡으로 접속 주소를 보냅니다.", body_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph("<i>(C) 2026 고고플렉스AI 연구소 All Rights Reserved.</i>", subtitle_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Local PDF build complete: {LOCAL_PDF_PATH}")

    # Copy to Desktop
    shutil.copy(LOCAL_PDF_PATH, DESKTOP_PDF_PATH)
    print(f"Desktop PDF copied successfully: {DESKTOP_PDF_PATH}")

if __name__ == "__main__":
    generate_pdf()
