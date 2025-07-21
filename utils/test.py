import random, os, asyncio
from playwright.async_api import async_playwright
from utils.retry_stats import init_stats
from utils.name_generator import get_random_name, get_random_dob
from utils.gmail_loader import load_emails, mark_email

def run_bulk_creation(config, st=None, progress=None):
    stats = init_stats()
    headless = config.get("headless", True)
    max_tabs = config.get("max_tabs", 3)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    EMAILS = load_emails()

    for i in range(max_tabs):
        if i < len(EMAILS):
            email_line = EMAILS[i]
            loop.run_until_complete(create_account(i + 1, headless, stats, st, progress, i, max_tabs, email_line))
        else:
            if st: st.warning("Not enough Gmail accounts available!")
            break

    return {"stats": stats}

async def create_account(tab_id, headless, stats, st, progress, index, total, email_line):
    try:
        email, app_pass = email_line.strip().split("|")
        first, last = get_random_name()
        day, month, year = get_random_dob()
        password = f"{first.lower()}{random.randint(1000,9999)}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Linux; Android 10) Chrome/119.0.0.0 Mobile Safari/537.36",
                viewport={"width": 412, "height": 915},
                is_mobile=True
            )
            page = await context.new_page()
            await page.goto("https://m.facebook.com/reg")

            await page.fill('input[name="firstname"]', first)
            await page.fill('input[name="lastname"]', last)
            await page.fill('input[name="reg_email__"]', email)
            await page.fill('input[name="reg_passwd__"]', password)
            await page.select_option('select[name="birthday_day"]', str(day))
            await page.select_option('select[name="birthday_month"]', month)
            await page.select_option('select[name="birthday_year"]', str(year))
            await page.click('input[value="2"]')  # Gender: Male
            await page.click('button[name="websubmit"]')

            stats["signup"]["success"] += 1
            mark_email(email_line, "used")

            os.makedirs("accounts/output", exist_ok=True)
            with open(f"accounts/output/{first.lower()}{last.lower()}.txt", "w") as f:
                f.write(f"{email}|{password}\n")

            msg = f"[Tab {tab_id}] ✅ Form submitted for {email}"
            if st: st.success(msg)
            if progress: progress.progress((index + 1) / total)

            await asyncio.sleep(5)
            await browser.close()

    except Exception as e:
        mark_email(email_line, "failed")
        stats["signup"]["failure"] += 1
        stats["signup"]["last_error"] = str(e)
        if st: st.error(f"[Tab {tab_id}] ❌ Error: {e}")