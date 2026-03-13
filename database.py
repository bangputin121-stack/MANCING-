import json
import os

DB_FILE = 'database.json'

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_data(user_id):
    data = load_data()
    user_id = str(user_id)
    if user_id not in data:
        # Data default buat member baru
        data[user_id] = {
            "balance": 0,
            "joran": "Bambu Biasa",
            "umpan": "Cacing",
            "inventory": ["Bambu Biasa", "Cacing"]
        }
        save_data(data)
    return data[user_id]

def update_user_data(user_id, key, value):
    data = load_data()
    user_id = str(user_id)
    if user_id in data:
        data[user_id][key] = value
        save_data(data)
