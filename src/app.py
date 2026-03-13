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

    # --- ESTRUTURA DE ABAS ---
    tab1, tab2, tab3 = st.tabs([
        "Evolução Temporal",
        "Comparativo de Volume",
        "Informações de Mercado"
    ])

    # --- ABA 1: EVOLUÇÃO TEMPORAL ---
    with tab1:
        st.subheader("Métricas de Engajamento")
        cols = st.columns(len(selected_games))

        for i, game in enumerate(selected_games):
            game_data = df[df['game'] == game].sort_values('timestamp')
            if len(game_data) >= 1:
                current = game_data.iloc[-1]['player_count']
                delta = current - game_data.iloc[-2]['player_count'] if len(game_data) > 1 else 0
                cols[i].metric(label=game, value=f"{current:,}", delta=f"{delta:,}")

        st.divider()

        st.subheader("Série Temporal de Jogadores")
        if not df_filtered.empty:
            fig = px.line(df_filtered, x='timestamp', y='player_count', color='game',
                        labels={'player_count': 'Jogadores Online', 'timestamp': 'Horário'},
                        markers=True, template="plotly_dark")
            st.plotly_chart(fig, width='stretch')
        else:
            st.warning("Selecione pelo menos um jogo no menu lateral.")

    # --- ABA 2: COMPARATIVO DE VOLUME ---
    with tab2:
        st.subheader("_Market Share_ e Volume Atual")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Ranking por Volume Atual**")
            latest_data = df[df['timestamp'] == df['timestamp'].max()]
            fig_bar = px.bar(latest_data, x='player_count', y='game', orientation='h', 
                            color='player_count', color_continuous_scale='Viridis')
            st.plotly_chart(fig_bar, width='stretch')

        with col2:
            st.write("**Participação Média no Período**")
            df_share = df_filtered.groupby('game')['player_count'].mean().reset_index()
            fig_pie = px.pie(df_share, values='player_count', names='game', hole=0.4)
            st.plotly_chart(fig_pie, width="stretch")

    with tab3:
        st.subheader("Análise de Horário Nobre")

        total_by_time = df_filtered.groupby('timestamp')['player_count'].sum().reset_index()
        if not total_by_time.empty:
            peak_moment = total_by_time.loc[total_by_time['player_count'].idxmax()]

            st.info(f"**Insight:** O pico de engajamento no período selecionado foi em "
                    f"**{peak_moment['timestamp'].strftime('%D/%M %H:%M')}** com "
                    f"**{peak_moment['player_count']:,}** jogadores combinados.")
            
            fig_area = px.area(total_by_time, x='timestamp', y='player_count',
                               title="Volume Total Acumulado",
                               color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig_area, width='stretch')

        st.divider()

        st.subheader("Índice de Estabilidade do Público")
        st.caption("Mede a variação entre o pico e a média.")

        estabilidade_lista = []

        for game in selected_games:
            stats = df_filtered[df_filtered['game'] == game]['player_count'].agg(['mean', 'std', 'min', 'max'])
            if stats['mean'] > 0:
                cv = (stats['std'] / stats['mean']) * 100
                estabilidade_lista.append({
                    "Jogo": game,
                    "Média": f"{int(stats['mean']):,}",
                    "Pico": f"{int(stats['max']):,}",
                    "Variação": round(cv, 2)
                })

        df_estabilidade = pd.DataFrame(estabilidade_lista).sort_values("Variação")

        st.table(df_estabilidade)

        st.info("""
        **Como ler este índice:**
        - **Variação Baixa (< 20%):** Público constante (provavelmente jogadores de várias regiões do mundo).
        - **Variação Alta (> 50%):** Público muito concentrado em um fuso horário.
        """)

else:
    st.error("Arquivo de dados não encontrado.")