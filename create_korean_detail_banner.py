import os
from PIL import Image, ImageDraw, ImageFont

bg_path = r"C:\Users\sude3\.gemini\antigravity-ide\brain\1de0288c-41aa-4fd5-8743-69643a6a7058\ai_report_saas_detail_banner_1786001252610.png"
output_detail = r"C:\Users\sude3\.gemini\antigravity-ide\brain\1de0288c-41aa-4fd5-8743-69643a6a7058\ai_report_korean_detail.png"

# Load background
img = Image.open(bg_path).convert("RGBA")
width, height = img.size

# Fonts
font_path_bold = r"C:\Windows\Fonts\malgunbd.ttf"
font_path = r"C:\Windows\Fonts\malgun.ttf"

font_title = ImageFont.truetype(font_path_bold, 50)
font_sub = ImageFont.truetype(font_path_bold, 32)
font_badge = ImageFont.truetype(font_path_bold, 26)
font_body = ImageFont.truetype(font_path, 24)

# Create overlay layer
overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Top Banner
draw.rectangle([(0, 0), (width, 220)], fill=(15, 23, 42, 235))
draw.rectangle([(0, 215), (width, 220)], fill=(79, 70, 229, 255))
draw.rounded_rectangle([(40, 20), (400, 65)], radius=18, fill=(239, 68, 68, 255))
draw.text((60, 28), "🚀 100% 무인 자동 생성", font=font_badge, fill=(255, 255, 255, 255))
draw.text((40, 80), "AI 사업계획서 & 보고서 3분 자동 생성기", font=font_title, fill=(255, 255, 255, 255))
draw.text((40, 150), "정부지원사업 • IR 투자유치 • 시장분석 (TAM-SAM-SOM) 완벽 대응", font=font_sub, fill=(199, 210, 254, 255))

# Bottom Banner
draw.rectangle([(0, height - 180), (width, height)], fill=(15, 23, 42, 240))
draw.rectangle([(0, height - 180), (width, height - 175)], fill=(16, 185, 129, 255))

draw.text((40, height - 150), "💡 대행사 비용 150만 원 ➔ 초저가 9,900원으로 3분 만에 해결!", font=font_sub, fill=(52, 211, 153, 255))
draw.text((40, height - 90), "✓ 입력 폼 정보 3초 자동 렌더링  ✓ .MD 마크다운 다운로드  ✓ PDF / 인쇄 출력 지원", font=font_body, fill=(226, 232, 240, 255))

# Composite and save
final_detail = Image.alpha_composite(img, overlay)
final_detail.convert("RGB").save(output_detail, "PNG")

# Also copy to static and desktop
static_dst = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static\ai_report_korean_detail.png"
desktop_dst = r"C:\Users\sude3\OneDrive\바탕 화면\크몽_AI사업계획서_한글_상세이미지.png"

os.makedirs(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static", exist_ok=True)
final_detail.convert("RGB").save(static_dst, "PNG")
final_detail.convert("RGB").save(desktop_dst, "PNG")

print("Korean sharp detail image generated successfully!")
