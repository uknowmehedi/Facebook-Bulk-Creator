import random
from pathlib import Path

# Path to the file containing Gmail address and App Passwords
GMAIL_FILE = Path("assets/gmail_address.txt")

# Path to the file that stores used email-password pairs
USED_FILE = Path("assets/used_gmail.txt")


def load_all_gmails():
    """
    Loads all available Gmail credentials from the file,
    excluding those already marked as used.
    """
    # Read all lines with valid format from gmail_address.txt
    with open(GMAIL_FILE, "r") as f:
        lines = [line.strip() for line in f if "|" in line]

    # Load already used credentials
    used = set()
    if USED_FILE.exists():
        with open(USED_FILE, "r") as f:
            used = set(line.strip() for line in f)

    # Filter out used ones
    available = [line for line in lines if line not in used]
    return available


def get_random_email():
    """
    Returns a random unused Gmail address and app password.
    Raises an error if none are left.
    """
    available = load_all_gmails()
    if not available:
        raise Exception("❌ No unused Gmail accounts left!")

    # Choose a random unused email-password pair
    line = random.choice(available)
    email, app_pw = line.split("|")
    return email.strip(), app_pw.strip()


def mark_email_used(email, app_pw):
    """
    Marks the given email-password pair as used
    by appending it to used_gmail.txt.
    """
    with open(USED_FILE, "a") as f:
        f.write(f"{email}|{app_pw}\n")