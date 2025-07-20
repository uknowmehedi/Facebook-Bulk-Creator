# Facebook Sign Up Automation using Playwright
# Uses mobile view, Gmail + OTP, and name/email from assets

import random
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# Constants
FB_SIGNUP_URL = "https://m.facebook.com/reg"
VIEWPORT = {"width": 412, "height": 915}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def load_names():
    with open("assets/names.json") as f:
        data = json.load(f)
    gender = random.choice(["male", "female"])
    name = random.choice(data[gender])
    return name, gender

def generate_dob():
    day = str(random.randint(1, 28))
    month = random.choice(MONTHS)
    year = str(random.randint(1988, 1998))
    return day, month, year

def generate_username(name):
    suffix = str(random.randint(10, 99))
    return f"{name.lower()}{suffix}"

def get_gmail():
    with open("assets/gmail_address.txt") as f:
        lines = f.readlines()
    line = random.choice(lines).strip()
    email, app_pw = line.split("|")
    return email.strip(), app_pw.strip()

def create_fb_account():
    name, gender = load_names()
    day, month, year = generate_dob()
    username = generate_username(name)
    password = "Fb@" + str(random.randint(10000000, 99999999))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=VIEWPORT)
        page = context.new_page()
        page.goto(FB_SIGNUP_URL)

        # Fill signup form
        page.fill('input[name="firstname"]', name)
        page.fill('input[name="lastname"]', name + "son")
        page.fill('input[name="reg_email__"]', f"{username}@gmail.com")
        page.fill('input[name="reg_passwd__"]', password)
        page.select_option('select[name="birthday_day"]', label=day)
        page.select_option('select[name="birthday_month"]', label=month)
        page.select_option('select[name="birthday_year"]', label=year)

        if gender == "male":
            page.check('input[value="2"]')
        else:
            page.check('input[value="1"]')

        page.click('button[name="websubmit"]')
        page.wait_for_timeout(5000)  # wait for redirection or OTP input

        print(f"🧠 Submitted for: {username}@gmail.com | DOB: {day}-{month}-{year} | Gender: {gender}")

        browser.close()

if __name__ == "__main__":
    create_fb_account()