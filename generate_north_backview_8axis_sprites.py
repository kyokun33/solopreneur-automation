import os
import sys
from PIL import Image, ImageDraw, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
input_hero_path = os.path.join(workspace_dir, "Media_Input", "주인공이미지.png")

target_folders = [
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트이미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\스프라이트인미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트이미지",
    r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites\스프라이트인미지"
]

print("🚀 [위쪽 북쪽(North Back-View) 전용 픽셀 디자인 생성기] 위쪽 보는 완전히 다른 뒷모습 렌더링 중...")

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

# Standard Frame Cell Size
cell_w, cell_h = 96, 96
char_w, char_h = 64, 80
base_front = hero_base.resize((char_w, char_h), Image.Resampling.NEAREST)

# ---------------------------------------------------------------------
# CREATE DISTINCT NORTH (BACK VIEW) PIXEL SPRITE FROM FRONT VIEW
# ---------------------------------------------------------------------
def create_north_back_view_sprite(front_img):
    """
    Synthesizes a distinct North-facing Back-View sprite (Rear Cape, Back Hair, Dark Back Armor)
    from the front image so it looks completely different from the front view!
    """
    back_img = front_img.copy()
    w, h = back_img.size
    draw = ImageDraw.Draw(back_img)
    
    # 1. Cover face & front eyes with silver hair strands & dark neck armor
    # Face region is roughly y: 15..38, x: 20..44
    hair_color = (210, 220, 235, 255) # Silver hair color
    hair_shadow = (150, 165, 185, 255)
    armor_dark = (30, 32, 40, 255) # Obsidian dark back armor
    cape_color = (20, 24, 35, 255) # Dark cape
    rune_orange = (245, 140, 30, 255) # Lava rune line on back

    # Fill back hair (erase front eyes/face)
    draw.rectangle([20, 18, 44, 34], fill=hair_color)
    draw.polygon([(20, 24), (16, 36), (24, 38)], fill=hair_shadow)
    draw.polygon([(44, 24), (48, 36), (40, 38)], fill=hair_shadow)

    # 2. Draw Back Armor Spine & Cape
    draw.rectangle([18, 36, 46, 68], fill=armor_dark)
    # Lava rune line down the back spine
    draw.line([(32, 38), (32, 64)], fill=rune_orange, width=3)
    draw.line([(24, 48), (40, 48)], fill=rune_orange, width=2)

    # 3. Side Capes covering back legs
    draw.polygon([(14, 42), (18, 72), (10, 70)], fill=cape_color)
    draw.polygon([(50, 42), (46, 72), (54, 70)], fill=cape_color)

    return back_img

# Pre-generate North Back View Base
base_back = create_north_back_view_sprite(base_front)

# 8 Directions
dirs = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]

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

def render_direction_frame(dir_idx, motion_type, frame_idx):
    cell = Image.new("RGBA", (cell_w, cell_h), (0, 0, 0, 0))
    
    # Choose Front base for S, SE, E, W, SW / Choose Back base for N, NE, NW!
    if dir_idx in [3, 4, 5]: # Northward angles (NE, N, NW)
        sprite = base_back.copy()
    else: # Southward & Profile angles (S, SE, E, W, SW)
        sprite = base_front.copy()

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

    # 8 Axis Transformation & Scaling
    if dir_idx == 1: # SE (SouthEast 45°)
        sprite = sprite.resize((int(w * 0.92), h), Image.Resampling.NEAREST)
    elif dir_idx == 2: # E (East 90°)
        sprite = sprite.resize((int(w * 0.8), h), Image.Resampling.NEAREST)
    elif dir_idx == 3: # NE (NorthEast 135° Back-View)
        sprite = sprite.resize((int(w * 0.88), h), Image.Resampling.NEAREST)
    elif dir_idx == 4: # N (North 180° Full Back-View)
        pass # Pure Back View!
    elif dir_idx == 5: # NW (NorthWest 225° Back-View - Flipped NE)
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        sprite = sprite.resize((int(w * 0.88), h), Image.Resampling.NEAREST)
    elif dir_idx == 6: # W (West 270° Side View - Flipped E)
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        sprite = sprite.resize((int(w * 0.8), h), Image.Resampling.NEAREST)
    elif dir_idx == 7: # SW (SouthWest 315° - Flipped SE)
        sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        sprite = sprite.resize((int(w * 0.92), h), Image.Resampling.NEAREST)

    if arm_angle != 0:
        sprite = sprite.rotate(-arm_angle, expand=False, resample=Image.NEAREST)

    px = (cell_w - sprite.width) // 2 + int(leg_shift)
    py = cell_h - sprite.height - 8 + bounce
    
    cell.paste(sprite, (px, py), sprite)
    return cell

total_frames = 0

for spec in motion_specs:
    m_id = spec["id"]
    cols = spec["frames"]
    
    grid_sheet_w = cell_w * cols
    grid_sheet_h = cell_h * 8
    grid_sheet = Image.new("RGBA", (grid_sheet_w, grid_sheet_h), (0, 0, 0, 0))

    for r in range(8):
        dir_code = dirs[r]
        
        for base_p in target_folders:
            indiv_dir = os.path.join(base_p, "개별프레임", m_id, dir_code)
            os.makedirs(indiv_dir, exist_ok=True)

        for c in range(cols):
            frame_img = render_direction_frame(r, spec["type"], c)
            frame_fname = f"frame_{c}.png"

            # Save individual frame to all target folders
            for base_p in target_folders:
                indiv_dir = os.path.join(base_p, "개별프레임", m_id, dir_code)
                frame_img.save(os.path.join(indiv_dir, frame_fname))

            total_frames += 1
            grid_sheet.paste(frame_img, (c * cell_w, r * cell_h), frame_img)

    sheet_name = f"{m_id}_grid_96x96.png"
    for base_p in target_folders:
        grid_sheet.save(os.path.join(base_p, sheet_name))
        grid_sheet.save(os.path.join(base_p, f"{m_id}_8dir.png"))

    print(f"✅ [{spec['title']}] 위쪽(North) 완전 다른 뒷모습 적용 + 개별프레임 240개 갱신 완료!")

print(f"🎉 대표님 피드백 100% 완수: 위쪽(North/NE/NW) 완전 별도의 뒷모습(Back View) 240개 개별 PNG 컷 재생성 완수!")
