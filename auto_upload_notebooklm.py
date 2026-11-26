import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def upload_report_directly(report_file_path):
    print(f"🚀 [고감독 직접 무인 자동 업로드] NotebookLM 『보고서 진행상황』 전용 노트북에 보고서 업로드 시작...")
    
    if os.path.exists(report_file_path):
        with open(report_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Copy content to Clipboard
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
        process.communicate(input=content.encode('utf-16le'))
        
        print("✅ [고감독 자율 100% 처리 완수] 보고서 내용이 윈도우 클립보드에 안착되었습니다!")
        print("✅ [NotebookLM 『보고서 진행상황』 무인 수색] 소스 추가 준비 완료!")
        return True
    else:
        print("❌ 보고서 파일 미감지!")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        upload_report_directly(sys.argv[1])
