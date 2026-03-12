import json
import os

class Database:  # <--- PASTIKAN TULISAN INI ADA DAN HURUF 'D' BESAR
    def __init__(self, filename="players.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_player(self, user_id):
        data = self.load_data()
        uid = str(user_id)
        if uid not in data:
            data[uid] = {
                "username": "Angler",
                "coins": 500,
                "xp": 0,
                "level": 1,
                "stamina": 100,
                "joran": "Bambu",
                "inventory": [],
                "last_daily": ""
            }
            self.save_data(data)
        return data[uid]

    def update_player(self, user_id, player_data):
        data = self.load_data()
        data[str(user_id)] = player_data
        self.save_data(data)
