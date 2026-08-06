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

PDF_FILENAME = "1대1_맞춤피드백_3초완결_대응가이드.pdf"
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
                self.drawRightString(200 * 2.83, 280 * 2.83, "AI 사업계획서 1:1 맞춤 피드백 3초 완결 대응 가이드북")
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

    # 1. Cover / Header
    story.append(Spacer(1, 5))
    story.append(Paragraph("💡 AI 사업계획서 1:1 맞춤 피드백<br/>3초 완결 실전 대응 가이드북", title_style))
    story.append(Paragraph("<b>[ 크몽 PREMIUM 49,000원 결제 고객 전담 튜닝 대응 매뉴얼 ]</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#4338ca"), spaceAfter=14))

    # Intro Callout Box
    intro_p = Paragraph(
        "<b>📌 핵심 마인드셋</b><br/>"
        "크몽 PREMIUM(49,000원) 구매 고객에게 직접 손으로 글을 써줄 필요가 전혀 없습니다.<br/>"
        "고객이 제출한 텍스트를 <b>챗GPT/Claude 전문 프롬프트 1줄</b>에 복사해 넣으면 3초 만에 10년 차 수석 컨설턴트 수준의 고품격 튜닝 원고가 완성됩니다.",
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

    # Section 1: 3-Step Workflow
    story.append(Paragraph("1. 3초 맞춤 튜닝 3단계 처리 프로세스", h1_style))
    
    proc_data = [
        [
            Paragraph("<b>STEP 01: 원고 수령</b>", h2_style),
            Paragraph("<b>STEP 02: 챗GPT 3초 튜닝</b>", h2_style),
            Paragraph("<b>STEP 03: 정중 전달</b>", h2_style)
        ],
        [
            Paragraph("고객이 작성한 사업계획서 텍스트 또는 .MD 파일 수령", body_style),
            Paragraph("본 가이드북의 목적별 튜닝 프롬프트에 복사+붙여넣기", body_style),
            Paragraph("완성본을 크몽 대화창으로 정중한 메시지와 함께 발송", body_style)
        ]
    ]
    proc_table = Table(proc_data, colWidths=[170, 175, 175])
    proc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#ffffff")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(proc_table)
    story.append(Spacer(1, 10))

    # Section 2: Core Tuning Prompts
    story.append(Paragraph("2. 목적별 3초 1:1 맞춤 튜닝 치트키 프롬프트 3선", h1_style))

    story.append(Paragraph("📌 [치트키 1] 정부지원사업(예창패/초창패) 합격 저격 튜닝", h2_style))
    p1 = (
        "[역할] 너는 정부지원사업(예비창업패키지/초기창업패키지) 수석 심사위원이야.\n"
        "[지시] 아래 제출된 사업계획서 원고를 심사 기준 4대 항목(문제성, 실현가능성, 성장전략, 팀구성)에 맞춰 합격률이 3배 높아지도록 보완해 줘.\n"
        "[보완 원칙] 1) 모호한 표현을 구체적 수치/통계로 변경 2) 타깃 시장 TAM-SAM-SOM 명확화 3) 독점적 차별화 가치 강조\n"
        "[제출 원고]\n[고객 사업계획서 텍스트 붙여넣기]"
    )
    story.append(make_box(p1, prompt_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("📌 [치트키 2] IR 투자 유치 / 투자자 미팅 팩트시트 튜닝", h2_style))
    p2 = (
        "[역할] 너는 벤처캐피탈(VC) 수석 심사역이자 스타트업 IR 전문가야.\n"
        "[지시] 아래 사업계획서를 투자자가 1분 만에 설득될 수 있도록 세련되고 임팩트 있는 IR 팩트시트 문체로 재구성해 줘.\n"
        "[강조 항목] 시장 규모(TAM-SAM-SOM), 100% 무자본 ROI 모델, 3단계 스케일업 타임라인\n"
        "[제출 원고]\n[고객 사업계획서 텍스트 붙여넣기]"
    )
    story.append(make_box(p2, prompt_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("📌 [치트키 3] 소상공인 정책자금 / 은행 대출 승인용 튜닝", h2_style))
    p3 = (
        "[역할] 너는 소상공인 정책자금 및 금융기관 대출 심사 전문가야.\n"
        "[지시] 아래 원고를 원리금 상환 능력과 안정적인 월 고정 매출 창출 능력이 돋보이도록 재무 안정성 중심으로 다듬어 줘.\n"
        "[제출 원고]\n[고객 사업계획서 텍스트 붙여넣기]"
    )
    story.append(make_box(p3, prompt_style))

    story.append(Spacer(1, 10))

    # Section 3: Customer Service Messages
    story.append(Paragraph("3. 고객 만족도 200% 정중 응대 메시지 템플릿", h1_style))
    story.append(Paragraph("고객에게 챗GPT 튜닝 결과물을 전달할 때 크몽 대화창에 발송하는 템플릿입니다.", body_style))

    cs_text = (
        "안녕하세요, 대표님! [Antigravity AI 전문 컨설팅]입니다. 😊\n\n"
        "신청해 주신 PREMIUM 1:1 맞춤 튜닝 작업이 완료되어 보고서 최종본을 전달드립니다.\n\n"
        "📌 [금회 1:1 맞춤 튜닝 주요 보완사항]\n"
        "1. 정부지원사업 / IR 심사 기준에 맞춘 구체적 시장 수치(TAM-SAM-SOM) 보강\n"
        "2. 경쟁사 대비 압도적 우위를 점하는 독점적 차별화(USP) 포인트 명확화\n"
        "3. 재무 추정 및 Phase 1~3 실행 로드맵 타임라인 구체화\n\n"
        "첨부해 드린 최종 보고서 원고를 검토해 보시고, 혹시 추가로 수정하고 싶은 부분이 계시다면 편하게 말씀해 주세요! 대표님의 사업 성공을 진심으로 응원합니다. 감사합니다! 🙏"
    )
    story.append(make_box(cs_text, prompt_style, bg_color="#f0fdf4", border_color="#10b981"))

    story.append(Spacer(1, 10))

    # Section 4: Emergency Quick Fixes
    story.append(Paragraph("4. 자주 발생하는 추가 수정 요청 3초 응급처치 3선", h1_style))
    
    fixes_data = [
        [
            Paragraph("<b>수정 요청 상황</b>", h2_style),
            Paragraph("<b>3초 응급처치 프롬프트</b>", h2_style)
        ],
        [
            Paragraph("<b>\"숫자나 데이터가 부족해요\"</b>", body_style),
            Paragraph("<code>[지시] 위 보고서에 2026년 기준 실증 시장 조사 수치와 통계 자료 3가지를 구체적으로 추가해 줘.</code>", body_style)
        ],
        [
            Paragraph("<b>\"경쟁사 차별점을 더 강조해 줘요\"</b>", body_style),
            Paragraph("<code>[지시] 기존 대행사 대비 제작 비용 1/150 절감 및 3분 완결 차별화 비교표를 더 세게 강조해 줘.</code>", body_style)
        ],
        [
            Paragraph("<b>\"예산집행 내역을 구체화해 줘요\"</b>", body_style),
            Paragraph("<code>[지시] 목표 예산 범위 안에서 인프라, 마케팅, 예비비 비중을 백분율(%)로 표 작성해 줘.</code>", body_style)
        ]
    ]
    fixes_table = Table(fixes_data, colWidths=[160, 360])
    fixes_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(fixes_table)

    story.append(Spacer(1, 10))
    story.append(Paragraph("<i>(C) 2026 고고플렉스AI 연구소 All Rights Reserved.</i>", subtitle_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Local PDF build complete: {LOCAL_PDF_PATH}")

    # Copy to Desktop
    shutil.copy(LOCAL_PDF_PATH, DESKTOP_PDF_PATH)
    print(f"Desktop PDF copied successfully: {DESKTOP_PDF_PATH}")

if __name__ == "__main__":
    generate_pdf()
