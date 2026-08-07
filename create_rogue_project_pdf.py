import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak, Table, TableStyle
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 파일 경로 설정
OUTPUT_DIR = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\고대표"
PDF_PATH = os.path.join(OUTPUT_DIR, "로그프로젝트_5대_전략_로드맵_보고서.pdf")

os.makedirs(OUTPUT_DIR, exist_ok=True)

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
                self.drawRightString(200 * 2.83, 280 * 2.83, "로그 프로젝트 월 1,000만원 달성 5대 전략 로드맵 보고서")
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(15 * 2.83, 278 * 2.83, 200 * 2.83, 278 * 2.83)
                
                page_text = f"- {self._pageNumber} / {num_pages} -"
                self.drawCentredString(105 * 2.83, 12 * 2.83, page_text)
                self.restoreState()
            super().showPage()
        super().save()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Malgun-Bold',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        alignment=1, # Center
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Malgun',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#0EA5E9'),
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Malgun-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Malgun',
        fontSize=9.5,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'Body_Bold_Custom',
        parent=styles['Normal'],
        fontName='Malgun-Bold',
        fontSize=9.5,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Malgun-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Malgun',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Malgun-Bold',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor('#0F172A')
    )

    elements = []

    # Title & Subtitle
    elements.append(Paragraph("🚀 [로그 프로젝트] 월 1,000만원 달성<br/>5대 전략 로드맵 & 무인 구축 보고서", title_style))
    elements.append(Paragraph("<b>수신</b>: 대표님 (CEO) &nbsp;|&nbsp; <b>발신</b>: 고감독 (총괄 디렉터) &nbsp;|&nbsp; <b>일시</b>: 2026. 08. 08", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0EA5E9'), spaceBefore=0, spaceAfter=15))

    # Section 1
    elements.append(Paragraph("🎯 1. 프로젝트 핵심 개요 및 목표", h1_style))
    elements.append(Paragraph("• <b>프로젝트명</b>: 로그 (Rogue) 모바일 게임 & 무인 자동화 프로젝트", body_style))
    elements.append(Paragraph("• <b>최종 수익 목표</b>: <b>월 1,000만원 이상 무인 자동화 지속 매출 창출</b>", body_style))
    elements.append(Paragraph("• <b>1차 런칭 목표</b>: 7일 단기 개발 완성 후 앱스토어/구글스토어 정식 출시 및 초기 500만원 매출 달성", body_style))
    elements.append(Paragraph("• <b>핵심 정체성</b>: 모바일 로그라이크(Roguelike) 게임 기반 무인 마케팅 및 자동 결제 파이프라인 구축", body_style))
    elements.append(Spacer(1, 10))

    # Section 2
    elements.append(Paragraph("🗺️ 2. 월 1,000만원 달성을 위한 5가지 시나리오별 전략 로드맵", h1_style))
    elements.append(Paragraph("아래 5가지 전략 시안 중 최적의 모델을 선택하여 무인 자동화 가동을 추진합니다.", body_style))
    elements.append(Spacer(1, 6))

    # Table 1: 5 Roadmaps
    table_data = [
        [
            Paragraph("구분", table_header_style),
            Paragraph("전략 모델", table_header_style),
            Paragraph("핵심 수익 구조", table_header_style),
            Paragraph("개발 기간", table_header_style),
            Paragraph("목표 월 매출", table_header_style)
        ],
        [
            Paragraph("시안 1", table_cell_bold),
            Paragraph("하이퍼캐주얼 IAP 직공략형", table_cell_bold),
            Paragraph("부활권($0.99), 무기 상자($2.99), 오프라인 루팅 패스($4.99) 직결제", table_cell_style),
            Paragraph("7일 (초단기)", table_cell_style),
            Paragraph("월 1,000만원", table_cell_bold)
        ],
        [
            Paragraph("시안 2", table_cell_bold),
            Paragraph("보상형 광고 + 미니 구독형", table_cell_bold),
            Paragraph("AdMob 30초 보상형 광고 시청 + 광고 제거 패스($4.99/월 구독)", table_cell_style),
            Paragraph("10일", table_cell_style),
            Paragraph("월 1,200만원", table_cell_bold)
        ],
        [
            Paragraph("시안 3", table_cell_bold),
            Paragraph("$49 SaaS 번들 패키지 결합형", table_cell_bold),
            Paragraph("게임 유저 ➡️ AI 자동화 템플릿 번들($49) 타깃 전환 판매", table_cell_style),
            Paragraph("7일", table_cell_style),
            Paragraph("월 1,500만원", table_cell_bold)
        ],
        [
            Paragraph("시안 4", table_cell_bold),
            Paragraph("유튜브/SNS 바이럴 팬덤형", table_cell_bold),
            Paragraph("레오 채널 숏폼 알고리즘 $0원 유입 ➡️ 스토어 직다운로드", table_cell_style),
            Paragraph("14일", table_cell_style),
            Paragraph("월 1,000만원", table_cell_bold)
        ],
        [
            Paragraph("시안 5 (추천)", table_cell_bold),
            Paragraph("AI 자율 무인 운영 확장형", table_cell_bold),
            Paragraph("Connect AI 10인 팀 24시간 무인 마케팅 + IAP + SaaS 자동 연동", table_cell_style),
            Paragraph("7일 (최고추천)", table_cell_style),
            Paragraph("월 1,800만원", table_cell_bold)
        ]
    ]

    col_widths = [45, 110, 210, 65, 80]
    t1 = Table(table_data, colWidths=col_widths)
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 15))

    # Section 3
    elements.append(Paragraph("🛠️ 3. 기술 인프라 및 에이전트 R&R 분담표", h1_style))
    
    t2_data = [
        [Paragraph("담당 에이전트", table_header_style), Paragraph("핵심 담당 업무 및 개발 사양", table_header_style)],
        [Paragraph("💻 고감독 & 코다리", table_cell_bold), Paragraph("• 모바일 로그라이크 게임 렌더링 스켈레톤 구축<br/>• Apple App Store & Google Play In-App Purchase (IAP) 연동<br/>• PayPal API 샌드박스 연동 및 결제 수집 시스템 구축", table_cell_style)],
        [Paragraph("🔍 Researcher", table_cell_bold), Paragraph("• 로그라이크 상위 5개 경쟁작 벤치마킹 분석<br/>• 유저 페인포인트 및 핵심 게임 후크(Hook) 데이터 도출", table_cell_style)],
        [Paragraph("✍️ Writer & 🎨 Designer", table_cell_bold), Paragraph("• 게임 스토리라인, 아이템 설명 카피라이팅<br/>• 스토어 썸네일, 게임 배너, 홍보 시각자료 제작", table_cell_style)],
        [Paragraph("📱 영숙 (Secretary)", table_cell_bold), Paragraph("• 앱스토어/구글스토어 심사 제출 일정 관리 및 데일리 브리핑", table_cell_style)]
    ]
    t2 = Table(t2_data, colWidths=[120, 390])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0EA5E9')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 15))

    # Section 4
    elements.append(Paragraph("📅 4. 7일 단기 개발 & 정식 런칭 일정표", h1_style))
    
    t3_data = [
        [Paragraph("일자", table_header_style), Paragraph("주요 작업 내용", table_header_style), Paragraph("책임 담당자", table_header_style)],
        [Paragraph("Day 1", table_cell_bold), Paragraph("로그라이크 핵심 메커니즘 & 레벨 디자인 확정", table_cell_style), Paragraph("고감독, 현빈", table_cell_style)],
        [Paragraph("Day 2", table_cell_bold), Paragraph("게임 코드 스켈레톤 및 UI/UX 핵심 모듈 완성", table_cell_style), Paragraph("코다리, 고감독", table_cell_style)],
        [Paragraph("Day 3", table_cell_bold), Paragraph("리소스 아트, 사운드, 썸네일/배너 제작", table_cell_style), Paragraph("디자이너, 에디터", table_cell_style)],
        [Paragraph("Day 4", table_cell_bold), Paragraph("결제 API (IAP/PayPal) 연동 및 테스트 빌드 검증", table_cell_style), Paragraph("코다리, 고감독", table_cell_style)],
        [Paragraph("Day 5", table_cell_bold), Paragraph("유튜브 숏폼 홍보 영상 및 마케팅 카피라이팅 완성", table_cell_style), Paragraph("레오, Writer", table_cell_style)],
        [Paragraph("Day 6", table_cell_bold), Paragraph("Apple App Store & Google Play Console 심사 제출", table_cell_style), Paragraph("고감독, 영숙", table_cell_style)],
        [Paragraph("Day 7", table_cell_bold), Paragraph("정식 런칭 & 무인 자동 마케팅/결제 파이프라인 가동", table_cell_style), Paragraph("전 에이전트", table_cell_style)]
    ]
    t3 = Table(t3_data, colWidths=[60, 350, 100])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t3)
    elements.append(Spacer(1, 15))

    # Conclusion
    elements.append(Paragraph("📌 5. 총괄 디렉터 고감독의 한마디", h1_style))
    elements.append(Paragraph("대표님! 본 5대 전략 로드맵 보고서는 대표님의 <b>'고대표'</b> 폴더에 마크다운(.md) 및 PDF(.pdf) 두 가지 형식으로 동시에 전달 완료되었습니다. 대표님께서 시안 하나를 선택해주시면, 고감독 지휘 하에 즉시 1일차 개발을 집행하겠습니다! 💖", body_style))

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"✅ PDF 생성 완료: {PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
