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

PDF_FILENAME = "수정_재진행_환불_3초완결_대응가이드.pdf"
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
                self.drawRightString(200 * 2.83, 280 * 2.83, "AI 사업계획서 수정/재진행/환불 3초 완결 대응 가이드북")
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(15 * 2.83, 278 * 2.83, 200 * 2.83, 278 * 2.83)
                
                page_text = f"- {self._pageNumber} / {num_pages} -"
                self.drawCentredString(105 * 2.83, 12 * 2.83, page_text)
                self.restoreState()
            super().showPage()
        super().save()

def make_box(text, style, bg_color="#f8fafc", border_color="#6366f1"):
    # HTML escape
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
    story.append(Paragraph("🛠️ AI 사업계획서 수정 • 재진행 • 환불<br/>3초 완결 실전 대응 가이드북", title_style))
    story.append(Paragraph("<b>[ 1인 기업가를 위한 크몽 고객 문의 100% 무상처치 & 분쟁 제로 매뉴얼 ]</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4338ca"), spaceAfter=14))

    # Intro Callout
    intro_p = Paragraph(
        "<b>📌 핵심 응대 원칙</b><br/>"
        "1. <b>단순 문구 수정/보강 요청</b>: 챗GPT 3초 프롬프트로 즉시 처리 (고객 만족도 200%)<br/>"
        "2. <b>사업 주제 전체 변경 요청</b>: 규정에 따라 추가 결제(10,000원) 정중히 유도<br/>"
        "3. <b>시스템 오류 문의</b>: 기술 안내 및 필요 시 100% 환불 처리로 분쟁 제로 유지",
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

    # Section 1: Simple Revisions
    story.append(Paragraph("1. [유형 1] 단순 문구 보완 및 수정 요청 3초 처리법", h1_style))
    story.append(Paragraph("상황: 고객이 '내용을 더 풍부하게 해달라' 또는 '특정 항목을 보강해 달라'고 요청할 때", body_style))

    p1 = (
        "[역할] 너는 사업계획서 전문 편집 수석 에디터야.\n"
        "[지시] 고객이 요청한 수정 사항: '[고객의 수정 요청 사항, 예: 경쟁사 차별점 추가]'을 반영하여 아래 원고를 2배 더 풍부하고 전문적인 어조로 수정한 최종본을 작성해 줘.\n"
        "[제출 원고]\n[기존 생성된 원고 텍스트]"
    )
    story.append(make_box(p1, prompt_style))
    story.append(Spacer(1, 6))

    msg1 = (
        "안녕하세요, 대표님! 요청해 주신 수정 사항을 반영하여 보고서를 한층 더 정교하게 보강했습니다. 😊\n"
        "첨부해 드린 수정본 원고를 확인해 보시고, 추가로 보완이 필요하신 부분은 언제든 편하게 말씀해 주세요. 감사합니다!"
    )
    story.append(make_box(msg1, prompt_style, bg_color="#f0fdf4", border_color="#10b981"))
    story.append(Spacer(1, 10))

    # Section 2: Topic Change (Re-order)
    story.append(Paragraph("2. [유형 2] 사업 아이템 전체 변경 요청 시 정중한 추가 결제 유도", h1_style))
    story.append(Paragraph("상황: 고객이 'A 사업으로 받았는데 B 사업으로 아예 바꿔주세요'라고 요청할 때", body_style))

    msg2 = (
        "안녕하세요, 대표님! 전달해 주신 새로운 프로젝트 주제 잘 확인했습니다. 😊\n\n"
        "크몽 서비스 규정 안내에 따라, 단순 문구 수정이 아닌 [사업 아이템/주제 자체가 완전히 새로 변경되는 경우]에는 신규 생성 이용권(10,000원) 구매 후 재진행이 필요합니다.\n\n"
        "새로운 프로젝트에 맞춰 최상의 결과물로 빠르게 렌더링해 드릴 예정이오니, 아래 1회 생성 이용권을 추가로 결제해 주시면 3분 만에 전용 보고서를 바로 발급해 드리겠습니다! 감사합니다. 🙏"
    )
    story.append(make_box(msg2, prompt_style, bg_color="#fefce8", border_color="#f59e0b"))
    story.append(Spacer(1, 10))

    # Section 3: Refund & System Error
    story.append(Paragraph("3. [유형 3] 환불 문의 및 시스템 오류 응대 가이드", h1_style))
    
    refund_data = [
        [
            Paragraph("<b>문의 상황</b>", h2_style),
            Paragraph("<b>대응 가이드 및 3초 메시지</b>", h2_style)
        ],
        [
            Paragraph("<b>\"다운로드가 안 돼요\"</b>", body_style),
            Paragraph("크몽 메시지로 .MD 및 PDF 파일 원본 직접 첨부 전달 후 \"크몽 첨부파일로 직접 발송해 드렸습니다\" 안내", body_style)
        ],
        [
            Paragraph("<b>\"화면 렌더링 오류\"</b>", body_style),
            Paragraph("서버 재가동 확인 후 \"서버 점검 완료되어 이용권을 재발급해 드렸습니다\" 메시지 발송", body_style)
        ],
        [
            Paragraph("<b>\"단순 변심 환불\"</b>", body_style),
            Paragraph("\"생성 서비스 특성상 무상 수정 횟수 제공으로 보완을 도와드리겠습니다\" 정중 안내 후 3초 수정 제공", body_style)
        ]
    ]
    refund_table = Table(refund_data, colWidths=[150, 370])
    refund_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(refund_table)

    story.append(Spacer(1, 10))

    # Section 4: FAQ
    story.append(Paragraph("4. 자주 들어오는 질문(FAQ) 1초 답변 템플릿 3선", h1_style))

    faq1 = (
        "Q. 사업계획서를 한글(HWP) 파일로 받을 수 있나요?\n"
        "답변: 저희 서비스는 마크다운(.MD) 파일 및 PDF 출력을 기본 제공합니다. 마크다운 파일의 텍스트를 한글(HWP) 프로그램에 [복사+붙여넣기] 하시면 1초 만에 그대로 편집이 가능하십니다! 😊"
    )
    story.append(make_box(faq1, prompt_style, bg_color="#f8fafc", border_color="#94a3b8"))
    story.append(Spacer(1, 6))

    faq2 = (
        "Q. 분량을 2배로 더 길게 늘려줄 수 있나요?\n"
        "답변: 네, 대표님! 각 파트별 세부 실행 로드맵과 수치를 2배 강화한 디테일 확장본으로 보완하여 3분 내로 재발송해 드리겠습니다. 잠시만 기다려 주세요! 🙏"
    )
    story.append(make_box(faq2, prompt_style, bg_color="#f8fafc", border_color="#94a3b8"))

    story.append(Spacer(1, 10))
    story.append(Paragraph("<i>(C) 2026 고고플렉스AI 연구소 All Rights Reserved.</i>", subtitle_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Local PDF build complete: {LOCAL_PDF_PATH}")

    # Copy to Desktop
    shutil.copy(LOCAL_PDF_PATH, DESKTOP_PDF_PATH)
    print(f"Desktop PDF copied successfully: {DESKTOP_PDF_PATH}")

if __name__ == "__main__":
    generate_pdf()
