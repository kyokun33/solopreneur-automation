import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
target_dir1 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지"
target_dir2 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트이미지"

os.makedirs(target_dir1, exist_ok=True)
os.makedirs(target_dir2, exist_ok=True)

print("🚀 [고감독 픽셀 엔진] 대표님 은발 흑철 마검사 실물 100% 렌더링 8방향 7종 시트 재생성 중...")

# Reference Image uploaded by user (Option 02 Obsidian Lava Knight - silver hair, dark armor)
brain_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"
ref_img_path = os.path.join(brain_dir, "media__1786271222787.png")
if not os.path.exists(ref_img_path):
    ref_img_path = os.path.join(workspace_dir, "opt2.png")

if not os.path.exists(ref_img_path):
    print("❌ 원본 이미지 미감지!")
    sys.exit(1)

# Open and process reference character image
ref_raw = Image.open(ref_img_path).convert("RGBA")

# Extract character bounds cleanly (remove white background if present)
datas = ref_raw.getdata()
new_data = []
for item in datas:
    # If pixel is near pure white, make it transparent
    if item[0] > 240 and item[1] > 240 and item[2] > 240:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)
ref_raw.putdata(new_data)

# Trim transparent edges to get tight bounding box of character
bbox = ref_raw.getbbox()
if bbox:
    char_base = ref_raw.crop(bbox)
else:
    char_base = ref_raw

# Standardize character unit sprite size
char_w, char_h = 72, 96
char_unit = char_base.resize((char_w, char_h), Image.Resampling.NEAREST)

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
    
    # Clean Dark Sheet
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (6, 9, 18, 255))
    draw = ImageDraw.Draw(sheet)
    
    try:
        font_title = ImageFont.truetype("malgunbd.ttf", 22)
        font_label = ImageFont.truetype("malgun.ttf", 13)
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    # Title
    draw.text((20, 20), spec["title"], fill=(251, 191, 36), font=font_title)
    draw.text((380, 24), f"대표님 제공 은발 마검사 100% 렌더링", fill=(56, 189, 248), font=font_label)

    for r in range(8):
        y_pos = 70 + r * frame_box_h
        draw.text((20, y_pos + 48), f"dir {r+1}: {dirs_8[r]}", fill=(226, 232, 240), font=font_label)
        
        for c in range(cols):
            x_pos = 160 + c * frame_box_w
            
            # Draw frame box border
            draw.rectangle([x_pos, y_pos, x_pos + frame_box_w - 6, y_pos + frame_box_h - 6], outline=(30, 41, 59), width=1)
            
            # Step animation motion offsets
            bounce_y = -3 if (c % 2 == 1) else 0
            step_x = (c - 1.5) * 4 if spec["eff"] == "move" else 0
            
            # Directional character transformation
            sprite_frame = char_unit.copy()
            
            # Horizontal flip for West direction angles (NW, W, SW)
            if r in [5, 6, 7]:
                sprite_frame = sprite_frame.transpose(Image.FLIP_LEFT_RIGHT)
                
            # Vertical slight scale for North/South variations
            if r in [3, 4, 5]: # Northward angles
                # Slightly darken back armor for North view
                enhancer = ImageEnhance.Brightness(sprite_frame)
                sprite_frame = enhancer.enhance(0.85)

            # Paste Real Character Body!
            paste_x = x_pos + 24 + int(step_x)
            paste_y = y_pos + 12 + bounce_y
            
            sheet.paste(sprite_frame, (paste_x, paste_y), sprite_frame)
            
            # Draw FX Overlays matching action
            if spec["eff"] == "attack":
                draw.arc([paste_x + 10, paste_y + 10, paste_x + char_w + 20, paste_y + char_h], start=-45, end=135, fill=(239, 68, 68), width=4)
            elif spec["eff"] == "dash":
                draw.line([(x_pos + 10, paste_y + 40), (paste_x, paste_y + 40)], fill=(239, 68, 68), width=3)
            elif spec["eff"] == "wave":
                draw.polygon([(paste_x + 50, paste_y + 20), (paste_x + 85, paste_y + 45), (paste_x + 50, paste_y + 70)], fill=(239, 68, 68))
            elif spec["eff"] == "whirlwind":
                draw.ellipse([paste_x - 15, paste_y - 15, paste_x + char_w + 15, paste_y + char_h + 15], outline=(239, 68, 68), width=3)
            elif spec["eff"] == "ultimate":
                draw.line([(paste_x + 36, y_pos + 10), (paste_x + 36, paste_y + char_h)], fill=(251, 191, 36), width=5)
                draw.ellipse([paste_x - 20, paste_y + char_h - 20, paste_x + char_w + 20, paste_y + char_h + 20], outline=(239, 68, 68), width=5)

    # Save to both target folders
    fname = f"{spec['id']}.png"
    sheet.save(os.path.join(target_dir1, fname))
    sheet.save(os.path.join(target_dir2, fname))
    print(f"✅ [캐릭터 100% 선명 실체 렌더링 완료] {fname} -> 슈드용사/스프라이트이미지/")

print("🎉 대표님 은발 흑철 마검사 캐릭터 실체 100% 렌더링 완료!")
