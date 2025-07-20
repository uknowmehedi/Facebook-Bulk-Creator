
# Gmail OTP Reader
# Connects to Gmail via IMAP to fetch OTP from unread messages

import imaplib
import email
import time
import re
from datetime import datetime, timedelta

# Cache to store recently used OTPs to avoid duplicates
otp_cache = {}

def read_latest_otp(gmail_address, app_password, delay_seconds=20, otp_regex=r"code is (\d{6})"):
    try:
        # Connect securely to Gmail IMAP server
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(gmail_address, app_password)

        # Try selecting the Inbox, fallback to All Mail
        try:
            mail.select("inbox")
        except:
            mail.select('"[Gmail]/All Mail"')

        # Search for unseen (unread) emails with subject "Facebook"
        result, data = mail.search(None, '(UNSEEN SUBJECT "Facebook")')
        if result != "OK":
            print("❌ Failed to search inbox.")
            return None

        mail_ids = data[0].split()
        if not mail_ids:
            print("📭 No new OTP emails found.")
            return None

        # Get the most recent email ID
        latest_id = mail_ids[-1]
        result, data = mail.fetch(latest_id, "(RFC822)")
        if result != "OK":
            print("❌ Failed to fetch email.")
            return None

        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Extract plain text body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        # Use regex to extract OTP code
        match = re.search(otp_regex, body)
        if match:
            otp = match.group(1)

            # Skip OTP if used too recently (cached)
            if otp in otp_cache and datetime.now() - otp_cache[otp] < timedelta(seconds=delay_seconds):
                print("⏳ OTP recently used, skipping duplicate.")
                return None

            otp_cache[otp] = datetime.now()

            # Mark email as seen so it's not reused again
            mail.store(latest_id, '+FLAGS', '\\Seen')

            print(f"✅ OTP found: {otp}")
            return otp
        else:
            print("❌ No OTP found in email.")
            return None

    except Exception as e:
        print(f"⚠️ Error reading OTP: {e}")
        return None