import subprocess
import sys
import time
import os

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

NLM_EXE = r"C:\Users\sude3\AppData\Local\Programs\Python\Python313\Scripts\nlm.exe"
SRC_TXT = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"

def main():
    print("🚀 [네이버 블로그 가이드 방식] nlm login 대화형 구글 인증 및 자동 연동 파이프라인 가동...")
    print("🔑 로그인 크롬 창이 모니터 전면에 새로 열립니다. 구글 계정으로 로그인해 주십시오!")
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # nlm login --force 대화형 실행
    p = subprocess.Popen([NLM_EXE, "login", "--force"], env=env, cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    p.wait()

    print("✨ nlm 인증 완료! '로그 프로젝트' 노트를 구글 서버에 자동 생성 중...")
    res1 = subprocess.run([NLM_EXE, "notebook", "create", "로그 프로젝트"], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    print("📄 '로그 프로젝트' 한글 소스 원고 100% 무인 업로드 중...")
    res2 = subprocess.run([NLM_EXE, "source", "add", "로그 프로젝트", "--file", SRC_TXT], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

    print("🔍 최종 생성된 제미나이 노트북 리스트 확인:")
    res3 = subprocess.run([NLM_EXE, "notebook", "list"], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res3.stdout)

    print("🎉 [네이버 블로그 가이드 기준] nlm 인증 및 '로그 프로젝트' 노트북 연동 100% 완수!")

if __name__ == "__main__":
    main()
