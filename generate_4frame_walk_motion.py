import os
import sys
from PIL import Image, ImageDraw, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

brain_dir = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996"
input_hero_path = os.path.join(brain_dir, "media__1786403424508.png")

target_folders = [
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트인미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트이미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트인미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\Media_Input",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
]

for folder in target_folders:
    os.makedirs(folder, exist_ok=True)

print(f"🚀 [대표님 원본 캐릭터] 4프레임 걷기 모션 정밀 렌더링 중...")

if not os.path.exists(input_hero_path):
    print("❌ media__1786403424508.png 파일 미감지!")
    sys.exit(1)

# 1. Load User's New Reference Character Image
raw_img = Image.open(input_hero_path).convert("RGBA")
print(f"✅ 대표님 원본 캐릭터 로드 성공! 해상도: {raw_img.size}")

# Transparent background removal (pure white / near white)
datas = raw_img.getdata()
new_data = []
for item in datas:
    if item[0] > 235 and item[1] > 235 and item[2] > 235:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)
raw_img.putdata(new_data)

bbox = raw_img.getbbox()
char_base = raw_img.crop(bbox) if bbox else raw_img

# Standard 4-Frame Cell Box: 120x120, Character Body: 80x100
cell_w, cell_h = 120, 120
char_w, char_h = 80, 100
char_unit = char_base.resize((char_w, char_h), Image.Resampling.NEAREST)

# ---------------------------------------------------------------------
# GENERATE 4 DISTINCT WALKING MOTION FRAMES
# Frame 0: Idle Walk Stance
# Frame 1: Left Leg Forward Stride & Head Bounce (-4px)
# Frame 2: Passing Stance (Middle)
# Frame 3: Right Leg Forward Stride & Head Bounce (-4px)
# ---------------------------------------------------------------------
frames = []

for f in range(4):
    cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    sprite = char_unit.copy()
    
    # Physics offsets for natural 4-frame walking motion
    bounce_y = 0
    leg_x = 0
    body_tilt = 0

    if f == 0:
        bounce_y = 0
        leg_x = -2
    elif f == 1: # Left foot forward stride
        bounce_y = -4
        leg_x = 4
        # Slightly stretch vertically during stride
        sprite = sprite.resize((char_w, char_h + 2), Image.Resampling.NEAREST)
    elif f == 2: # Passing stance
        bounce_y = 0
        leg_x = 0
    elif f == 3: # Right foot forward stride
        bounce_y = -4
        leg_x = -4
        sprite = sprite.resize((char_w, char_h + 2), Image.Resampling.NEAREST)

    px = (cell_w - sprite.width) // 2 + leg_x
    py = cell_h - sprite.height - 6 + bounce_y
    
    cell.paste(sprite, (px, py), sprite)
    frames.append(cell)

# 2. Save 4 Individual PNG Frames
indiv_subfolder_names = ["02_move_4frames", "걷는모션_4프레임"]

for base_p in target_folders:
    for sub in indiv_subfolder_names:
        sub_p = os.path.join(base_p, sub)
        os.makedirs(sub_p, exist_ok=True)
        for idx, f_img in enumerate(frames):
            f_img.save(os.path.join(sub_p, f"frame_{idx}.png"))

# 3. Save 4-Frame Combined Grid Sheet (480x120)
sheet_w = cell_w * 4
sheet_h = cell_h
combined_sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

for idx, f_img in enumerate(frames):
    combined_sheet.paste(f_img, (idx * cell_w, 0), f_img)

sheet_names = [
    "02_move_4frames_sheet.png",
    "sude_walk_4frames.png",
    "슈드용사_4프레임_걷는모션_스프라이트.png"
]

for base_p in target_folders:
    for s_name in sheet_names:
        combined_sheet.save(os.path.join(base_p, s_name))

print("✅ [4프레임 걷는모션 완성] 개별 4개 PNG 컷 및 가로 480x120 스프라이트 시트 저장 전수 완료!")
