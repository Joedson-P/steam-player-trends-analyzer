import time
import subprocess
import sys

def start_automated_collector():
    print("Iniciando coleta de dados automática.")
    try:
        while True:
            subprocess.run([sys.executable, 'src/collectors/extract_players.py'])
            print(f"Aguardando próxima coleta... {time.strftime('%H:%M:%S')}")
            time.sleep(1800)
    except KeyboardInterrupt:
        print("\n Coleta automatizada interrompida pelo usuário.")

if __name__ == "__main__":
    start_automated_collector()