import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    browser = await async_playwright().start()
    context = await browser.chromium.launch_persistent_context(
        user_data_dir="./profile",
        headless=False,  # ОБЯЗАТЕЛЬНО false — мы запускаем через xvfb
    )

    page = await context.new_page()
    await page.goto("https://t.me/sticker_store_webapp?startapp=store")
    print("✅ Открыт Telegram WebApp. Войди через QR с телефона.")
    print("⌛ Ожидаю вход...")

    # Ждём ручной вход (дай 1–2 минуты)
    await asyncio.sleep(90)

    # Сохраняем сессию
    await context.storage_state(path="session.json")
    print("💾 session.json сохранён")

    await browser.stop()

asyncio.run(run())
