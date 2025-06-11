import asyncio
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Загружаем переменные из .env
load_dotenv()
STICKER_URL = os.getenv("STICKER_URL")
COOKIE_PATH = os.getenv("COOKIE_PATH", "session.json")

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Загружаем сохранённую сессию, если есть
        context = None
        if os.path.exists(COOKIE_PATH):
            context = await browser.new_context(storage_state=COOKIE_PATH)
            print("🔐 Сессия загружена.")
        else:
            context = await browser.new_context()
            print("🕹 Первый запуск. Войди вручную в Telegram и не закрывай окно!")

        page = await context.new_page()
        await page.goto(STICKER_URL)
        print("🌐 Открыл Sticker Store")

        # Если это первый вход — ждём авторизацию вручную
        if not os.path.exists(COOKIE_PATH):
            print("⏳ Ожидаю вход в Telegram... После входа — нажми Enter.")
            input("👉 Нажми Enter, когда авторизуешься...")

            # Сохраняем сессию
            await context.storage_state(path=COOKIE_PATH)
            print("💾 Сессия сохранена в", COOKIE_PATH)

        # Ждём кнопку "Buy" (адаптируй селектор при необходимости)
        try:
            await page.wait_for_selector("button", timeout=10000)
            buttons = await page.query_selector_all("button")

            for btn in buttons:
                text = await btn.inner_text()
                if "Buy" in text or "Купить" in text:
                    await btn.click()
                    print("🎯 Куплено!")
                    break
            else:
                print("⚠️ Кнопка 'Buy' не найдена.")

        except Exception as e:
            print("❌ Ошибка:", e)

        await asyncio.sleep(5)
        await browser.close()

asyncio.run(run())
