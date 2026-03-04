import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('11A74229580C2F7CD3B416EA4CAEC081')

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

    output_path = 'data\player_history.csv'

    if os.path.exists(output_path):
        df.to_csv(output_path, mode='a', header=False, index=False)
    else:
        df.to_csv(output_path, index=False)

if __name__ == "__main__":
    collect_data()