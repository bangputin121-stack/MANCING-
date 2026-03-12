import json
import os

class Database:
    def __init__(self, filename="database.json"):
        self.filename = filename
        self.data = self.load()

    def load(self):
        # Cek jika file database ada, jika tidak buat baru
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        # Simpan data ke file JSON
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get_player(self, user_id):
        user_id = str(user_id)
        
        # Jika user belum ada, buat data default
        if user_id not in self.data:
            self.data[user_id] = {
                "inventory": [],
                "balance": 0,
                "rod": "Bambu",
                "xp": 0,
                "level": 1,
                "last_fishing": 0
            }
            self.save()
        
        # LOGIKA UPDATE: Pastikan pemain lama juga punya kolom XP dan Level
        player = self.data[user_id]
        if "xp" not in player:
            player["xp"] = 0
        if "level" not in player:
            player["level"] = 1
            
        return player

    def update_player(self, user_id, player_data):
        # Update data pemain dan simpan
        user_id = str(user_id)
        self.data[user_id] = player_data
        self.save()
