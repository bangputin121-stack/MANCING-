import json
import os

class Database:
    def __init__(self, db_file='database.json'):
        self.db_file = db_file
        # Membuat file database.json jika belum ada
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)

    def load_data(self):
        try:
            with open(self.db_file, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=4)

    def get_user(self, user_id):
        data = self.load_data()
        u_id = str(user_id)
        if u_id not in data:
            # Data awal buat member baru
            data[u_id] = {
                "balance": 0,
                "joran": "Bambu Biasa",
                "umpan": "Cacing"
            }
            self.save_data(data)
        return data[u_id]

    def update_user(self, user_id, key, value):
        data = self.load_data()
        u_id = str(user_id)
        if u_id in data:
            data[u_id][key] = value
            self.save_data(data)
