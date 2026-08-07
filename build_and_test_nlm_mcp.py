import os
import sys
import json
import time
import subprocess
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

from notebooklm_tools.core.auth import AuthManager

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

NLM_EXE = r"C:\Users\sude3\AppData\Local\Programs\Python\Python313\Scripts\nlm.exe"
SRC_TXT = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"
USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")

async def build_profile():
    print("🔑 대표님의 로그인 세션에서 구글 쿠키를 추출하여 AuthManager 프로필을 구축합니다...")
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
        await asyncio.sleep(2)

        cookies = await context.cookies()
        await context.close()

    print(f"✅ 총 {len(cookies)}개 쿠키 추출 성공!")

    auth = AuthManager("default")
    profile = auth.save_profile(
        cookies=cookies,
        email="sude3@gmail.com",
        force=True
    )
    print(f"💾 AuthManager.save_profile 완수! profile_exists: {auth.profile_exists()}")

    # nlm notebook list 테스트
    print("📌 [nlm CLI] nlm notebook list 실행 테스트...")
    res = subprocess.run([NLM_EXE, "notebook", "list"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)

    # nlm notebook create 테스트
    print("📌 [nlm CLI] '로그 프로젝트' 제미나이 노트북 생성 중...")
    res1 = subprocess.run([NLM_EXE, "notebook", "create", "로그 프로젝트"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    # nlm source add 테스트
    print("📄 [nlm CLI] '로그 프로젝트' 소스 원고 추가 중...")
    res2 = subprocess.run([NLM_EXE, "source", "add", "로그 프로젝트", "--file", SRC_TXT], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

if __name__ == "__main__":
    asyncio.run(build_profile())
