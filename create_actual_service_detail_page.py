import os
from PIL import Image, ImageDraw, ImageFont

# Canvas Dimension: 1000px wide x 2400px tall (Within Kmong specs: 652~2000px width, <=3000px height)
width = 1000
height = 2400

# Fonts
font_bold_path = r"C:\Windows\Fonts\malgunbd.ttf"
font_path = r"C:\Windows\Fonts\malgun.ttf"

f_hero_title = ImageFont.truetype(font_bold_path, 42)
f_hero_sub = ImageFont.truetype(font_bold_path, 24)
f_sec_title = ImageFont.truetype(font_bold_path, 32)
f_card_title = ImageFont.truetype(font_bold_path, 24)
f_body_bold = ImageFont.truetype(font_bold_path, 20)
f_body = ImageFont.truetype(font_path, 18)
f_small = ImageFont.truetype(font_path, 16)

canvas = Image.new("RGB", (width, height), (248, 250, 252)) # #f8fafc background
draw = ImageDraw.Draw(canvas)

# 1. Top Hero Header (0 ~ 400px)
draw.rectangle([(0, 0), (width, 380)], fill=(30, 27, 75)) # #1e1b4b
draw.rectangle([(0, 375), (width, 380)], fill=(99, 102, 241)) # #6366f1 accent

# Red Badge
draw.rounded_rectangle([(60, 40), (460, 85)], radius=20, fill=(239, 68, 68))
draw.text((80, 48), "🔥 대행사 비용 300만 원 ➔ 9,900원 완결", font=f_small, fill=(255, 255, 255))

# Hero Titles
draw.text((60, 110), "3분 만에 완성되는 AI 사업계획서", font=f_hero_title, fill=(255, 255, 255))
draw.text((60, 165), "& 비즈니스 리포트 자동 생성기", font=f_hero_title, fill=(165, 180, 252))
draw.text((60, 235), "정부지원사업(예비/초기창업패키지) • IR 투자유치 • 시장분석 무인 렌더링", font=f_hero_sub, fill=(226, 232, 240))

# 3 Feature Pills
draw.rounded_rectangle([(60, 290), (330, 335)], radius=10, fill=(49, 46, 129))
draw.text((80, 300), "⚡ 3분 자동 렌더링", font=f_body_bold, fill=(165, 180, 252))

draw.rounded_rectangle([(350, 290), (620, 335)], radius=10, fill=(49, 46, 129))
draw.text((370, 300), "📄 .MD & PDF 다운로드", font=f_body_bold, fill=(52, 211, 153))

draw.rounded_rectangle([(640, 290), (930, 335)], radius=10, fill=(49, 46, 129))
draw.text((660, 300), "💎 9,900원 초저가 무인 서비스", font=f_body_bold, fill=(251, 191, 36))


# 2. Section: 실제 프로그램 작동 방식 (420 ~ 950px)
draw.text((60, 420), "💻 실제 프로그램 사용 & 작동 프로세스", font=f_sec_title, fill=(15, 23, 42))

# Program UI Box Mockup
draw.rounded_rectangle([(60, 480), (940, 920)], radius=18, fill=(15, 23, 42), outline=(79, 70, 229), width=2)

# Program Top Window Bar
draw.rounded_rectangle([(60, 480), (940, 530)], radius=18, fill=(30, 41, 59))
draw.ellipse([(85, 500), (97, 512)], fill=(239, 68, 68))
draw.ellipse([(107, 500), (119, 512)], fill=(245, 158, 11))
draw.ellipse([(129, 500), (141, 512)], fill=(16, 185, 129))
draw.text((160, 497), "AI Business Report Generator SaaS - [report_generator]", font=f_small, fill=(148, 163, 184))

# Left Input Form Mockup
draw.rounded_rectangle([(80, 550), (480, 900)], radius=12, fill=(30, 41, 59))
draw.text((100, 565), "📝 프로젝트 정보 입력 폼", font=f_body_bold, fill=(165, 180, 252))

draw.text((100, 605), "• 사업 아이템명: AI 기반 리포트 생성기", font=f_small, fill=(226, 232, 240))
draw.text((100, 640), "• 리포트 목적: 🏛️ 정부지원사업 제출용", font=f_small, fill=(226, 232, 240))
draw.text((100, 675), "• 타겟 고객: 1인 기업가, 소상공인", font=f_small, fill=(226, 232, 240))
draw.text((100, 710), "• 핵심 기능: 3분 자동 PDF 렌더링", font=f_small, fill=(226, 232, 240))
draw.text((100, 745), "• 목표 예산: 초기 1,000만 원 / 월 500만 원", font=f_small, fill=(226, 232, 240))

draw.rounded_rectangle([(100, 810), (460, 865)], radius=10, fill=(79, 70, 229))
draw.text((130, 825), "✨ 사업계획서 자동 생성하기 (3초)", font=f_body_bold, fill=(255, 255, 255))

# Right Generated Report Preview Mockup
draw.rounded_rectangle([(500, 550), (920, 900)], radius=12, fill=(255, 255, 255))
draw.text((520, 565), "📄 3분 자동 완성 보고서 결과", font=f_body_bold, fill=(79, 70, 229))
draw.line([(520, 595), (900, 595)], fill=(226, 232, 240), width=1)

draw.text((520, 610), "# [사업계획서] AI 자동 리포트 생성기", font=f_small, fill=(15, 23, 42))
draw.text((520, 640), "1. 사업 개요 및 배경 (Executive Summary)", font=f_small, fill=(67, 56, 202))
draw.text((520, 670), "   - 1인기업 및 예비창업자 업무생산성 10배 향상", font=f_small, fill=(71, 85, 105))
draw.text((520, 700), "2. 타겟 시장 분석 (TAM-SAM-SOM)", font=f_small, fill=(67, 56, 202))
draw.text((520, 730), "   - TAM: 5조 원 / SAM: 5,000억 원 / SOM: 100억 원", font=f_small, fill=(71, 85, 105))
draw.text((520, 760), "3. 고투마켓 마케팅 & 수익 모델", font=f_small, fill=(67, 56, 202))
draw.text((520, 790), "   - 단건 9,900원 / 월 무제한 PRO 29,900원", font=f_small, fill=(71, 85, 105))

draw.rounded_rectangle([(520, 835), (690, 880)], radius=8, fill=(16, 185, 129))
draw.text((540, 848), "🖨️ PDF 발급", font=f_small, fill=(255, 255, 255))

draw.rounded_rectangle([(710, 835), (900, 880)], radius=8, fill=(99, 102, 241))
draw.text((730, 848), "📥 .MD 다운로드", font=f_small, fill=(255, 255, 255))


# 3. Section: 5대 핵심 생성 영역 (970 ~ 1550px)
draw.text((60, 970), "📋 5대 핵심 비즈니스 파트 자동 구성", font=f_sec_title, fill=(15, 23, 42))

sections_info = [
    ("1. 사업 개요 & 배경", "목표 시장의 가려운 곳(Pain Point)과 프로젝트 핵심 비전 자동 정돈"),
    ("2. 타겟 시장 분석 (TAM-SAM-SOM)", "전체 시장, 유효 시장, 초기 수익 시장 수치 추정 및 경쟁 우위 비교표"),
    ("3. 핵심 기술 & 서비스 스펙", "자동화 렌더링 엔진 스펙 및 시스템 입출력 아키텍처 정의"),
    ("4. 마케팅 전략 & 수익 모델", "온라인 바이럴, SEO 노출 전략 및 건당/구독형 수익 구조 설계"),
    ("5. 재무 추정 & 3단계 로드맵", "Phase 1~3 실행 타임라인 및 예산 집행 세부 항목 시뮬레이션")
]

y_pos = 1030
for title, desc in sections_info:
    draw.rounded_rectangle([(60, y_pos), (940, y_pos + 85)], radius=12, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((90, y_pos + 16), title, font=f_body_bold, fill=(79, 70, 229))
    draw.text((90, y_pos + 48), desc, font=f_body, fill=(71, 85, 105))
    y_pos += 100


# 4. Section: 기존 대행사 VS 본 툴 비교표 (1570 ~ 1900px)
draw.text((60, 1570), "📊 기존 대행사 VS AI 자동 생성기 비교", font=f_sec_title, fill=(15, 23, 42))

# Comparison Table Box
table_top = 1630
draw.rounded_rectangle([(60, table_top), (940, table_top + 230)], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Table Header
draw.rectangle([(60, table_top), (940, table_top + 50)], fill=(241, 245, 249))
draw.text((90, table_top + 14), "구분", font=f_body_bold, fill=(15, 23, 42))
draw.text((380, table_top + 14), "기존 대행사 / 외주 대필", font=f_body_bold, fill=(100, 116, 139))
draw.text((700, table_top + 14), "✨ AI 보고서 생성기", font=f_body_bold, fill=(79, 70, 229))

rows = [
    ("제작 비용", "150만 원 ~ 300만 원", "9,900원 ~ 29,900원 (초저가)"),
    ("소요 시간", "2주 ~ 4주 소요", "3분 이내 즉시 완성"),
    ("수정 & 인쇄", "수정 시 추가 비용 발생", "무제한 수정 & 즉시 PDF/MD 출력")
]

row_y = table_top + 60
for category, old_val, new_val in rows:
    draw.line([(60, row_y), (940, row_y)], fill=(226, 232, 240), width=1)
    draw.text((90, row_y + 14), category, font=f_body, fill=(15, 23, 42))
    draw.text((380, row_y + 14), old_val, font=f_body, fill=(100, 116, 139))
    draw.text((700, row_y + 14), new_val, font=f_body_bold, fill=(16, 185, 129))
    row_y += 55


# 5. Section: 합리적 가격 및 무제한 플랜 (1930 ~ 2350px)
draw.text((60, 1930), "💎 합리적인 가격 정책 (0원 위험 부담)", font=f_sec_title, fill=(15, 23, 42))

# Pricing Cards 2 columns
# Card 1: 9,900 won
draw.rounded_rectangle([(60, 1990), (480, 2300)], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
draw.text((90, 2020), "1회 생성 이용권", font=f_body_bold, fill=(79, 70, 229))
draw.text((90, 2060), "9,900원", font=f_hero_title, fill=(15, 23, 42))
draw.text((90, 2120), "• 단건 사업계획서 3분 렌더링", font=f_body, fill=(71, 85, 105))
draw.text((90, 2155), "• 실시간 웹 미리보기 제공", font=f_body, fill=(71, 85, 105))
draw.text((90, 2190), "• .MD 마크다운 파일 제공", font=f_body, fill=(71, 85, 105))
draw.text((90, 2225), "• PDF 출력 및 인쇄 기능", font=f_body, fill=(71, 85, 105))

# Card 2: 29,900 won PRO
draw.rounded_rectangle([(510, 1990), (940, 2300)], radius=16, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
draw.rounded_rectangle([(530, 2015), (640, 2045)], radius=10, fill=(79, 70, 229))
draw.text((545, 2022), "POPULAR", font=f_small, fill=(255, 255, 255))

draw.text((655, 2020), "PRO 월 무제한 구독", font=f_body_bold, fill=(67, 56, 202))
draw.text((530, 2060), "29,900원 /월", font=f_hero_title, fill=(15, 23, 42))
draw.text((530, 2120), "• 모든 템플릿 무제한 생성", font=f_body_bold, fill=(15, 23, 42))
draw.text((530, 2155), "• 정부지원/IR/시장분석 100% 대응", font=f_body, fill=(71, 85, 105))
draw.text((530, 2190), "• 우선 순위 알고리즘 적용", font=f_body, fill=(71, 85, 105))
draw.text((530, 2225), "• 평생 업데이트 지원", font=f_body, fill=(71, 85, 105))


# Save Image Output
output_png = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static\kmong_actual_service_detail_page.png"
desktop_png = r"C:\Users\sude3\OneDrive\바탕 화면\크몽_실제프로그램사용_상세페이지.png"

os.makedirs(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static", exist_ok=True)
canvas.save(output_png, "PNG")

desktop_paths = [r'C:\Users\sude3\OneDrive\바탕 화면', r'C:\Users\sude3\Desktop']
for d in desktop_paths:
    if os.path.exists(d):
        dst = os.path.join(d, '크몽_실제프로그램사용_상세페이지.png')
        canvas.save(dst, "PNG")
        print('Saved actual service detail page to desktop:', dst)
        break

print(f"Pixel-perfect Kmong detail page PNG generated successfully! (Width: {width}px, Height: {height}px)")
