# Automation logic using Playwright
# Handles multi-tab Facebook signup with OTP verification (simulated version)

import time
import random
import logging
from controllers.gmail_otp_reader import read_latest_otp

def start_account_creation(headless=True, max_tabs=5, max_attempts=3, delay=30, fallback_enabled=True):
    logging.info(f"🧠 Starting Account Creation Process")
    logging.info(f"Headless: {headless}, Max Tabs: {max_tabs}, Max Attempts: {max_attempts}, Delay: {delay}, Fallback: {fallback_enabled}")

    created_accounts = []
    failed_accounts = []

    # Gmail credentials (placeholder for demonstration)
    gmail_address = "example@gmail.com"
    app_password = "abcd efgh ijkl mnop"

    for tab in range(1, max_tabs + 1):
        logging.info(f"🌐 Launching tab {tab} {'(headless)' if headless else '(visible)'}...")
        time.sleep(1)  # Simulated loading delay

        attempt = 0
        success = False

        while attempt < max_attempts and not success:
            attempt += 1
            logging.info(f"🔄 Attempt {attempt} for Tab {tab}")
            time.sleep(delay / 10)  # Simulated delay

            # OTP verification from Gmail
            otp = read_latest_otp(gmail_address, app_password)
            if otp:
                acc_name = f"user{otp}"
                created_accounts.append(acc_name)
                logging.info(f"✅ Account '{acc_name}' created successfully in Tab {tab} with OTP {otp}")
                success = True
            else:
                logging.warning("❌ OTP verification failed – retrying...")

        # Fallback logic
        if not success and fallback_enabled:
            logging.info(f"🧪 Fallback activated for Tab {tab}")
            fallback_success = random.choice([True, False])
            if fallback_success:
                acc_name = f"userfb{random.randint(1000,9999)}"
                created_accounts.append(acc_name)
                logging.info(f"✅ Fallback account '{acc_name}' created")
            else:
                failed_accounts.append(f"Tab {tab}")
                logging.error(f"❌ Fallback failed for Tab {tab}")

    logging.info(f"🎯 Summary: {len(created_accounts)} Success | {len(failed_accounts)} Failed")
    
    # Export results
    from controllers.export_logs import export_results
    export_results(created_accounts, failed_accounts)

    return created_accounts, failed_accounts