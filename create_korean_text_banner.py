import os
from PIL import Image, ImageDraw, ImageFont

bg_path = r"C:\Users\sude3\.gemini\antigravity-ide\brain\1de0288c-41aa-4fd5-8743-69643a6a7058\ai_report_saas_thumbnail_1to1_1786001184590.png"
output_thumb = r"C:\Users\sude3\.gemini\antigravity-ide\brain\1de0288c-41aa-4fd5-8743-69643a6a7058\ai_report_korean_thumb.png"
output_detail = r"C:\Users\sude3\.gemini\antigravity-ide\brain\1de0288c-41aa-4fd5-8743-69643a6a7058\ai_report_korean_detail.png"

# Load background
img = Image.open(bg_path).convert("RGBA")
width, height = img.size

# Fonts
font_path_bold = r"C:\Windows\Fonts\malgunbd.ttf"
font_path = r"C:\Windows\Fonts\malgun.ttf"

font_title = ImageFont.truetype(font_path_bold, 54)
font_sub = ImageFont.truetype(font_path_bold, 36)
font_badge = ImageFont.truetype(font_path_bold, 28)
font_body = ImageFont.truetype(font_path, 26)

# Create overlay layer
overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Dark gradient bar at top
draw.rectangle([(0, 0), (width, 240)], fill=(15, 23, 42, 230))
# Accent bar
draw.rectangle([(0, 235), (width, 240)], fill=(99, 102, 241, 255))

# Top Badge
draw.rounded_rectangle([(40, 25), (420, 75)], radius=20, fill=(239, 68, 68, 255))
draw.text((60, 35), "🔥 3분 완성 AI 사업계획서", font=font_badge, fill=(255, 255, 255, 255))

# Main Title Text
draw.text((40, 90), "AI 사업계획서 & 보고서 자동 생성기", font=font_title, fill=(255, 255, 255, 255))
draw.text((40, 165), "정부지원사업 제출용 • IR 투자유치용 • 시장분석 100% 대응", font=font_sub, fill=(165, 180, 252, 255))

# Bottom Info Overlay Bar
draw.rectangle([(0, height - 160), (width, height)], fill=(15, 23, 42, 235))
draw.rectangle([(0, height - 160), (width, height - 155)], fill=(16, 185, 129, 255))

draw.text((40, height - 130), "⚡ 9,900원 초저가 3분 완결  |  월 무제한 PRO 29,900원", font=font_sub, fill=(52, 211, 153, 255))
draw.text((40, height - 75), "✓ 실시간 웹 미리보기  ✓ .MD 마크다운 다운로드  ✓ 🖨️ PDF / 인쇄 출력", font=font_body, fill=(226, 232, 240, 255))

# Composite and save
final_thumb = Image.alpha_composite(img, overlay)
final_thumb.convert("RGB").save(output_thumb, "PNG")

# Also copy to static and desktop
static_dst = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static\ai_report_korean_thumb.png"
desktop_dst = r"C:\Users\sude3\OneDrive\바탕 화면\크몽_AI사업계획서_한글_대표썸네일.png"

os.makedirs(r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\static", exist_ok=True)
final_thumb.convert("RGB").save(static_dst, "PNG")
final_thumb.convert("RGB").save(desktop_dst, "PNG")

print("Korean sharp thumbnail generated successfully!")
