import os
import sys
import winreg
import datetime
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# Import ReportLab modules
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

print("🚀 [고감독 C드라이브 프로그램 정밀 스캐너] 레지스트리 및 디스크 용량 탐색 중...")

# Register Korean Font (Malgun Gothic)
font_path = r"C:\Windows\Fonts\malgun.ttf"
font_bold_path = r"C:\Windows\Fonts\malgunbd.ttf"

pdfmetrics.registerFont(TTFont('MalgunGothic', font_path))
pdfmetrics.registerFont(TTFont('MalgunGothicBold', font_bold_path))

# Registry Uninstall Keys
registry_keys = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")
]

installed_apps = []
seen_names = set()

def get_folder_size_mb(folder_path):
    if not os.path.exists(folder_path):
        return 0
    total_size = 0
    try:
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                try:
                    fp = os.path.join(root, f)
                    total_size += os.path.getsize(fp)
                except:
                    pass
    except:
        pass
    return round(total_size / (1024 * 1024), 1)

# Categorize Function
def categorize_app(name, path):
    name_l = name.lower()
    path_l = path.lower() if path else ""
    
    if any(k in name_l for k in ['unity', 'epic', 'steam', 'game', 'genshin', 'roblox', 'lol', 'overwatch']):
        return "🎮 게임 & 게임엔진"
    elif any(k in name_l for k in ['python', 'comfyui', 'pytorch', 'adobe', 'photoshop', 'premiere', 'blender', 'cuda', 'nvidia', 'ai']):
        return "🎨 AI & 미디어 & 그래픽"
    elif any(k in name_l for k in ['visual studio', 'vscode', 'git', 'node.js', 'docker', 'android studio', 'java', 'sdk']):
        return "💻 개발 & IT 도구"
    elif any(k in name_l for k in ['chrome', 'edge', 'brave', 'bandizip', 'kakaotalk', 'hancom', 'alzip', 'v3', 'alyac']):
        return "🌐 브라우저 & 유틸리티"
    elif any(k in name_l for k in ['office', 'excel', 'word', 'powerpoint', 'onedrive', 'notion', 'zoom']):
        return "💼 업무 & 클라우드"
    else:
        return "🛠️ 일반 소프트웨어"

# Collect from Windows Registry
for root_key, subkey in registry_keys:
    try:
        key = winreg.OpenKey(root_key, subkey)
        for i in range(0, winreg.QueryInfoKey(key)[0]):
            try:
                sub_name = winreg.EnumKey(key, i)
                sub_key = winreg.OpenKey(key, sub_name)
                
                disp_name = ""
                inst_location = ""
                uninst_str = ""
                inst_date = ""
                size_mb = 0.0

                try: disp_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                except: pass
                
                if not disp_name or disp_name in seen_names or "update" in disp_name.lower():
                    continue

                try: inst_location = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                except: pass
                
                try: uninst_str = winreg.QueryValueEx(sub_key, "UninstallString")[0]
                except: pass
                
                try: inst_date = str(winreg.QueryValueEx(sub_key, "InstallDate")[0])
                except: pass
                
                try:
                    estimated_size = winreg.QueryValueEx(sub_key, "EstimatedSize")[0]
                    size_mb = round(estimated_size / 1024, 1)
                except:
                    pass

                # If size missing in registry, calculate from InstallLocation
                if size_mb == 0 and inst_location and os.path.exists(inst_location):
                    size_mb = get_folder_size_mb(inst_location)

                # Date formatting
                formatted_date = "-"
                if inst_date and len(inst_date) == 8:
                    formatted_date = f"{inst_date[:4]}-{inst_date[4:6]}-{inst_date[6:]}"
                elif inst_location and os.path.exists(inst_location):
                    try:
                        mtime = os.path.getmtime(inst_location)
                        formatted_date = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                    except:
                        pass

                # Clean Uninstall Method text
                clean_uninst = "설정 -> 앱 및 기능 삭제"
                if uninst_str:
                    if "msiexec" in uninst_str.lower():
                        clean_uninst = f"MSI 언인스톨러 ({uninst_str[:35]})"
                    else:
                        clean_uninst = f"제거 실행파일: {os.path.basename(uninst_str)}"

                cat = categorize_app(disp_name, inst_location)

                installed_apps.append({
                    "name": disp_name,
                    "category": cat,
                    "size_mb": size_mb,
                    "size_gb": round(size_mb / 1024, 2),
                    "date": formatted_date,
                    "path": inst_location if inst_location else "C:\\Program Files 및 관련 경로",
                    "uninstall": clean_uninst
                })
                seen_names.add(disp_name)
            except:
                pass
    except:
        pass

# Add Known Large Software Directories manually if missed
large_known = [
    ("ComfyUI Desktop / Portable", r"C:\ComfyUI_windows_portable", "🎨 AI & 미디어 & 그래픽"),
    ("Unity Engine / Hub", r"C:\Program Files\Unity", "🎮 게임 & 게임엔진"),
    ("Microsoft Visual Studio", r"C:\Program Files\Microsoft Visual Studio", "💻 개발 & IT 도구"),
    ("Android SDK / Studio", r"C:\Users\sude3\AppData\Local\Android", "💻 개발 & IT 도구"),
    ("Python Environments", r"C:\Users\sude3\AppData\Local\Programs\Python", "🎨 AI & 미디어 & 그래픽")
]

for l_name, l_path, l_cat in large_known:
    if os.path.exists(l_path) and l_name not in seen_names:
        l_size = get_folder_size_mb(l_path)
        if l_size > 50:
            mtime = os.path.getmtime(l_path)
            f_date = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
            installed_apps.append({
                "name": l_name,
                "category": l_cat,
                "size_mb": l_size,
                "size_gb": round(l_size / 1024, 2),
                "date": f_date,
                "path": l_path,
                "uninstall": "폴더 삭제 또는 전용 Uninstaller 실행"
            })
            seen_names.add(l_name)

# Sort Descending by Size (MB)
installed_apps.sort(key=lambda x: x["size_mb"], reverse=True)

print(f"✅ 총 {len(installed_apps)}개 정식 설치 프로그램 감지 완료! (용량 순 내림차순 정렬)")

# PDF Output Paths
pdf_output_path = r"c:\Users\sude3\OneDrive\바탕 화면\📊_C드라이브_설치프로그램_용량순_정밀분석보고서.pdf"
workspace_pdf_path = r"c:\Users\sude3\OneDrive\바탕 화면\1인기업\📊_C드라이브_설치프로그램_용량순_정밀분석보고서.pdf"

# Build PDF Document (A4 Landscape for perfect table width)
doc = SimpleDocTemplate(
    pdf_output_path,
    pagesize=landscape(A4),
    leftMargin=20, rightMargin=20, topMargin=25, bottomMargin=25
)

story = []
styles = getSampleStyleSheet()

# Custom Text Styles (Ensuring 100% Word Wrap & Text Wrapping Safety)
title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='MalgunGothicBold', fontSize=20, leading=26, textColor=colors.HexColor('#1e1b4b'))
subtitle_style = ParagraphStyle('DocSubtitle', parent=styles['Normal'], fontName='MalgunGothic', fontSize=10, leading=14, textColor=colors.HexColor('#475569'))
cat_header_style = ParagraphStyle('CatHeader', parent=styles['Normal'], fontName='MalgunGothicBold', fontSize=12, leading=16, textColor=colors.HexColor('#0f172a'))

# Table Cell Text Styles (Paragraph WordWrap)
th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='MalgunGothicBold', fontSize=9, leading=11, textColor=colors.white, alignment=1)
td_style = ParagraphStyle('TD', parent=styles['Normal'], fontName='MalgunGothic', fontSize=8, leading=11, textColor=colors.HexColor('#0f172a'))
td_bold = ParagraphStyle('TDBold', parent=styles['Normal'], fontName='MalgunGothicBold', fontSize=8.5, leading=11, textColor=colors.HexColor('#b91c1c'))
td_code = ParagraphStyle('TDCode', parent=styles['Normal'], fontName='MalgunGothic', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#334155'))

# Document Header
story.append(Paragraph("📊 [Connect AI] C드라이브 전체 프로그램 용량순 정밀 분석 보고서", title_style))
story.append(Spacer(1, 4))
now_str = datetime.datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
story.append(Paragraph(f"총괄 디렉터: 고감독 (Antigravity) | 분석 일시: {now_str} | 대상: C: 드라이브 전체 프로그램 ({len(installed_apps)}개 감지)", subtitle_style))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#ef4444'), spaceAfter=12))

# Table Header Data
table_data = [[
    Paragraph("순위", th_style),
    Paragraph("프로그램 명칭", th_style),
    Paragraph("카테고리", th_style),
    Paragraph("차지 용량", th_style),
    Paragraph("설치 날짜", th_style),
    Paragraph("설치 경로 (Install Location)", th_style),
    Paragraph("삭제 및 제거 방법 (Uninstall Method)", th_style)
]]

total_scanned_gb = 0.0

for rank, app in enumerate(installed_apps, start=1):
    total_scanned_gb += app['size_gb']
    
    # Size Display formatting
    if app['size_gb'] >= 1.0:
        size_display = f"{app['size_gb']} GB"
    else:
        size_display = f"{app['size_mb']} MB"

    row = [
        Paragraph(str(rank), td_bold if rank <= 10 else td_style),
        Paragraph(app['name'], td_bold if rank <= 10 else td_style),
        Paragraph(app['category'], td_style),
        Paragraph(size_display, td_bold if app['size_gb'] >= 1.0 else td_style),
        Paragraph(app['date'], td_style),
        Paragraph(app['path'], td_code),
        Paragraph(app['uninstall'], td_code)
    ]
    table_data.append(row)

# Column Widths (A4 Landscape Total Printable Width = 842 - 40 = 802pt)
col_widths = [32, 160, 110, 65, 65, 200, 170]

col_table = Table(table_data, colWidths=col_widths, repeatRows=1)

# Table Styling (High End Modern Theme)
col_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ('ALIGN', (3, 0), (4, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))

story.append(col_table)
story.append(Spacer(1, 15))

# Summary Footer Paragraph
summary_p = Paragraph(f"<b>💡 [고감독 종합 요약]</b> 스캔 완료된 C드라이브 정식 프로그램 총 차지 용량: <b>약 {round(total_scanned_gb, 2)} GB</b> | 상위 10개 프로그램이 디스크 용량의 대다수를 차지하고 있으므로 미사용 프로그램은 우측 '삭제 및 제거 방법'의 안내에 따라 정리하실 수 있습니다.", cat_header_style)
story.append(summary_p)

# Build Document
doc.build(story)

# Copy to Workspace Folder too
if os.path.exists(pdf_output_path):
    import shutil
    shutil.copy(pdf_output_path, workspace_pdf_path)

print("🎉 C드라이브 용량순 정밀 분석 PDF 보고서 생성 완료!")
print(f"📁 바탕화면 PDF 경로: {pdf_output_path}")
