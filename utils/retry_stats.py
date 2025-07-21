import json, os
STATS_FILE = "logs/retry_stats.json"

def init_stats():
    return {
        "signup": {"success": 0, "failure": 0, "last_error": ""},
    }

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE) as f:
            return json.load(f)
    return init_stats()

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

def reset_stats():
    if os.path.exists(STATS_FILE):
        os.remove(STATS_FILE)
