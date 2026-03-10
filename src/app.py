import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Steam Trend Analyzer", layout="wide")

st.title("Tendências na Steam")
st.subheader("Análise de engajamento de usuários na plataforma Steam.")

# Caminho para o database
db_path = Path(__file__).parent.parent / "data" / "steam_data.db"

def load_data_from_db(path):
    conn = sqlite3.connect(path)
    query = "SELECT * FROM player_stats"
    df_db = pd.read_sql(query, conn)
    conn.close()

    # Converter timestamps para datetime
    df_db['timestamp'] = pd.to_datetime(df_db['timestamp'])
    return df_db

if db_path.exists():
    df = load_data_from_db(db_path)

    # Cálculo de insihgt global
    total_by_time = df.groupby('timestamp')['player_count'].sum().reset_index()
    peak_moment = total_by_time.loc[total_by_time['player_count'].idxmax()]
    st.info(f"O pico de engajamento global nesta sessão foi em **{peak_moment['timestamp'].strftime('%d/%m %H:%M')}** com **{peak_moment['player_count']:,}** jogadores combinados.")

    # --- SIDEBAR: Hierarquia ---
    st.sidebar.header("Painel de Controle")

    # 1. FILTROS
    all_games = df['game'].unique()
    selected_games = st.sidebar.multiselect("Selecione os jogos", all_games, default=all_games[:3])

    # Filtrando o df
    df_filtered = df[df['game'].isin(selected_games)]

    st.sidebar.divider()

    # Filtro de data
    st.sidebar.subheader("Período de Análise")

    min_date = df['timestamp'].min().date()
    max_date = df['timestamp'].max().date()

    start_date, end_date = st.sidebar.date_input(
        "Selecione o intervalo",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    df_filtered = df_filtered[
        (df_filtered['timestamp'].dt.date >= start_date) & 
        (df_filtered['timestamp'].dt.date <= end_date)
    ]

    st.sidebar.divider()
    
    # 2. RECORDES
    st.sidebar.subheader("Recordes da Sessão")
    for game in selected_games:
        game_history = df[df['game'] == game]
        if not game_history.empty:
            peak = game_history['player_count'].max()
            st.sidebar.write(f"**{game}**")
            st.sidebar.caption(f"Pico: {peak:,} jogadores")
        else:
            st.sidebar.caption(f"Sem dados para {game}")

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
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("Selecione pelo menos um jogo no menu lateral.")

    # --- RANKING ATUAL ---
    st.subheader("Comparativo de Volume Atual")
    latest_data = df[df['timestamp'] == df['timestamp'].max()]
    fig_bar = px.bar(latest_data, x='player_count', y='game', orientation='h', 
                     color='player_count', color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, width='stretch')

else:
    st.error("Arquivo de dados não encontrado.")