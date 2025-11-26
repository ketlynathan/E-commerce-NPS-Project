## 🚀 Desafio Prático: Calculando NPS com IA Local e Stack Python

### **Objetivo Final**

Construir um sistema completo de ponta a ponta (Full-Stack) em Python para calcular o **Net Promoter Score (NPS)** de um e-commerce de roupas femininas. A análise de sentimento das avaliações dos clientes será realizada por um **modelo de Linguagem Grande (LLM)** local usando **Ollama**.

### **📚 Tecnologias a Serem Utilizadas**

  * **Linguagem Principal:** Python
  * **Banco de Dados:** SQLite
  * **ORM:** SQLAlchemy
  * **Backend (API):** FastAPI
  * **Análise de Sentimento (IA):** Ollama Client (conectado a um modelo pequeno, ex: Phi-3)
  * **Frontend (Dashboard):** Streamlit
  * **Utilitários:** Faker, Pandas, Requests

-----

## Passo 1: Configuração do Ambiente e Setup Inicial

### 1.1. Estrutura do Projeto

Crie a seguinte estrutura de diretórios:

```
ecommerce_nps/
├── data/
├── backend/
│   ├── backend.py
│   └── fake_data.py
├── frontend/
│   └── frontend.py
└── requirements.txt
```

### 1.2. Instalação de Dependências

Crie o arquivo `requirements.txt` e instale as dependências:

  * **Tarefa:** Complete o `requirements.txt` com todas as bibliotecas necessárias para rodar o projeto.

### 1.3. Configuração do Ollama (Requisito Prévio)

O aluno deve ter o Ollama instalado (via WSL/Docker ou nativo) e um modelo pequeno baixado (ex: `phi3:mini`).

  * **Instrução:** Garanta que o serviço Ollama esteja em execução em `http://localhost:11434` e que você tenha um modelo instalado via `ollama run <modelo>`.

-----

## Passo 2: Backend - Modelos e Geração de Dados

### 2.1. Criação do Banco de Dados e Modelos (Em `backend/backend.py`)

  * **Tarefa 2.1.1 (Configuração ORM):** Configure o **SQLAlchemy** para se conectar ao banco **SQLite** em `./data/ecommerce_nps.db`.
  * **Tarefa 2.1.2 (Modelo `Avaliacao`):** Crie o modelo ORM `Avaliacao` com os campos:
      * `id`: `Integer`, Primary Key.
      * `texto_avaliacao`: `String`.
      * `nota_llm`: `Integer` (Aceita valores **nulos** inicialmente, de 0 a 10).
  * **Tarefa 2.1.3 (Função de Setup):** Crie a função `create_db_and_tables()` para inicializar o banco e as tabelas, se elas não existirem.

### 2.2. Geração de Dados Falsos (Em `backend/fake_data.py`)

  * **Tarefa 2.2.1 (Faker):** Use a biblioteca **Faker** para gerar 1000 registros de avaliações.
  * **Tarefa 2.2.2 (Textos):** Crie uma lista de frases de roupas femininas que misturem sentimentos positivos, neutros e negativos. Use `Faker` para gerar dados de contexto e persistir 1000 novas `Avaliacao` no banco.
  * **Tarefa 2.2.3 (Estado Inicial):** Garanta que, ao inserir os dados, a coluna `nota_llm` seja **NULA** para que o próximo passo possa processá-las.

-----

## Passo 3: Backend - API e Integração com IA

### 3.1. Integração com Ollama (Em `backend/backend.py`)

  * **Tarefa 3.1.1 (Função LLM):** Crie a função assíncrona `get_ollama_sentiment_score(text: str) -> int`.
      * Use a biblioteca `ollama` para fazer uma requisição.
      * Crie um **prompt conciso** que instrua o LLM a retornar **APENAS UM NÚMERO INTEIRO de 0 a 10** para a satisfação do cliente.
      * Implemente o *parsing* e o tratamento de erros para garantir que a função retorne um `int` ou um valor padrão (ex: 0) em caso de falha de conexão.

### 3.2. Rotas FastAPI

  * **Tarefa 3.2.1 (Rota de Processamento - `POST /api/processar_avaliacoes`):**
    1.  Busque todas as avaliações onde `nota_llm` é `NULL`.
    2.  Itere sobre essas avaliações e chame a função `get_ollama_sentiment_score()`.
    3.  **Atualize** o registro no banco com a nota recebida do LLM.
    4.  Retorne o número de avaliações processadas.
  * **Tarefa 3.2.2 (Rota de Dados - `GET /api/avaliacoes`):**
    1.  Retorne todas as avaliações no banco.
  * **Tarefa 3.2.3 (Rota NPS - `GET /api/nps`):**
    1.  Consulte o banco para obter todas as `nota_llm`.
    2.  **Classifique** os clientes:
          * **Promotores (P):** Notas $9 \le \text{Nota} \le 10$
          * **Neutros (N):** Notas $7 \le \text{Nota} \le 8$
          * **Detratores (D):** Notas $0 \le \text{Nota} \le 6$
    3.  Calcule o **NPS** usando a fórmula:
        $$NPS = \left( \frac{\text{Total P}}{\text{Total Clientes}} - \frac{\text{Total D}}{\text{Total Clientes}} \right) \times 100$$
    4.  Retorne a contagem de P, N, D, o total e o `nps_score`.

-----

## Passo 4: Frontend - Dashboard Streamlit

Crie o arquivo `frontend/frontend.py` para construir o painel de visualização.

### 4.1. Layout e Interação

  * **Tarefa 4.1.1 (Conexão):** Defina a URL base da API do FastAPI.
  * **Tarefa 4.1.2 (Botão de Análise):** No *sidebar* ou no topo da página, crie um botão **"EXECUTAR ANÁLISE DE SENTIMENTO (Ollama)"**. Ao ser clicado, ele deve chamar a rota `POST /api/processar_avaliacoes` e, em seguida, recarregar os dados.

### 4.2. Visualização de Métricas

  * **Tarefa 4.2.1 (Métricas Principais):**
      * Use `st.metric` para exibir em destaque o valor do **NPS Score** (com cores condicionais, se possível).
      * Exiba o total de Promotores, Neutros e Detratores em colunas separadas.

### 4.3. Gráfico de Distribuição

  * **Tarefa 4.3.2 (Gráfico):** Usando **Pandas** e **Plotly** (ou `st.bar_chart`), crie um gráfico que ilustre a distribuição percentual dos clientes (P, N, D). Este gráfico é crucial para visualizar a composição do NPS.

### 4.4. Tabela de Dados

  * **Tarefa 4.4.3 (Tabela):** Exiba uma tabela paginada (`st.dataframe`) com as colunas: `ID`, `Texto da Avaliação` e `Nota LLM`.

-----

## Instruções de Lançamento

1.  Rode o script de geração de dados: `python backend/fake_data.py`
2.  Inicie o servidor FastAPI: `uvicorn backend.backend:app --reload`
3.  Inicie o Dashboard Streamlit: `streamlit run frontend/frontend.py`
4.  No Dashboard, clique no botão para rodar a análise de sentimento (que irá chamar o Ollama) e observe o NPS ser calculado\!