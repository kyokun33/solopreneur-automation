import asyncio
import os
import sys
import subprocess
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
SRC_TXT = r"c:\Users\sude3\OneDrive\바탕 화면\로그프로젝트_전체진행상황_소스.txt"

async def run():
    print("🔑 대표님의 로그인 세션에서 구글 인증 쿠키 문자열을 직접 조립합니다...")
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
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies if "google" in c.get("domain", "")])
        print(f"✅ 총 {len(cookies)}개 쿠키 조립 완료! (길이: {len(cookie_str)}자)")
        await context.close()

    env = os.environ.copy()
    env["NOTEBOOKLM_COOKIES"] = cookie_str

    print("📌 [nlm CLI] '로그 프로젝트' 노트북 생성 명령 실행...")
    cmd1 = [sys.executable, "-m", "notebooklm_tools.cli.main", "notebook", "create", "로그 프로젝트"]
    res1 = subprocess.run(cmd1, env=env, capture_output=True, text=True, cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    print("STDOUT:", res1.stdout)
    print("STDERR:", res1.stderr)

    print("📄 [nlm CLI] '로그 프로젝트' 소스 파일 직접 탑재...")
    cmd2 = [sys.executable, "-m", "notebooklm_tools.cli.main", "source", "add", "로그 프로젝트", "--file", SRC_TXT]
    res2 = subprocess.run(cmd2, env=env, capture_output=True, text=True, cwd=r"c:\Users\sude3\OneDrive\바탕 화면\1인기업")
    print("STDOUT:", res2.stdout)
    print("STDERR:", res2.stderr)

    print("🎉 jacob-bd/gemini-notebook-mcp-cli 엔진을 통한 '로그 프로젝트' 무인 업로드 완수!")

if __name__ == "__main__":
    asyncio.run(run())
