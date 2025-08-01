import json
from datetime import datetime

LOG_FILE = "analytics.json"

def track_interaction(model, prompt, response):
    """Log user interactions with timestamp."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "prompt": prompt,
        "response": response,
    }
    try:
        with open(LOG_FILE, "r", encoding='utf-8') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    except json.JSONDecodeError:
        logs = []

    logs.append(log_entry)

    try:
        with open(LOG_FILE, "w", encoding='utf-8') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error saving to analytics log: {e}")

def get_analytics():
    """Retrieve analytics data."""
    try:
        with open(LOG_FILE, "r", encoding='utf-8') as f:
            logs = json.load(f)
        return logs
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error reading analytics file - corrupted JSON")
        return []