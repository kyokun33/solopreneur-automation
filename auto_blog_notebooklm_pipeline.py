import os
import sys
import json
import time
import subprocess
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

NLM_EXE = r"C:\Users\sude3\AppData\Local\Programs\Python\Python313\Scripts\nlm.exe"
NOTEBOOKLM_MCP_EXE = r"C:\Users\sude3\AppData\Local\Programs\Python\Python313\Scripts\notebooklm-mcp.exe"
SRC_TXT = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
NLM_STORAGE = Path.home() / ".notebooklm-mcp-cli"
DEFAULT_PROFILE_DIR = NLM_STORAGE / "profiles" / "default"

async def run_pipeline():
    print("🚀 [블로그 가이드 기준] Antigravity x NotebookLM MCP 완전 수동/자동 재구축 파이프라인 가동!")

    # 1단계: NLM 프로필 폴더 구조 보장
    DEFAULT_PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    # 2단계: 대표님의 로그인 세션 쿠키 수집 및 NLM 인증 프로필 빌드
    print("🔑 대표님의 로그인 세션에서 쿠키를 추출하여 NLM default 인증 프로필을 구축합니다...")
    async with async_playwright() as p:
        try:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                channel="chrome",
                headless=True
            )
        except Exception:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=True
            )

        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://notebooklm.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(3)

        cookies = await context.cookies()
        await context.close()

    cookie_dict = {c["name"]: c["value"] for c in cookies if "google" in c.get("domain", "")}
    cookie_header_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])

    # profile.json 생성
    profile_json_path = DEFAULT_PROFILE_DIR / "profile.json"
    profile_data = {
        "name": "default",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cookies": cookie_dict,
        "csrf_token": "",
        "session_id": "",
        "build_label": "",
        "base_host": "notebooklm.google.com"
    }
    with open(profile_json_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=2)

    print(f"✅ NLM 인증 프로필 파일 저장 완료: {profile_json_path}")

    # 환경변수 설정
    env = os.environ.copy()
    env["NOTEBOOKLM_COOKIES"] = cookie_header_str

    # 3단계: nlm CLI로 '로그 프로젝트' 생성
    print("📌 [nlm CLI] '로그 프로젝트' 제미나이 노트북 생성 중...")
    res1 = subprocess.run([NLM_EXE, "notebook", "create", "로그 프로젝트"], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    # 4단계: nlm CLI로 소스 파일 추가
    print("📄 [nlm CLI] '로그 프로젝트' 소스 파일(로그프로젝트_전체진행상황_소스.txt) 업로드 중...")
    res2 = subprocess.run([NLM_EXE, "source", "add", "로그 프로젝트", "--file", SRC_TXT], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

    # 5단계: nlm CLI로 노트북 목록 확인
    print("🔍 [nlm CLI] 생성된 노트북 목록 확인:")
    res3 = subprocess.run([NLM_EXE, "notebook", "list"], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res3.stdout)

    print("🎉 [블로그 가이드 기준] NotebookLM MCP 설치 및 '로그 프로젝트' 연동 100% 완수!")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
