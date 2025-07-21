import os

GMAIL_FILE = "assets/gmail_address.txt"
USED_FILE = "assets/used_gmails.txt"
FAILED_FILE = "assets/failed_gmails.txt"

def load_emails():
    if not os.path.exists(GMAIL_FILE):
        return []
    with open(GMAIL_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def mark_email(email_line, status="used"):
    path = USED_FILE if status == "used" else FAILED_FILE
    with open(path, "a") as f:
        f.write(email_line + "\n")
    if os.path.exists(GMAIL_FILE):
        lines = load_emails()
        with open(GMAIL_FILE, "w") as f:
            for l in lines:
                if l != email_line:
                    f.write(l + "\n")