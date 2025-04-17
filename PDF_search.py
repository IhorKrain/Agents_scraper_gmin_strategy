import asyncio
import os
import aiohttp
import aiofiles
from urllib.parse import quote
from playwright.async_api import async_playwright

SAVE_DIR = "pdfs"
os.makedirs(SAVE_DIR, exist_ok=True)

# Отдельный список для сайтов, которые требуют специальной обработки
SPECIAL_SITES = ["bibliotekanauki.pl", "bip.lubelskie.pl"]

async def download_pdf_direct(url, save_dir=SAVE_DIR):
    filename = url.split("/")[-1].split("?")[0]
    if not filename.endswith(".pdf"):
        filename += ".pdf"
    filepath = os.path.join(save_dir, filename)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                content_type = resp.headers.get("Content-Type", "")
                if resp.status == 200 and "application/pdf" in content_type:
                    async with aiofiles.open(filepath, mode="wb") as f:
                        await f.write(await resp.read())
                    print(f"✅ PDF saved (direct): {filepath}")
                    return filepath
                else:
                    print(f"❌ Not a PDF or bad response: {url}")
    except Exception as e:
        print(f"⚠️ Direct download error: {e}")
    return None

async def download_pdf_via_playwright(page, url, save_dir=SAVE_DIR):
    try:
        await page.goto(url)
        await page.wait_for_timeout(3000)

        # Ищем iframe с PDF
        frames = page.frames
        for frame in frames:
            frame_url = frame.url
            if frame_url.endswith(".pdf"):
                return await download_pdf_direct(frame_url, save_dir)

        # Или кнопку "Pobierz" / "Download"
        buttons = await page.query_selector_all("a, button")
        for btn in buttons:
            text = (await btn.inner_text()).lower()
            if "pobierz" in text or "download" in text or "pdf" in text:
                async with page.expect_download() as download_info:
                    await btn.click()
                download = await download_info.value
                save_path = os.path.join(save_dir, download.suggested_filename)
                await download.save_as(save_path)
                print(f"📥 PDF saved (via Playwright): {save_path}")
                return save_path

        print(f"⚠️ PDF not found interactively: {url}")
    except Exception as e:
        print(f"❌ Playwright interaction failed: {url}\n   Reason: {e}")
    return None

async def download_pdf(page, url):
    for domain in SPECIAL_SITES:
        if domain in url:
            return await download_pdf_via_playwright(page, url)
    return await download_pdf_direct(url)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://duckduckgo.com")
        await page.fill("input[name='q']", "filetype:pdf strategia rozwoju gminy jack\xF3w")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(3000)

        links = await page.query_selector_all("a")
        pdf_links = set()
        for link in links:
            href = await link.get_attribute("href")
            if href and href.endswith(".pdf"):
                pdf_links.add(href)

        print(f"\n🔗 Znaleziono {len(pdf_links)} PDF link\xF3w.\n")

        for link in pdf_links:
            await download_pdf(page, link)

        await browser.close()

asyncio.run(run())

