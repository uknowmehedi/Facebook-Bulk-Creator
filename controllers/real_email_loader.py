import random
from pathlib import Path
from dashboard import log_message  # Import from your GUI file

# Paths to data files
GMAIL_FILE = Path("assets/gmail_address.txt")
USED_FILE = Path("assets/used_gmail.txt")


def load_all_gmails():
    """
    Returns all available Gmail credentials,
    excluding those already used.
    """
    with open(GMAIL_FILE, "r") as f:
        lines = [line.strip() for line in f if "|" in line]

    used = set()
    if USED_FILE.exists():
        with open(USED_FILE, "r") as f:
            used = set(line.strip() for line in f)

    available = [line for line in lines if line not in used]
    return available


def get_random_email():
    """
    Picks a random unused Gmail address and app password.
    """
    available = load_all_gmails()
    if not available:
        raise Exception("❌ No unused Gmail accounts left!")

    line = random.choice(available)
    email, app_pw = line.split("|")
    return email.strip(), app_pw.strip()


def mark_email_used(email, app_pw):
    """
    Marks a Gmail account as used.
    """
    entry = f"{email}|{app_pw}"
    if USED_FILE.exists():
        with open(USED_FILE, "r") as f:
            used = set(line.strip() for line in f)
        if entry in used:
            return  # Already marked

    with open(USED_FILE, "a") as f:
        f.write(f"{entry}\n")


def reset_used_emails():
    """
    Clears the used_gmail.txt file, resetting usage.
    """
    if USED_FILE.exists():
        USED_FILE.unlink()
        log_message("🔄 All used emails have been reset.")
    else:
        log_message("⚠️ No used email file found to reset.")


def get_email_usage_stats():
    """
    Displays count of total, used, and unused Gmail accounts.
    """
    total = 0
    used = 0
    available = 0

    if GMAIL_FILE.exists():
        with open(GMAIL_FILE, "r") as f:
            total = len([line for line in f if "|" in line])

    if USED_FILE.exists():
        with open(USED_FILE, "r") as f:
            used = len([line for line in f if "|" in line])

    available = max(total - used, 0)

    log_message(f"📧 Total Emails:     {total}")
    log_message(f"✅ Used Emails:      {used}")
    log_message(f"🟢 Unused Available: {available}")

    return total, used, available