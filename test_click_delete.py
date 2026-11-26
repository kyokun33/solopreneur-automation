import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROFILE_DIR = r"C:\Users\sude3\.chrome_dev_profile"

async def main():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            PROFILE_DIR,
            channel="chrome",
            headless=False,
            args=["--start-maximized"],
            no_viewport=True
        )

        page = context.pages[0] if len(context.pages) > 0 else await context.new_page()
        await page.goto("https://notebook.google.com/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        # Find menu button for an untitled notebook card
        menu_btns = page.locator("button:has-text('more_vert')")
        print("Menu buttons count:", await menu_btns.count())

        if await menu_btns.count() > 2:
            # Click menu button on card #2
            await menu_btns.nth(2).click(force=True)
            await asyncio.sleep(1.5)

            # Click '삭제' menu item
            del_text = page.get_by_text("삭제", exact=True)
            if await del_text.count() > 0:
                print("Clicking '삭제' text...")
                box = await del_text.first.bounding_box()
                if box:
                    await page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    await asyncio.sleep(2)

                    await page.screenshot(path="temp_delete_dialog_popup.png", full_page=True)

                    # Check dialog elements
                    dialog_texts = await page.locator("mat-dialog-container *, div[role='dialog'] *").all_inner_texts()
                    print("Dialog inner texts:", set(dialog_texts))

                    # Click confirm delete in dialog
                    confirm_btn = page.locator("mat-dialog-container button, div[role='dialog'] button").filter(has_text="삭제").first
                    if await confirm_btn.count() > 0:
                        print("Clicking confirmation delete button in dialog...")
                        await confirm_btn.click(force=True)
                        await asyncio.sleep(3)

                        await page.screenshot(path="temp_after_deletion.png", full_page=True)

        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
