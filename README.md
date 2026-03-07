# Steam Player Trends Analyzer

Sistema automatizado de monitoramento e visualização de dados em tempo real da Steam Web API.

## Funcionalidades
- **Coleta Automatizada**: Script em Python que consulta a API da Steam a cada 30 minutos.
- **Dashboard Interativo**: Interface construída em Streamlit com gráficos dinâmicos (Plotly).
- **Análise de Tendências**: Monitoramento de picos de jogadores, deltas de variação e recordes de sessão.
- **Segurança**: Gestão de credenciais via variáveis de ambiente (`.env`).

## Tecnologias
- **Python 3.12**
- **Pandas & Plotly**: Processamento e Visualização
- **Streamlit** Interface Web
- **Steam Web API**: Fonte de Dados

## Estrutura
`src/collectors`: Scripts de mineração.  
`src/app.py`: Interface do dashboard.  
`run_collector.py`: Script de coleta de dados.