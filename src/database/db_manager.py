import sqlite3
import pandas as pd
from pathlib import Path

def migrate_csv_to_sqlite(csv_path, db_path):
    if Path(csv_path).exists():
        df = pd.read_csv(csv_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        conn = sqlite3.connect(db_path)
        df.to_sql('player_stats', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Migração concluída: {len(df)} registros movidos para o banco de dados.")
    else:
        print("Arquivo CSV não encontrado.")

if __name__ == "__main__":
    CSV_FILE = Path(__file__).parent.parent.parent / 'data' / 'player_history.csv'
    DB_FILE = Path(__file__).parent.parent.parent / 'data' / 'steam_data.db'
    migrate_csv_to_sqlite(CSV_FILE, DB_FILE)