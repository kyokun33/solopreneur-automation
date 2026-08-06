import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Preformatted, PageBreak, Image, Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MD_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\2번_아이템_1인기업_AI자동화_프롬프트100선_전자책.md"
PDF_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\1인기업_AI자동화_프롬프트100선_전자책.pdf"

COVER_IMG_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static\ebook_cover.png"
STEP_ICONS_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static\step_icons_3d.png"

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
                self.drawRightString(200 * 2.83, 280 * 2.83, "1인 기업가를 위한 AI 업무 자동화 비밀 프롬프트 100선")
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(15 * 2.83, 278 * 2.83, 200 * 2.83, 278 * 2.83)
                
                page_text = f"- {self._pageNumber} / {num_pages} -"
                self.drawCentredString(105 * 2.83, 12 * 2.83, page_text)
                self.restoreState()
            super().showPage()
        super().save()

def build_pdf():
    if not os.path.exists(MD_PATH):
        print(f"파일이 없습니다: {MD_PATH}")
        return

    with open(MD_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(
        PDF_PATH,
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
        fontSize=20,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        fontName='Malgun',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Malgun-Bold',
        fontSize=15,
        leading=21,
        textColor=colors.HexColor("#4f46e5"),
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Malgun-Bold',
        fontSize=12,
        leading=17,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        fontName='Malgun-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Malgun',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        fontName='Malgun',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#6366f1"),
        borderWidth=1.5,
        borderPadding=10,
        spaceBefore=6,
        spaceAfter=12
    )

    story = []

    # 1. Cover
    story.append(Spacer(1, 10))
    if os.path.exists(COVER_IMG_PATH):
        story.append(Image(COVER_IMG_PATH, width=380, height=220))
        story.append(Spacer(1, 15))
    
    story.append(Paragraph("💡 밤샘 일하던 1인 기업가가<br/>하루 4시간만 일하고 매출 2배 만든 프롬프트 100선", title_style))
    story.append(Paragraph("<b>[ 3초 복사+붙여넣기 무자본 무인 수익화 실전 치트키 완장판 ]</b>", subtitle_style))
    story.append(HRFlowable(width="70%", thickness=2, color=colors.HexColor("#4f46e5"), spaceAfter=20))
    story.append(Paragraph("<b>저자</b>: Antigravity 1인기업 AI 연구소 &nbsp;|&nbsp; <b>정가</b>: 29,000원 (디지털 무한 소장판)", subtitle_style))
    story.append(PageBreak())

    # Crisp Step Section on Page 2
    if os.path.exists(STEP_ICONS_PATH):
        story.append(Paragraph("<b>⚡ 1초 만에 따라하는 선명한 4단계 실행 가이드</b>", h2_style))
        story.append(Image(STEP_ICONS_PATH, width=480, height=130))
        story.append(Spacer(1, 10))

    # Crisp Step Table
    table_data = [
        [
            Paragraph("<b>STEP 01</b><br/>📋 1초 복사", h3_style),
            Paragraph("<b>STEP 02</b><br/>💬 대화창 붙여넣기", h3_style),
            Paragraph("<b>STEP 03</b><br/>📌 내 정보 입력", h3_style),
            Paragraph("<b>STEP 04</b><br/>⚡ 3초 자동 완성", h3_style),
        ],
        [
            Paragraph("[1초 복사] 버튼 클릭", body_style),
            Paragraph("ChatGPT 대화창 Ctrl+V", body_style),
            Paragraph("[ ] 괄호에 내 제품명 입력", body_style),
            Paragraph("엔터 치면 3초 만에 원고 완결", body_style),
        ]
    ]
    step_table = Table(table_data, colWidths=[125, 125, 125, 125])
    step_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#c7d2fe")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(step_table)
    story.append(Spacer(1, 15))

    # 2. Content Parser
    in_code = False
    code_lines = []

    for line in lines:
        raw_line = line.rstrip()
        stripped = raw_line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            if not in_code:
                code_text = "\n".join(code_lines)
                story.append(Preformatted(code_text, code_style))
                code_lines = []
            continue

        if in_code:
            code_lines.append(raw_line)
            continue

        if stripped.startswith("# "):
            story.append(Paragraph(stripped[2:], h1_style))
        elif stripped.startswith("## "):
            story.append(Paragraph(stripped[3:], h2_style))
        elif stripped.startswith("### "):
            story.append(Paragraph(stripped[4:], h3_style))
        elif stripped.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceBefore=10, spaceAfter=10))
        elif stripped:
            clean_text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(clean_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"선명한 벡터 인포그래픽 PDF 재빌드 완료: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
