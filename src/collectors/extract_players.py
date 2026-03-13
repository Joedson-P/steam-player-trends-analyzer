import requests
import pandas as pd
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('STEAM_API_KEY')

def get_player_count(app_id):
    url = f"http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['response'].get('player_count', 0)
    else:
        return 0
    
def collect_data():
    games = {
        '730': 'Counter-Strike 2',
        '578080': 'PUBG: Battlegrounds',
        '570': 'Dota 2',
        '1808500': 'ARC Raiders',
        '3764200': 'Resident Evil Requiem',
        '1086940': 'Baldur\'s Gate 3',
        '1091500': 'Cyberpunk 2077',
        '1097150': 'Elden Ring',
    }

    results = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for app_id, name in games.items():
        print(f"Coletando dados para {name}.")
        count = get_player_count(app_id)
        results.append({
            'timestamp': timestamp,
            'app_id': app_id,
            'game': name,
            'player_count': count
        })

    df = pd.DataFrame(results)

    db_path = Path(__file__).parent.parent.parent / 'data' / 'steam_data.db'

    try:
        conn = sqlite3.connect(db_path)
        df.to_sql('player_stats', conn, if_exists='append', index=False)
        conn.close()
        print(f"Dados salvos com sucesso às {timestamp}.")
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")

if __name__ == "__main__":
    collect_data()