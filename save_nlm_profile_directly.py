import os
import sys
import json
import asyncio
from playwright.async_api import async_playwright

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

USER_DATA_DIR = os.path.expanduser(r"~\.notebooklm_real_session")
PROFILE_DIR = os.path.expanduser(r"~\AppData\Local\notebooklm-mcp\profiles")
DEFAULT_PROFILE = os.path.join(PROFILE_DIR, "default.json")

async def create_profile():
    print("🚀 NLM 프로필 저장소를 탐색하고 인증 프로필을 직접 생성합니다...")
    os.makedirs(PROFILE_DIR, exist_ok=True)

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
        cookie_dict = {c["name"]: c["value"] for c in cookies if "google" in c.get("domain", "")}

        profile_data = {
            "name": "default",
            "cookies": cookie_dict,
            "raw_cookies": cookies
        }

        with open(DEFAULT_PROFILE, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=2)

        print(f"✅ NLM 인증 프로필 저장 완료: {DEFAULT_PROFILE}")

if __name__ == "__main__":
    asyncio.run(create_profile())
