import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

report_path = r"C:\Users\sude3\.gemini\antigravity-ide\brain\a666220d-4085-4ee9-b4f9-6ea8727b4996\mobile_app_capability_report.md"

if os.path.exists(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
    process.communicate(input=content.encode('utf-16le'))
    print("✅ [클립보드 자동 복사 완료] 모바일 앱 개발 역량 보고서가 윈도우 클립보드(Ctrl+V)에 복사되었습니다!")
else:
    print("❌ 보고서 파일 미감지")
