import os
import sys
import shutil
import subprocess

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SRC_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
TARGET_DIR = os.path.expanduser(r"~\.notebooklm-mcp-cli\profiles\default\chrome_user_data")
SRC_TXT = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"

def main():
    print("🚀 NLM Chrome 프로필 폴더 복사 및 세션 동기화를 진행합니다...")
    os.makedirs(os.path.dirname(TARGET_DIR), exist_ok=True)

    if os.path.exists(SRC_DIR):
        print(f"📁 '{SRC_DIR}' 세션을 NLM 프로필 위치로 동기화 중...")
        try:
            shutil.copytree(SRC_DIR, TARGET_DIR, dirs_exist_ok=True)
            print("✅ 프로필 동기화 완료!")
        except Exception as e:
            print(f"⚠️ 부분 복사 완료 (일부 파일 포함): {e}")

    # nlm CLI로 '로그 프로젝트' 생성 및 소스 업로드 테스트
    print("📌 nlm CLI: '로그 프로젝트' 노트북 생성 시도...")
    res = subprocess.run([sys.executable, "-m", "notebooklm_tools.cli.main", "notebook", "create", "로그 프로젝트"], capture_output=True, text=True, cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    print(res.stdout)
    print(res.stderr)

    print("📄 nlm CLI: '로그 프로젝트' 소스 업로드 시도...")
    res2 = subprocess.run([sys.executable, "-m", "notebooklm_tools.cli.main", "source", "add", "로그 프로젝트", "--file", SRC_TXT], capture_output=True, text=True, cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    print(res2.stdout)
    print(res2.stderr)

if __name__ == "__main__":
    main()
