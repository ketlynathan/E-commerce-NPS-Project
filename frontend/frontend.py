import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard NPS E-commerce",
    page_icon="📊",
    layout="wide"
)

# URL base do FastAPI
API_BASE_URL = "http://localhost:8000"

# Funções de requisição
def get_nps():
    """Busca os dados de NPS da API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/nps")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao buscar NPS: {e}")
        return None

def get_avaliacoes():
    """Busca todas as avaliações da API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/avaliacoes")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao buscar avaliações: {e}")
        return []

def processar_avaliacoes():
    """Processa avaliações pendentes usando Ollama."""
    try:
        with st.spinner("Processando avaliações com Ollama... Isso pode levar alguns minutos."):
            response = requests.post(f"{API_BASE_URL}/api/processar_avaliacoes")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Erro ao processar avaliações: {e}")
        return None

# CSS customizado para melhorar a aparência
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Barra Lateral
with st.sidebar:
    st.title("⚙️ Controles")
    st.markdown("---")
    
    if st.button("🤖 Rodar Análise de Sentimento (Ollama)", type="primary", use_container_width=True):
        resultado = processar_avaliacoes()
        if resultado:
            st.success(f"✅ Processadas: {resultado['total_processadas']} avaliações")
            st.info(f"Total pendentes: {resultado['total_pendentes']}")
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 Sobre o NPS")
    st.markdown("""
    **Net Promoter Score (NPS)**
    
    - 🟢 **Promotores** (9-10): Clientes entusiastas
    - 🟡 **Neutros** (7-8): Clientes satisfeitos mas não entusiastas
    - 🔴 **Detratores** (0-6): Clientes insatisfeitos
    
    **Fórmula:**  
    NPS = % Promotores - % Detratores
    
    **Interpretação:**
    - NPS > 50: Excelente
    - NPS 0-50: Bom
    - NPS < 0: Precisa melhorar
    """)

# Título Principal
st.title("📊 Dashboard NPS de E-commerce")
st.markdown("### Análise de Satisfação do Cliente com IA")
st.markdown("---")

# Buscar dados
nps_data = get_nps()
avaliacoes_data = get_avaliacoes()

if nps_data and nps_data['total_avaliacoes'] > 0:
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Determinar cor do NPS
        nps_score = nps_data['nps_score']
        if nps_score > 50:
            delta_color = "normal"
            emoji = "🎉"
        elif nps_score > 0:
            delta_color = "normal"
            emoji = "👍"
        else:
            delta_color = "inverse"
            emoji = "⚠️"
        
        st.metric(
            label=f"{emoji} NPS Score",
            value=f"{nps_score:.1f}",
            delta="Excelente" if nps_score > 50 else ("Bom" if nps_score > 0 else "Atenção"),
            delta_color=delta_color
        )
    
    with col2:
        st.metric(
            label="🟢 Promotores",
            value=nps_data['promotores'],
            delta=f"{nps_data['percentual_promotores']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="🟡 Neutros",
            value=nps_data['neutros'],
            delta=f"{nps_data['percentual_neutros']:.1f}%"
        )
    
    with col4:
        st.metric(
            label="🔴 Detratores",
            value=nps_data['detratores'],
            delta=f"{nps_data['percentual_detratores']:.1f}%",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Gráficos
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 Distribuição de Clientes")
        
        # Gráfico de Pizza
        labels = ['Promotores', 'Neutros', 'Detratores']
        values = [nps_data['promotores'], nps_data['neutros'], nps_data['detratores']]
        colors = ['#00CC66', '#FFD700', '#FF4444']
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.4,
            textinfo='label+percent',
            textfont_size=14
        )])
        
        fig_pie.update_layout(
            title_text="Categorias de Clientes",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_chart2:
        st.subheader("📊 Comparativo de Categorias")
        
        # Gráfico de Barras
        fig_bar = go.Figure(data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=colors,
                text=values,
                textposition='auto',
                textfont=dict(size=16, color='white')
            )
        ])
        
        fig_bar.update_layout(
            title_text="Quantidade por Categoria",
            xaxis_title="Categoria",
            yaxis_title="Quantidade de Clientes",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # Tabela de Avaliações
    st.subheader("📋 Avaliações Detalhadas")
    
    if avaliacoes_data:
        # Filtrar apenas avaliações processadas
        df = pd.DataFrame(avaliacoes_data)
        df_processadas = df[df['nota_llm'].notna()].copy()
        
        if not df_processadas.empty:
            # Adicionar categoria
            def categorizar(nota):
                if nota >= 9:
                    return "🟢 Promotor"
                elif nota >= 7:
                    return "🟡 Neutro"
                else:
                    return "🔴 Detrator"
            
            df_processadas['Categoria'] = df_processadas['nota_llm'].apply(categorizar)
            df_processadas['Nota'] = df_processadas['nota_llm']
            df_processadas['Avaliação'] = df_processadas['texto_avaliacao']
            
            # Selecionar colunas para exibição
            df_display = df_processadas[['id', 'Categoria', 'Nota', 'Avaliação']].sort_values('Nota', ascending=False)
            
            # Filtros
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                categoria_filter = st.multiselect(
                    "Filtrar por Categoria:",
                    options=["🟢 Promotor", "🟡 Neutro", "🔴 Detrator"],
                    default=["🟢 Promotor", "🟡 Neutro", "🔴 Detrator"]
                )
            
            with col_filter2:
                num_rows = st.slider("Número de linhas a exibir:", 10, 100, 50)
            
            # Aplicar filtro
            df_filtered = df_display[df_display['Categoria'].isin(categoria_filter)].head(num_rows)
            
            # Exibir tabela
            st.dataframe(
                df_filtered,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": st.column_config.NumberColumn("ID", width="small"),
                    "Categoria": st.column_config.TextColumn("Categoria", width="medium"),
                    "Nota": st.column_config.NumberColumn("Nota", width="small"),
                    "Avaliação": st.column_config.TextColumn("Avaliação", width="large")
                }
            )
            
            # Estatísticas adicionais
            st.markdown("---")
            st.subheader("📈 Estatísticas Adicionais")
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                media_nota = df_processadas['nota_llm'].mean()
                st.metric("Nota Média", f"{media_nota:.2f}")
            
            with col_stat2:
                total_processadas = len(df_processadas)
                total_avaliacoes = len(df)
                st.metric("Avaliações Processadas", f"{total_processadas}/{total_avaliacoes}")
            
            with col_stat3:
                pendentes = total_avaliacoes - total_processadas
                st.metric("Pendentes de Análise", pendentes)
        
        else:
            st.warning("⚠️ Nenhuma avaliação foi processada ainda. Clique no botão 'Rodar Análise de Sentimento' na barra lateral.")
    
else:
    st.warning("⚠️ Nenhum dado disponível. Execute o script fake_data.py para popular o banco de dados.")
    st.info("💡 Depois, clique no botão 'Rodar Análise de Sentimento' para processar as avaliações.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>Dashboard NPS E-commerce | Powered by FastAPI + Streamlit + Ollama 🚀</p>
    </div>
    """,
    unsafe_allow_html=True
)
