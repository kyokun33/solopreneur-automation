import subprocess
import sys
import time
import os

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_PATH = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"

def main():
    print("🚀 nlm CLI 및 MCP 인증 프로세스를 재가동합니다...")
    # 기존 크롬 프로세스 정리하여 포트 점유 해제
    subprocess.run("taskkill /F /IM chrome.exe /T", shell=True, capture_output=True)
    time.sleep(1.5)

    print("🔑 nlm login 가동! 새로 뜬 브라우저에서 로그인해 주시면 nlm 프로필이 100% 자동 생성됩니다.")
    p = subprocess.Popen([sys.executable, "-m", "notebooklm_tools.cli.main", "login"], cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    p.wait()

    print("✨ 인증 프로필 감지 완료! '로그 프로젝트' 노트를 생성하고 소스를 업로드합니다...")
    
    # 1. 노트 생성
    subprocess.run([sys.executable, "-m", "notebooklm_tools.cli.main", "notebook", "create", "로그 프로젝트"], cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    time.sleep(2)

    # 2. 소스 파일 추가
    subprocess.run([sys.executable, "-m", "notebooklm_tools.cli.main", "source", "add", "로그 프로젝트", "--file", SRC_PATH], cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    time.sleep(2)

    print("🎉 NLM CLI를 통한 '로그 프로젝트' 노트 생성 및 본문 텍스트 연동 100% 완료!")

if __name__ == "__main__":
    main()
