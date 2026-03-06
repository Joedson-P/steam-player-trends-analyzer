import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(page_title="Steam Trend Analyzer", layout="wide")

st.title("Tendências na Steam")
st.subheader("Análise de engajamento de usuários na plataforma Steam.")

# Caminho para o arquivo CSV
data_path = Path(__file__).parent.parent / "data" / "player_history.csv"

if data_path.exists():
    df = pd.read_csv(data_path)

    # Converter timestamps para datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- SIDEBAR: Hierarquia ---
    st.sidebar.header("Painel de Controle")

    # 1. FILTROS
    all_games = df['game'].unique()
    selected_games = st.sidebar.multiselect("Selecione os jogos", all_games, default=all_games[:3])

    # Filtrando o df
    df_filtered = df[df['game'].isin(selected_games)]

    st.sidebar.divider()
    
    # 2. RECORDES
    st.sidebar.subheader("Recordes da Sessão")
    for game in enumerate(selected_games):
        game_history = df[df['game'] == game]
        if not game_history.empty:
            peak = game_history['player_count'].max()
            st.sidebar.write(f"**{game}**")
            st.sidebar.caption(f"Pico: {peak:,} jogadores")

    # --- MÉTRICAS COM DELTA ---
    st.subheader("Métricas de Engajamento")
    cols = st.columns(len(selected_games))

    for i, game in enumerate(selected_games):
        game_data = df[df['game'] == game].sort_values('timestamp')
        if len(game_data) >= 1:
            current = game_data.iloc[-1]['player_count']
            delta = current - game_data.iloc[-2]['player_count'] if len(game_data) > 1 else 0
            cols[i].metric(label=game, value=f"{current:,}", delta=f"{delta:,}")

    st.divider()

    # --- GRÁFICO DE SÉRIE TEMPORAL ---
    st.subheader("Evolução Temporal de Jogadores")
    if not df_filtered.empty:
        fig = px.line(df_filtered, x='timestamp', y='player_count', color='game',
                      labels={'player_count': 'Jogadores Online', 'timestamp': 'Horário'},
                      markers=True, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecione pelo menos um jogo no menu lateral.")

    # --- RANKING ATUAL ---
    st.subheader("Comparativo de Volume Atual")
    latest_data = df[df['timestamp'] == df['timestamp'].max()]
    fig_bar = px.bar(latest_data, x='player_count', y='game', orientation='h', 
                     color='player_count', color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Arquivo de dados não encontrado.")