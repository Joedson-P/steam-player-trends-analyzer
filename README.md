# Steam Trend Analyzer

Um dashboard inteligente de análise de dados em tempo real (ETL) que monitora o engajamento de jogadores na plataforma Steam utilizando Python, SQLite e Streamlit.

## Sobre o Projeto
Este projeto foi desenvolvido para coletar dados de jogadores simultâneos via **Steam Web API**, armazená-los de forma estruturada e gerar insights sobre o comportamento do mercado de games, como horários de pico e estabilidade de público.

## Tecnologias
* **Linguagem:** Python 3.12
* **Interface:** Streamlit (Layout responsivo com abas)
* **Banco de Dados:** SQLite3 (Migrado de CSV para melhor performance)
* **Visualização:** Plotly Express (Gráficos dinâmicos e interativos)
* **ETL:** Requests & Pandas

## Principais Funcionalidades
* **Monitoramento em Tempo Real:** Coleta automatizada de dados de jogadores.
* **Análise de Market Share:** Gráfico de rosca mostrando a dominância de títulos como CS2 e Dota 2.
* **Índice de Estabilidade:** Cálculo estatístico (Coeficiente de Variação) para identificar a fidelidade da base de jogadores.
* **Filtros Inteligentes:** Seleção de jogos e intervalos de datas granulares.

## Insights Extraídos (Exemplos)
* **PUBG:** Apresenta alta volatilidade (~60% de variação), indicando concentração em fusos horários específicos (Ásia).
* **Dota 2:** Base de jogadores mais estável e fiel, com menor variação diária.
* **Prime Time:** Identificação matemática do momento de maior tráfego global da plataforma.

## Como Executar
1. **Clone o repositório**: `git clone ...`
2. **Instale as dependências**: `pip install -r requirements.txt`
3. **Configure as credenciais**: 
    * Crie um arquivo `.env` na raiz do projeto.
    * Adicione sua chave da API da Steam: `STEAM_API_KEY=sua_chave_aqui`
4. Execute o coletor para alimentar o banco de dados SQLite: `python src/collectors/extract_players.py`
5. Execute o dashboard: `streamlit run src/app.py`

### _OBS: O projeto já inclui um snapshot de dados históricos para demonstração imediata na pasta `/data`._