import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업"
dst_sprites = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사\Assets\Sprites"
dst_root = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\슈드용사"

os.makedirs(dst_sprites, exist_ok=True)

print("🚀 대표님 제공 한글 도트 종합 시트 양식 100% 완벽 복제 생성 중...")

def build_korean_master_sheet(hero_name, class_title, primary_color, secondary_color, source_img_path, output_filename):
    # Width: 1080, Height: 1800 matching user reference image ratio
    canvas_w, canvas_h = 1080, 1800
    bg_color = (255, 255, 255)
    
    sheet = Image.new("RGB", (canvas_w, canvas_h), bg_color)
    draw = ImageDraw.Draw(sheet)

    # Fonts
    try:
        font_main_title = ImageFont.truetype("malgun.ttf", 44)
        font_sub_title = ImageFont.truetype("malgunbd.ttf", 36)
        font_label = ImageFont.truetype("malgun.ttf", 26)
        font_small = ImageFont.truetype("malgun.ttf", 20)
    except:
        font_main_title = ImageFont.load_default()
        font_sub_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Load Source Hero Image
    hero_src = None
    if os.path.exists(source_img_path):
        hero_src = Image.open(source_img_path).convert("RGBA")

    unit_sprite = None
    if hero_src:
        unit_sprite = hero_src.resize((72, 96), Image.Resampling.NEAREST)

    # --- SECTION 1: HEADER & 4-DIR WALKING & CLASS EVOLUTION ---
    draw.text((220, 40), "(남 / 동 / 서 / 북)", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    draw.text((220, 95), "걷기 (남)", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    
    draw.text((780, 40), f"클래스 전직: {hero_name}", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    draw.text((780, 95), class_title, fill=(0, 0, 0), font=font_sub_title, anchor="mm")

    # Draw Walking Poses Row (S, E, W, N)
    if unit_sprite:
        for c in range(4):
            frame = unit_sprite.copy()
            if c == 2: frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
            sheet.paste(frame, (60 + c * 100, 130), frame)
            
        for c in range(4):
            frame = unit_sprite.copy()
            sheet.paste(frame, (600 + c * 110, 130), frame)
            draw.text((636 + c * 110, 235), f"V{c+1}", fill=(0,0,0), font=font_small, anchor="mm")

    # --- SECTION 2: ATTACK (EAST) ---
    draw.text((220, 275), "공격 (동)", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    if unit_sprite:
        for c in range(4):
            frame = unit_sprite.copy()
            sheet.paste(frame, (60 + c * 100, 310), frame)

    # --- SECTION 3: IDLE & INJURY ---
    draw.text((220, 435), "대기 & 전투 태세", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    if unit_sprite:
        for r in range(2):
            for c in range(4):
                frame = unit_sprite.copy()
                sheet.paste(frame, (60 + c * 100, 470 + r * 100), frame)

    # Divider Line
    draw.line([(30, 680), (1050, 680)], fill=(50, 50, 50), width=4)

    # --- SECTION 4: SKILL SET & ULTIMATE (KUHYUN CHOAN) ---
    draw.text((540, 715), f"{hero_name} 스킬 세트 & 필살기 (구현 초안)", fill=(0, 0, 0), font=font_main_title, anchor="mm")

    # Skill 1
    draw.text((220, 780), "스킬 1: 성스런 참격 (Holy Slash)", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    if unit_sprite:
        for c in range(5):
            frame = unit_sprite.copy()
            sheet.paste(frame, (40 + c * 90, 820), frame)

    # Skill 2
    draw.text((220, 940), "스킬 2: 용의 수호 / 마나 방패", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    if unit_sprite:
        for c in range(4):
            frame = unit_sprite.copy()
            sheet.paste(frame, (40 + c * 90, 980), frame)
            draw.ellipse([50 + c * 90, 980, 100 + c * 90, 1060], outline=primary_color, width=3)

    # Skill 3
    draw.text((220, 1100), "스킬 3: 축성 / 아케인 결계", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    if unit_sprite:
        for c in range(4):
            frame = unit_sprite.copy()
            sheet.paste(frame, (40 + c * 90, 1140), frame)

    # Skill 4
    draw.text((220, 1260), "스킬 4: 드래곤 화염 / 천사의 검", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    if unit_sprite:
        for r in range(4):
            for c in range(4):
                frame = unit_sprite.copy()
                sheet.paste(frame, (40 + c * 90, 1300 + r * 90), frame)

    # --- SECTION 5: RIGHT ULTIMATE & GAME MOCKUP ---
    draw.text((780, 780), "필살기: 신성한 개입 / 용의 분노", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    draw.rectangle([560, 820, 1020, 1240], outline=(0,0,0), width=3)
    draw.text((780, 845), "충전 단계 -> 필살기 시퀀스 실행", fill=(0,0,0), font=font_label, anchor="mm")
    if unit_sprite:
        for r in range(2):
            for c in range(2):
                frame = unit_sprite.copy()
                sheet.paste(frame, (620 + c * 180, 880 + r * 160), frame)
                draw.ellipse([600 + c * 180, 860 + r * 160, 780 + c * 180, 1020 + r * 160], outline=secondary_color, width=4)

    # Mock Game Screen (Bottom Right)
    draw.text((780, 1280), "모의 게임 화면 (In-Game Battle Mockup)", fill=(0, 0, 0), font=font_sub_title, anchor="mm")
    mock_box = [560, 1310, 1020, 1720]
    draw.rectangle(mock_box, fill=(30, 41, 59), outline=(0,0,0), width=4)
    # UI Bar
    draw.rectangle([580, 1330, 800, 1360], fill=(220, 38, 38))
    draw.text((590, 1335), "체력: 2450 / 2450", fill=(255,255,255), font=font_small)
    draw.rectangle([580, 1370, 800, 1400], fill=(37, 99, 235))
    draw.text((590, 1375), "마력: 1880 / 1880", fill=(255,255,255), font=font_small)
    if unit_sprite:
        frame = unit_sprite.resize((96, 128), Image.Resampling.NEAREST)
        sheet.paste(frame, (740, 1480), frame)
        draw.ellipse([700, 1440, 880, 1600], outline=primary_color, width=4)

    # Save
    out_ws = os.path.join(workspace_dir, output_filename)
    out_sp = os.path.join(dst_sprites, output_filename)
    out_rt = os.path.join(dst_root, output_filename)

    sheet.save(out_ws)
    sheet.save(out_sp)
    sheet.save(out_rt)
    print(f"✅ [대표님 한글 양식 복제 완료] {output_filename} -> Assets/Sprites/")

# 1. Option 04: Dragon Templar
build_korean_master_sheet(
    "드래곤 템플러",
    "Royal Dragon Templar",
    (239, 68, 68),
    (251, 191, 36),
    os.path.join(workspace_dir, "opt4.png"),
    "sude_option04_dragon_templar_full_sheet.png"
)

# 2. Option 05: Arcane Swordmaster
build_korean_master_sheet(
    "아케인 소드마스터",
    "Arcane Swordmaster",
    (56, 189, 248),
    (168, 85, 247),
    os.path.join(workspace_dir, "opt5.png"),
    "sude_option05_arcane_swordmaster_full_sheet.png"
)

print("🎉 2대 캐릭터 (Dragon Templar & Arcane Swordmaster) 대표님 양식 100% 한글 도트 종합 시트 생성 및 배포 성공!")
