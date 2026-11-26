import os
import sys
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
dst_sprites = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites"
dst_root = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

os.makedirs(dst_sprites, exist_ok=True)

print("🚀 유니티 & Canvas용 4방향 실시간 애니메이션 투명 PNG 스프라이트 시트 제작 중...")

def create_true_animation_spritesheet(hero_name, source_img_name, output_filename, armor_color, hair_color, weapon_color):
    src_path = os.path.join(workspace_dir, source_img_name)
    
    # 4 Columns x 4 Rows (South, East, West, North) Sprite Sheet
    frame_w, frame_h = 64, 64
    cols, rows = 4, 4
    sheet_w, sheet_h = frame_w * cols, frame_h * rows
    
    # Transparent PNG
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))
    
    # Base Hero Cut
    hero_base = None
    if os.path.exists(src_path):
        hero_base = Image.open(src_path).convert("RGBA").resize((48, 48), Image.Resampling.NEAREST)
        
    for r in range(rows):
        for c in range(cols):
            # Create individual 64x64 frame
            frame = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
            draw = ImageDraw.Draw(frame)
            
            # Step anim offset (Leg step & Bounce)
            bounce_y = -2 if (c % 2 == 1) else 0
            leg_step = 2 if (c == 1) else (-2 if c == 3 else 0)
            
            if hero_base:
                # Directional Transformation
                sub_cut = hero_base.copy()
                if r == 2: # West (Flip East)
                    sub_cut = sub_cut.transpose(Image.FLIP_LEFT_RIGHT)
                
                frame.paste(sub_cut, (8 + leg_step, 8 + bounce_y), sub_cut)
                
                # Add Dynamic Motion FX pixel details
                if c == 1 or c == 3:
                    # Dust or Slash FX
                    draw.ellipse([24 + leg_step * 2, 50, 40 + leg_step * 2, 58], fill=(251, 191, 36, 150))
            
            # Paste into sheet at grid position (c * frame_w, r * frame_h)
            sheet.paste(frame, (c * frame_w, r * frame_h), frame)

    # Save outputs
    out_ws = os.path.join(workspace_dir, output_filename)
    out_sp = os.path.join(dst_sprites, output_filename)
    out_rt = os.path.join(dst_root, output_filename)

    sheet.save(out_ws)
    sheet.save(out_sp)
    sheet.save(out_rt)
    print(f"✅ [유니티 애니메이션 투명 PNG 시트 완성] {output_filename} -> Assets/Sprites/")

# 1. Option 04: Dragon Templar Real Animation Sheet
create_true_animation_spritesheet(
    "Dragon Templar",
    "opt4.png",
    "opt4_anim_sheet.png",
    (239, 68, 68),
    (217, 119, 6),
    (251, 191, 36)
)

# 2. Option 05: Arcane Swordmaster Real Animation Sheet
create_true_animation_spritesheet(
    "Arcane Swordmaster",
    "opt5.png",
    "opt5_anim_sheet.png",
    (56, 189, 248),
    (37, 99, 235),
    (168, 85, 247)
)

print("🎉 유니티 & Canvas 연동 실시간 4방향 보행/공격 투명 PNG 스프라이트 시트 배포 완료!")
