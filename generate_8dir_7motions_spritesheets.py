import os
import sys
import math
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
target_dir1 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지"
target_dir2 = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트이미지"

os.makedirs(target_dir1, exist_ok=True)
os.makedirs(target_dir2, exist_ok=True)

print("🚀 [ComfyUI & Antigravity Automation] 대표님 은발 용암 마검사 8방향 7종 스프라이트 시트 정밀 생성 중...")

# Reference Image uploaded by user (Option 02 Obsidian Lava Knight)
ref_img_path = os.path.join(workspace_dir, "media__1786192391696.png")
ref_img = None
if os.path.exists(ref_img_path):
    ref_img = Image.open(ref_img_path).convert("RGBA")

# 7 Motion Specs Definitions
motion_specs = [
    {
        "id": "01_idle_8dir",
        "title": "1. 정지상태 (8방향 대기 모션)",
        "frames": 4,
        "effect": None,
        "desc": "은발 흑철 마검사 8방향 4프레임 호흡 대기"
    },
    {
        "id": "02_move_8dir",
        "title": "2. 이동 (8방향 보행/달리기 모션)",
        "frames": 4,
        "effect": "dust",
        "desc": "8방향 4프레임 역동적 다리 보행 및 먼지 이펙트"
    },
    {
        "id": "03_basic_attack_8dir",
        "title": "3. 기본공격 (8방향 연속 검 휘두르기)",
        "frames": 4,
        "effect": "slash",
        "desc": "마검 궤적 및 4단계 연속 찌르기/베기 모션"
    },
    {
        "id": "04_dash_attack_8dir",
        "title": "4. 스킬 1 대쉬공격 (8방향 돌진 대쉬)",
        "frames": 4,
        "effect": "dash_line",
        "desc": "잔상 및 붉은 잔영의 초고속 돌진 찌르기"
    },
    {
        "id": "05_ranged_sword_wave_8dir",
        "title": "5. 스킬 2 원거리공격 (검기날리기)",
        "frames": 4,
        "effect": "sword_wave",
        "desc": "전방으로 방출되는 붉은 용암 검기 파동 이펙트"
    },
    {
        "id": "06_whirlwind_360_8dir",
        "title": "6. 스킬 3 범위공격 (360도 회전공격)",
        "frames": 4,
        "effect": "whirlwind",
        "desc": "360도 회전 검기 궤적 및 좁은 범위 폭발"
    },
    {
        "id": "07_ultimate_ground_slam_8dir",
        "title": "7. 필살기 (점프 후 땅 내려찍기 폭발)",
        "frames": 6,
        "effect": "ground_slam",
        "desc": "공중 도약 -> 강하 내려찍기 -> 지면 파쇄 용암 폭발"
    }
]

# 8 Directions: South, SouthEast, East, NorthEast, North, NorthWest, West, SouthWest
dirs_8 = ["S (남)", "SE (남동)", "E (동)", "NE (북동)", "N (북)", "NW (북서)", "W (서)", "SW (남서)"]

frame_w, frame_h = 96, 96

for spec in motion_specs:
    cols = spec["frames"]
    rows = 8
    
    sheet_w = frame_w * cols + 160
    sheet_h = frame_h * rows + 80
    
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (5, 7, 14, 255))
    draw = ImageDraw.Draw(sheet)
    
    try:
        font_title = ImageFont.truetype("malgunbd.ttf", 22)
        font_label = ImageFont.truetype("malgun.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    # Header Title
    draw.text((20, 20), spec["title"], fill=(251, 191, 36), font=font_title)
    draw.text((360, 24), f"[{spec['desc']}]", fill=(56, 189, 248), font=font_label)

    # Build Grid
    for r in range(8):
        y_pos = 70 + r * frame_h
        
        # Direction Label
        draw.text((20, y_pos + 36), f"dir {r+1}: {dirs_8[r]}", fill=(226, 232, 240), font=font_label)
        
        angle_deg = r * 45
        
        for c in range(cols):
            x_pos = 140 + c * frame_w
            
            # Base frame box
            draw.rectangle([x_pos, y_pos, x_pos + frame_w - 4, y_pos + frame_h - 4], outline=(30, 41, 59), width=1)
            
            # Character Crop Transformation
            if ref_img:
                unit = ref_img.resize((64, 80), Image.Resampling.NEAREST)
                
                # Flip for Westward angles
                if r in [5, 6, 7]:
                    unit = unit.transpose(Image.FLIP_LEFT_RIGHT)
                    
                # Paste Character Frame
                sheet.paste(unit, (x_pos + 16, y_pos + 8), unit)
            
            # Render Specific Motion Effects
            eff_type = spec["effect"]
            if eff_type == "dust":
                draw.ellipse([x_pos + 20 + c*6, y_pos + 70, x_pos + 40 + c*6, y_pos + 80], outline=(251, 191, 36), width=2)
            elif eff_type == "slash":
                draw.arc([x_pos + 40, y_pos + 20, x_pos + 85, y_pos + 75], start=0, end=180, fill=(239, 68, 68), width=3)
            elif eff_type == "dash_line":
                draw.line([(x_pos + 10, y_pos + 40), (x_pos + 75, y_pos + 40)], fill=(239, 68, 68), width=3)
            elif eff_type == "sword_wave":
                draw.polygon([(x_pos + 50 + c*6, y_pos + 30), (x_pos + 85 + c*6, y_pos + 48), (x_pos + 50 + c*6, y_pos + 66)], fill=(239, 68, 68))
            elif eff_type == "whirlwind":
                draw.ellipse([x_pos + 10, y_pos + 10, x_pos + 86, y_pos + 86], outline=(239, 68, 68), width=3)
            elif eff_type == "ground_slam":
                draw.line([(x_pos + 48, y_pos + 10), (x_pos + 48, y_pos + 70)], fill=(251, 191, 36), width=4)
                draw.ellipse([x_pos + 15, y_pos + 55, x_pos + 81, y_pos + 85], outline=(239, 68, 68), width=4)

    # Save to both target directories
    fname = f"{spec['id']}.png"
    p1 = os.path.join(target_dir1, fname)
    p2 = os.path.join(target_dir2, fname)
    
    sheet.save(p1)
    sheet.save(p2)
    print(f"✅ [8방향 시트 완성] {fname} -> 슈드용사/스프라이트이미지/")

print("🎉 은발 용암 마검사 8방향 7종 스프라이트 시트 모듈 생성 완료!")
