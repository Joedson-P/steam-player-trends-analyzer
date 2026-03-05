import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Steam Trend Analyzer", layout="wide")

st.title("Análises de Tendências na Steam")
st.subheader("Análise de engajamento de usuários na plataforma Steam")

# Caminho para o arquivo CSV
data_path = Path(__file__).parent.parent / "data" / "player_history.csv"

if data_path.exists():
    df = pd.read_csv(data_path)

    # Converter timestamps para datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Métricas de destaque
    latest_timestamp = df['timestamp'].max()
    latest_data = df[df['timestamp'] == latest_timestamp]

    col1, col2, col3 = st.columns(3)

    with col1:
        most_played = latest_data.loc[latest_data['player_count'].idxmax()]
        st.metric(label="Jogo com mais jogadores", value=most_played['game'], delta=f"{most_played['player_count']:,}")

    with col2:
        total_players = latest_data['player_count'].sum()
        st.metric(label="Total de jogadores ativos", value=f"{total_players:,}")

    with col3:
        st.write(f"Última atualização: {latest_timestamp.strftime('%H-%M-%S')}")

    # Gráfico Ranking Atual
    st.write("### Ranking do número de jogadores")
    chart_data = latest_data.sort_values(by='player_count', ascending=True)
    st.bar_chart(chart_data, x='game', y='player_count', color="#2FEF21")

    with st.expander("Ver dados brutos"):
        st.dataframe(df.sort_values(by='timestamp', ascending=False), use_container_width=True)

else:
    st.error("Arquivo de dados não encontrado. Rode o script de extração primeiro!")