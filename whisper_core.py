import json
from datetime import datetime

DATA_FILE = "posts.json"

def load_posts():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_post(message):
    posts = load_posts()
    posts.append({
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(DATA_FILE, "w") as f:
        json.dump(posts, f, indent=2)

def delete_post(index):
    posts = load_posts()
    if 0 <= index < len(posts):
        del posts[index]
        with open(DATA_FILE, "w") as f:
            json.dump(posts, f, indent=2)
