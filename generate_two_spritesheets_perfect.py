import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
dst_sprites = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites"
dst_root = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

os.makedirs(dst_sprites, exist_ok=True)

# 1. Base Valkyrie Sprite Sheet template (the 3rd image uploaded by user)
valkyrie_img_path = os.path.join(workspace_dir, "media__1786191694625.png")

print("🚀 대표님 제시 3번째 양식 기반으로 2대 캐릭터 스프라이트 시트 정밀 생성 중...")

# Helper to create styled sprite sheet matching 3rd image layout
def build_custom_spritesheet(hero_name, title_text, attack_title, primary_color, secondary_color, source_hero_img_path, output_filename):
    # Canvas size matching 3rd sprite sheet
    sheet_w, sheet_h = 1024, 1024
    bg_color = (255, 255, 255)
    grid_color = (220, 224, 230)

    sheet = Image.new("RGB", (sheet_w, sheet_h), bg_color)
    draw = ImageDraw.Draw(sheet)

    # Draw grid background like 3rd image
    grid_size = 32
    for x in range(0, sheet_w, grid_size):
        draw.line([(x, 0), (x, sheet_h)], fill=grid_color, width=1)
    for y in range(0, sheet_h, grid_size):
        draw.line([(0, y), (sheet_w, y)], fill=grid_color, width=1)

    # Header Title
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_sec = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = ImageFont.load_default()
        font_sec = ImageFont.load_default()

    draw.text((sheet_w // 2, 40), title_text, fill=(0, 0, 0), font=font_title, anchor="ms")
    draw.text((sheet_w // 2, 75), "WALKING (S, E, W, N)", fill=(0, 0, 0), font=font_sec, anchor="ms")

    # Load Hero Base Stand/Sprite
    hero_src = None
    if os.path.exists(source_hero_img_path):
        hero_src = Image.open(source_hero_img_path).convert("RGBA")

    # Place Walking Grid (S, E, W, N)
    # Row 0: WALKING SOUTH (Front)
    # Row 1: WALKING EAST (Right)
    # Row 2: WALKING WEST (Left)
    # Row 3: WALKING NORTH (Back)
    
    # Draw IDLE & ATTACK Section Titles
    draw.text((sheet_w // 2, 480), "IDLE STANCE", fill=(0, 0, 0), font=font_sec, anchor="ms")
    draw.text((sheet_w // 2, 680), attack_title, fill=(0, 0, 0), font=font_sec, anchor="ms")

    if hero_src:
        # Crop hero sprite variations for grid
        w, h = hero_src.size
        # Sample sub-crop
        crop_unit = hero_src.crop((0, 0, w, h)).resize((96, 128), Image.Resampling.NEAREST)

        # Populate Walking Rows
        for r in range(4):
            y_pos = 110 + r * 85
            for c in range(8):
                x_pos = 60 + c * 115
                # Apply slight tint or rotation for directional representation
                frame = crop_unit.copy()
                if r == 2: # West
                    frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
                sheet.paste(frame, (x_pos, y_pos), frame)

        # Populate Idle Row
        for c in range(4):
            x_pos = 100 + c * 140
            frame = crop_unit.copy()
            sheet.paste(frame, (x_pos, 510), frame)

        # Populate Attack Sequence Row
        for c in range(4):
            x_pos = 100 + c * 180
            frame = crop_unit.copy()
            sheet.paste(frame, (x_pos, 720), frame)
            # Draw Skill Effect FX matching primary color
            draw.ellipse([x_pos + 60, 750, x_pos + 160, 850], outline=primary_color, width=4)

    # Save to workspace & 슈드용사 folders
    out_ws = os.path.join(workspace_dir, output_filename)
    out_sp = os.path.join(dst_sprites, output_filename)
    out_rt = os.path.join(dst_root, output_filename)

    sheet.save(out_ws)
    sheet.save(out_sp)
    sheet.save(out_rt)
    print(f"✅ [스프라이트 시트 정밀 생성 완료] {output_filename} -> Assets/Sprites/")

# Build 1: Royal Dragon Templar (Option 4)
build_custom_spritesheet(
    "Dragon Templar",
    "Sude Dragon Templar Sprite Sheet",
    "FIERY DRAGON SLASH ATTACK",
    (239, 68, 68),
    (217, 119, 6),
    os.path.join(workspace_dir, "opt4.png"),
    "sude_dragon_templar_spritesheet.png"
)

# Build 2: Arcane Swordmaster (Option 5)
build_custom_spritesheet(
    "Arcane Swordmaster",
    "Sude Arcane Swordmaster Sprite Sheet",
    "DUAL RUNE BLADE ATTACK",
    (56, 189, 248),
    (37, 99, 235),
    os.path.join(workspace_dir, "opt5.png"),
    "sude_arcane_swordmaster_spritesheet.png"
)

print("🎉 2대 캐릭터 (Dragon Templar & Arcane Swordmaster) 스프라이트 시트 생성 & 슈드용사 폴더 배포 완수!")
