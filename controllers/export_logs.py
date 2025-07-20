# Export results to JSON
# Logs created/failed accounts and used emails into timestamped files

import json
from datetime import datetime
from pathlib import Path

# Directory where logs will be stored
EXPORT_DIR = Path("logs")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def export_results(success_list, failed_list, used_emails=None):
    # Generate timestamp to create unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # File paths for saving
    success_path = EXPORT_DIR / f"success_accounts_{timestamp}.json"
    failed_path = EXPORT_DIR / f"failed_accounts_{timestamp}.json"
    email_path = EXPORT_DIR / f"used_emails_{timestamp}.json"

    # Save successful accounts
    with open(success_path, "w") as f:
        json.dump(success_list, f, indent=4)

    # Save failed attempts
    with open(failed_path, "w") as f:
        json.dump(failed_list, f, indent=4)

    # Save used emails if provided
    if used_emails:
        with open(email_path, "w") as f:
            json.dump(used_emails, f, indent=4)

    # Return paths for confirmation or GUI use
    return success_path, failed_path, email_path if used_emails else None
