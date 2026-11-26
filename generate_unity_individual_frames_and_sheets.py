import os
import sys
from PIL import Image, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
input_hero_path = os.path.join(workspace_dir, "Media_Input", "주인공이미지.png")

target_base = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지"
typo_base = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트인미지"
unity_assets_base = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트이미지"
unity_assets_typo = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트인미지"

print("🚀 [유니티 2D 전문 스프라이트 아키텍처] 개별 프레임 컷 분리 및 유니티 Grid Atlas 시트 생성 중...")

if not os.path.exists(input_hero_path):
    print("❌ 원본 주인공이미지.png 미감지!")
    sys.exit(1)

# Load User Hero Base Image
hero_raw = Image.open(input_hero_path).convert("RGBA")

datas = hero_raw.getdata()
new_data = []
for item in datas:
    if item[0] > 240 and item[1] > 240 and item[2] > 240:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)
hero_raw.putdata(new_data)

bbox = hero_raw.getbbox()
hero_base = hero_raw.crop(bbox) if bbox else hero_raw

# Standard Frame Cell Size (Unity Grid: 96x96, Character Body: 64x80)
cell_w, cell_h = 96, 96
char_w, char_h = 64, 80
base_char = hero_base.resize((char_w, char_h), Image.Resampling.NEAREST)

# 8 Directions
dirs = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
dirs_full = ["S_South", "SE_SouthEast", "E_East", "NE_NorthEast", "N_North", "NW_NorthWest", "W_West", "SW_SouthWest"]

# 7 Motions
motion_specs = [
    {"id": "01_idle", "title": "1. 정지상태 (Idle)", "frames": 4, "type": "idle"},
    {"id": "02_move", "title": "2. 이동 (Move)", "frames": 4, "type": "move"},
    {"id": "03_basic_attack", "title": "3. 기본공격 (BasicAttack)", "frames": 4, "type": "attack"},
    {"id": "04_dash_attack", "title": "4. 스킬 1 대쉬공격 (DashAttack)", "frames": 4, "type": "dash"},
    {"id": "05_ranged_sword_wave", "title": "5. 스킬 2 원거리공격 (RangedWave)", "frames": 4, "type": "wave"},
    {"id": "06_whirlwind_360", "title": "6. 스킬 3 360도 회전 (Whirlwind360)", "frames": 4, "type": "whirlwind"},
    {"id": "07_ultimate_ground_slam", "title": "7. 필살기 점프 내려찍기 (UltimateSlam)", "frames": 6, "type": "ultimate"}
]

# Function to generate distinct single 96x96 frame PNG
def render_single_frame(dir_idx, motion_type, frame_idx):
    # Transparent 96x96 cell
    cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    sprite = base_char.copy()
    
    w, h = sprite.size
    bounce = 0
    leg_shift = 0
    arm_angle = 0

    if motion_type == "move":
        bounce = -3 if (frame_idx % 2 == 1) else 0
        leg_shift = (frame_idx - 1.5) * 4
    elif motion_type == "attack":
        arm_angle = (frame_idx - 1.5) * 10
    elif motion_type == "dash":
        bounce = -2
        leg_shift = (frame_idx - 1.5) * 8
    elif motion_type == "ultimate":
        if frame_idx in [1, 2]: bounce = -14
        elif frame_idx in [3, 4]: bounce = 6

    # 8 Axis Transformation
    if dir_idx == 1: # SE
        sprite = sprite.resize((int(w * 0.92), h), Image.Resampling.NEAREST)
    elif dir_idx == 2: # E
        sprite = sprite.resize((int(w * 0.8), h), Image.Resampling.NEAREST)
        sprite = ImageEnhance.Brightness(sprite).enhance(0.95)
    elif dir_idx == 3: # NE
        sprite = sprite.resize((int(w * 0.88), h), Image.Resampling.NEAREST)
        sprite = ImageEnhance.Brightness(sprite).enhance(0.85)
    elif dir_idx == 4: # N
        sprite = ImageEnhance.Brightness(sprite).enhance(0.78)
    elif dir_idx == 5: # NW
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        sprite = sprite.resize((int(w * 0.88), h), Image.Resampling.NEAREST)
        sprite = ImageEnhance.Brightness(sprite).enhance(0.85)
    elif dir_idx == 6: # W
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        sprite = sprite.resize((int(w * 0.8), h), Image.Resampling.NEAREST)
        sprite = ImageEnhance.Brightness(sprite).enhance(0.95)
    elif dir_idx == 7: # SW
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        sprite = sprite.resize((int(w * 0.92), h), Image.Resampling.NEAREST)

    if arm_angle != 0:
        sprite = sprite.rotate(-arm_angle, expand=False, resample=Image.NEAREST)

    # Align to Bottom-Center pivot of 96x96 cell
    px = (cell_w - sprite.width) // 2 + int(leg_shift)
    py = cell_h - sprite.height - 8 + bounce
    
    cell.paste(sprite, (px, py), sprite)
    return cell

total_individual_frames = 0

# Generate Individual Frames and Grid Sheets
for spec in motion_specs:
    m_id = spec["id"]
    cols = spec["frames"]
    
    # Grid sheet setup (96x96 cell grid)
    grid_sheet_w = cell_w * cols
    grid_sheet_h = cell_h * 8
    grid_sheet = Image.new("RGBA", (grid_sheet_w, grid_sheet_h), (0, 0, 0, 0))

    for r in range(8):
        dir_code = dirs[r]
        
        # Folder for individual frames: e.g. 슈드용사/스프라이트이미지/개별프레임/01_idle/S/
        indiv_dir = os.path.join(target_base, "개별프레임", m_id, dir_code)
        os.makedirs(indiv_dir, exist_ok=True)
        
        for c in range(cols):
            # Render individual frame
            frame_img = render_single_frame(r, spec["type"], c)
            
            # Save individual frame file: frame_0.png, frame_1.png...
            frame_fname = f"frame_{c}.png"
            frame_path = os.path.join(indiv_dir, frame_fname)
            frame_img.save(frame_path)
            total_individual_frames += 1

            # Paste into Unity Grid Atlas Sheet
            grid_sheet.paste(frame_img, (c * cell_w, r * cell_h), frame_img)

    # Save Grid Sheet (e.g. 01_idle_grid_96x96.png)
    sheet_name = f"{m_id}_grid_96x96.png"
    
    # Save to all target locations
    for base_p in [target_base, typo_base, unity_assets_base, unity_assets_typo]:
        os.makedirs(base_p, exist_ok=True)
        grid_sheet.save(os.path.join(base_p, sheet_name))
        grid_sheet.save(os.path.join(base_p, f"{m_id}_8dir.png")) # Keep legacy name alias

    print(f"✅ [{spec['title']}] 개별 프레임 {cols*8}개 생성 + Unity Grid Atlas 시트 ({grid_sheet_w}x{grid_sheet_h}) 패킹 완료!")

print(f"🎉 총 {total_individual_frames}개의 개별 PNG 프레임 파일 분리 생성 & Unity Grid Sprite Atlas 시트 패킹 전수 완수!")
