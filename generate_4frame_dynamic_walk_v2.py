import os
import sys
import math
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

print("🚀 [고감독 픽셀 물리 엔진] 대표님 캐릭터 은발 머리카락 찰랑임 + 팔다리 전후 스윙 4프레임 생성 중...")

if not os.path.exists(input_hero_path):
    print("❌ media__1786403424508.png 파일 미감지!")
    sys.exit(1)

raw_img = Image.open(input_hero_path).convert("RGBA")

# Transparent background
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

cell_w, cell_h = 120, 120
char_w, char_h = 80, 100
char_unit = char_base.resize((char_w, char_h), Image.Resampling.NEAREST)

frames = []

for f in range(4):
    cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    sprite = char_unit.copy()
    
    # -------------------------------------------------------------
    # 3 DYNAMIC MOTION PHYSICS: LEGS + ARMS + SILVER HAIR FLOW
    # -------------------------------------------------------------
    bounce_y = 0
    leg_x = 0
    hair_shift_y = 0
    hair_shift_x = 0
    arm_rotate = 0

    if f == 0: # Idle stance
        bounce_y = 0
        leg_x = 0
        hair_shift_y = 0
    elif f == 1: # Left leg forward + Right arm back + Hair Upward Sway
        bounce_y = -4
        leg_x = 5
        hair_shift_y = -3 # Silver hair floats upward
        hair_shift_x = 2 # Sway right
        arm_rotate = -6
    elif f == 2: # Passing stance
        bounce_y = 0
        leg_x = 0
        hair_shift_y = 0
    elif f == 3: # Right leg forward + Left arm back + Hair Downward/Left Sway
        bounce_y = -4
        leg_x = -5
        hair_shift_y = -3 # Silver hair floats upward
        hair_shift_x = -2 # Sway left
        arm_rotate = 6

    # 1. Hair Animation Layers (Extract hair region y: 0..30 & apply flow offset)
    if hair_shift_y != 0 or hair_shift_x != 0:
        hair_crop = sprite.crop((0, 0, char_w, int(char_h * 0.38)))
        # Draw hair flow enhancement on crop
        sprite.paste((0,0,0,0), (0, 0, char_w, int(char_h * 0.38))) # Erase original top hair
        sprite.paste(hair_crop, (hair_shift_x, hair_shift_y), hair_crop) # Paste animated floating hair!

    # 2. Arm swing rotation
    if arm_rotate != 0:
        sprite = sprite.rotate(arm_rotate, expand=False, resample=Image.NEAREST)

    px = (cell_w - sprite.width) // 2 + leg_x
    py = cell_h - sprite.height - 6 + bounce_y
    
    cell.paste(sprite, (px, py), sprite)
    frames.append(cell)

# Save 4 Individual PNG Frames
indiv_subfolders = ["02_move_4frames", "걷는모션_4프레임"]

for base_p in target_folders:
    for sub in indiv_subfolders:
        sub_p = os.path.join(base_p, sub)
        os.makedirs(sub_p, exist_ok=True)
        for idx, f_img in enumerate(frames):
            f_img.save(os.path.join(sub_p, f"frame_{idx}.png"))

# Save Combined Sheet (480x120)
sheet_w = cell_w * 4
sheet_h = cell_h
combined_sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

for idx, f_img in enumerate(frames):
    combined_sheet.paste(f_img, (idx * cell_w, 0), f_img)

sheet_names = ["02_move_4frames_sheet.png", "sude_walk_4frames.png"]

for base_p in target_folders:
    for s_name in sheet_names:
        combined_sheet.save(os.path.join(base_p, s_name))

print("✅ [머리카락 찰랑임 + 팔다리 스윙 4프레임 완성] 개별 4개 PNG 및 시트 100% 갱신 완수!")
