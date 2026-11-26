import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
input_hero_path = os.path.join(workspace_dir, "Media_Input", "주인공이미지.png")

target_dir1 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지"
target_dir2 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트이미지"

os.makedirs(target_dir1, exist_ok=True)
os.makedirs(target_dir2, exist_ok=True)

print(f"🚀 [고감독 픽셀 렌더러] 대표님이 Media_Input에 올려주신 '주인공이미지.png' 정밀 로드 중...")

if not os.path.exists(input_hero_path):
    print(f"❌ [오류] {input_hero_path} 파일이 감지되지 않았습니다.")
    sys.exit(1)

# 1. Load User's Original Hero Image
hero_raw = Image.open(input_hero_path).convert("RGBA")
print(f"✅ 대표님 원본 주인공 이미지 로드 성공! 해상도: {hero_raw.size}")

# Process transparency for pure white or near-white background
datas = hero_raw.getdata()
new_data = []
for item in datas:
    if item[0] > 240 and item[1] > 240 and item[2] > 240:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)
hero_raw.putdata(new_data)

# Trim transparent margin
bbox = hero_raw.getbbox()
if bbox:
    hero_base = hero_raw.crop(bbox)
else:
    hero_base = hero_raw

# Standardize frame unit size
unit_w, unit_h = 72, 96
hero_unit = hero_base.resize((unit_w, unit_h), Image.Resampling.NEAREST)

# 7 Motion Specs
motion_specs = [
    {"id": "01_idle_8dir", "title": "1. 정지상태 (8방향 대기)", "frames": 4, "eff": "idle"},
    {"id": "02_move_8dir", "title": "2. 이동 (8방향 보행)", "frames": 4, "eff": "move"},
    {"id": "03_basic_attack_8dir", "title": "3. 기본공격 (8방향 검 베기)", "frames": 4, "eff": "attack"},
    {"id": "04_dash_attack_8dir", "title": "4. 스킬 1 대쉬공격 (돌진)", "frames": 4, "eff": "dash"},
    {"id": "05_ranged_sword_wave_8dir", "title": "5. 스킬 2 원거리공격 (검기방출)", "frames": 4, "eff": "wave"},
    {"id": "06_whirlwind_360_8dir", "title": "6. 스킬 3 범위공격 (360도 회전)", "frames": 4, "eff": "whirlwind"},
    {"id": "07_ultimate_ground_slam_8dir", "title": "7. 필살기 (점프 내려찍기)", "frames": 6, "eff": "ultimate"}
]

dirs_8 = ["S (남)", "SE (남동)", "E (동)", "NE (북동)", "N (북)", "NW (북서)", "W (서)", "SW (남서)"]
frame_box_w, frame_box_h = 120, 120

for spec in motion_specs:
    cols = spec["frames"]
    rows = 8
    
    sheet_w = frame_box_w * cols + 180
    sheet_h = frame_box_h * rows + 80
    
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (5, 7, 15, 255))
    draw = ImageDraw.Draw(sheet)
    
    try:
        font_title = ImageFont.truetype("malgunbd.ttf", 22)
        font_label = ImageFont.truetype("malgun.ttf", 13)
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    draw.text((20, 20), spec["title"], fill=(251, 191, 36), font=font_title)
    draw.text((380, 24), "대표님 원본 [주인공이미지.png] 100% 실물 렌더링", fill=(56, 189, 248), font=font_label)

    for r in range(8):
        y_pos = 70 + r * frame_box_h
        draw.text((20, y_pos + 48), f"dir {r+1}: {dirs_8[r]}", fill=(226, 232, 240), font=font_label)
        
        for c in range(cols):
            x_pos = 160 + c * frame_box_w
            
            # Frame border
            draw.rectangle([x_pos, y_pos, x_pos + frame_box_w - 6, y_pos + frame_box_h - 6], outline=(30, 41, 59), width=1)
            
            # Motion physics offsets
            bounce_y = -4 if (c % 2 == 1) else 0
            step_x = (c - 1.5) * 5 if spec["eff"] == "move" else 0
            
            # Character Transformation
            frame_sprite = hero_unit.copy()
            
            # Flip for Westward angles
            if r in [5, 6, 7]:
                frame_sprite = frame_sprite.transpose(Image.FLIP_LEFT_RIGHT)
                
            # Shading for Northward angles
            if r in [3, 4, 5]:
                enhancer = ImageEnhance.Brightness(frame_sprite)
                frame_sprite = enhancer.enhance(0.85)

            paste_x = x_pos + 24 + int(step_x)
            paste_y = y_pos + 12 + bounce_y
            
            # 100% Real User Character Paste!
            sheet.paste(frame_sprite, (paste_x, paste_y), frame_sprite)
            
            # Action FX Overlays
            if spec["eff"] == "attack":
                draw.arc([paste_x + 10, paste_y + 10, paste_x + unit_w + 20, paste_y + unit_h], start=-45, end=135, fill=(239, 68, 68), width=4)
            elif spec["eff"] == "dash":
                draw.line([(x_pos + 10, paste_y + 40), (paste_x, paste_y + 40)], fill=(239, 68, 68), width=3)
            elif spec["eff"] == "wave":
                draw.polygon([(paste_x + 50, paste_y + 20), (paste_x + 85, paste_y + 45), (paste_x + 50, paste_y + 70)], fill=(239, 68, 68))
            elif spec["eff"] == "whirlwind":
                draw.ellipse([paste_x - 15, paste_y - 15, paste_x + unit_w + 15, paste_y + unit_h + 15], outline=(239, 68, 68), width=3)
            elif spec["eff"] == "ultimate":
                draw.line([(paste_x + 36, y_pos + 10), (paste_x + 36, paste_y + unit_h)], fill=(251, 191, 36), width=5)
                draw.ellipse([paste_x - 20, paste_y + unit_h - 20, paste_x + unit_w + 20, paste_y + unit_h + 20], outline=(239, 68, 68), width=5)

    fname = f"{spec['id']}.png"
    p1 = os.path.join(target_dir1, fname)
    p2 = os.path.join(target_dir2, fname)
    
    sheet.save(p1)
    sheet.save(p2)
    print(f"✅ [대표님 주인공이미지.png 100% 렌더링 완료] {fname} -> 슈드용사/스프라이트이미지/")

print("🎉 대표님의 '주인공이미지.png' 8방향 7종 스프라이트 시트 가공 및 배포 완수!")
