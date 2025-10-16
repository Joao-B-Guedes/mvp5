import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(
    page_title="Sistema de Matrículas Escolares",
    page_icon="📊",
    layout="wide"
)

# Carregar dataset
@st.cache_data
def carregar_dados(name):
    df = pd.read_csv(name)
    return df

df = carregar_dados("dados_matriculas.csv")

# Sidebar com os índices como radio buttons (todos visíveis)
st.sidebar.title("📋 **Menu de Navegação**")
st.sidebar.markdown("---")

# Lista de páginas
pages = [
    "🏠 Apresentação do Projeto",
    "📈 Dashboard Regional",
    "🏫 Dashboard por Escola",
    "🏛️ Dashboard por Superintendência",
    "💾 Base de dados",
    "🚀 Próximas Etapas",
    "👨‍💻 Desenvolvedor"
]

# Seleção da página com radio buttons (todos itens visíveis e clicáveis)
selected_page = st.sidebar.radio(
    "Escolha uma seção:",
    options=pages,
    index=0,
    help="Clique na opção desejada para navegar"
)

# FILTROS GLOBAIS (apenas Ano mantido na sidebar, Região removido)
st.sidebar.markdown("---")
st.sidebar.header("🔍 **Filtros Globais**")

ano_selecionado = st.sidebar.multiselect(
    "Selecionar Ano de Matrícula",
    options=df["Ano_Matricula"].unique(),
    default=df["Ano_Matricula"].unique()
)

# Aplicar filtro global de Ano
df_filtrado_global = df[
    df["Ano_Matricula"].isin(ano_selecionado)
]

# === FUNÇÕES DAS PÁGINAS ===

def mostrar_apresentacao():
    st.title("🏠 **Apresentação do Projeto**")
    st.markdown("""
    ## 📋 **Sistema de Análise de Matrículas Escolares**
    
    **Objetivo:** Monitorar e analisar indicadores de matrículas por região, escola e superintendência.
    
    ## 📊 **Escopo**
    | Módulo | Descrição | Status |
    |--------|-----------|--------|
    | Regional | Visão por estado/região | ✅ |
    | Por Escola | Detalhamento por unidade | ✅ |
    | Superintendência | Análise por agrupamento | ✅ |
    
    ## 🛠️ **Tecnologias**
    - **Frontend:** Streamlit + Plotly
    - **Backend:** Python + Pandas
    - **Dados:** CSV
    
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Escolas", len(df_filtrado_global["Nome_Unidade_Escolar"].unique()))
    with col2:
        st.metric("Regiões", len(df_filtrado_global["Regiao"].unique()))
    with col3:
        st.metric("Superintendências", len(df_filtrado_global["Superintendencia"].unique()))
    with col4:
        st.metric("Total Matrículas", f"{df_filtrado_global['Numero_Matriculas'].sum():,.0f}")

def mostrar_regional():
    st.title("📈 **Dashboard Regional**")
    
    # FILTRO DE REGIÃO MOVIDO PARA ESTA PÁGINA
    regiao_selecionada = st.multiselect(
        "Selecionar Região",
        options=df_filtrado_global["Regiao"].unique(),
        default=df_filtrado_global["Regiao"].unique(),
        key="regiao_regional"
    )
    
    df_filtrado_regional = df_filtrado_global[
        df_filtrado_global["Regiao"].isin(regiao_selecionada)
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("**Matrículas por Região**")
        matriculas_por_regiao = df_filtrado_regional.groupby("Regiao")["Numero_Matriculas"].sum().reset_index()
        fig_regiao = px.bar(
            matriculas_por_regiao,
            x="Regiao", y="Numero_Matriculas",
            title="Total de Matrículas por Região",
            labels={"Regiao": "Região", "Numero_Matriculas": "Número de Matrículas"},
            color="Regiao"
        )
        st.plotly_chart(fig_regiao, use_container_width=True)
    
    with col2:
        st.subheader("**Matrículas por Estado**")
        matriculas_por_estado = df_filtrado_regional.groupby("Estado")["Numero_Matriculas"].sum().reset_index()
        fig_estado = px.bar(
            matriculas_por_estado,
            x="Estado", y="Numero_Matriculas",
            title="Total de Matrículas por Estado",
            labels={"Estado": "Estado", "Numero_Matriculas": "Número de Matrículas"},
            color="Estado"
        )
        st.plotly_chart(fig_estado, use_container_width=True)

def mostrar_escola():
    st.title("🏫 **Dashboard por Escola**")
    
    # FILTRO DE REGIÃO MOVIDO PARA ESTA PÁGINA
    regiao_selecionada = st.multiselect(
        "Selecionar Região",
        options=df_filtrado_global["Regiao"].unique(),
        default=df_filtrado_global["Regiao"].unique(),
        key="regiao_escola"
    )
    
    df_filtrado_escola = df_filtrado_global[
        df_filtrado_global["Regiao"].isin(regiao_selecionada)
    ]
    
    # FILTRO ESPECÍFICO DESTA PÁGINA
    col1, col2 = st.columns([2, 1])
    with col1:
        tipo_unidade_selecionado = st.multiselect(
            "Filtrar por Tipo de Unidade Escolar",
            options=df_filtrado_escola["Tipo_Unidade_Escolar"].unique(),
            default=df_filtrado_escola["Tipo_Unidade_Escolar"].unique()
        )
    with col2:
        num_escolas = st.slider("Número de Escolas para Exibir", min_value=5, max_value=50, value=10)
    
    df_filtrado_unidade = df_filtrado_escola[
        df_filtrado_escola["Tipo_Unidade_Escolar"].isin(tipo_unidade_selecionado)
    ]
    
    matriculas_por_unidade = df_filtrado_unidade.groupby(["Nome_Unidade_Escolar", "Tipo_Unidade_Escolar"])["Numero_Matriculas"].sum().reset_index()
    matriculas_por_unidade = matriculas_por_unidade.sort_values(by="Numero_Matriculas", ascending=False)
    
    fig_unidade = px.bar(
        matriculas_por_unidade.head(num_escolas),
        x="Nome_Unidade_Escolar", y="Numero_Matriculas",
        color="Tipo_Unidade_Escolar",
        title=f"Top {num_escolas} Unidades Escolares por Número de Matrículas",
        labels={"Nome_Unidade_Escolar": "Unidade Escolar", "Numero_Matriculas": "Número de Matrículas"}
    )
    st.plotly_chart(fig_unidade, use_container_width=True)

def mostrar_superintendencia():
    st.title("🏛️ **Dashboard por Superintendência**")
    
    # FILTRO DE REGIÃO MOVIDO PARA ESTA PÁGINA
    regiao_selecionada = st.multiselect(
        "Selecionar Região",
        options=df_filtrado_global["Regiao"].unique(),
        default=df_filtrado_global["Regiao"].unique(),
        key="regiao_super"
    )
    
    df_filtrado_super_base = df_filtrado_global[
        df_filtrado_global["Regiao"].isin(regiao_selecionada)
    ]
    
    # FILTRO ESPECÍFICO DESTA PÁGINA
    col1, col2 = st.columns(2)
    with col1:
        superintendencia_selecionada = st.multiselect(
            "Filtrar por Superintendência",
            options=df_filtrado_super_base["Superintendencia"].unique(),
            default=df_filtrado_super_base["Superintendencia"].unique()
        )
    
    df_filtrado_super = df_filtrado_super_base[
        df_filtrado_super_base["Superintendencia"].isin(superintendencia_selecionada)
    ]
    
    matriculas_por_super = df_filtrado_super.groupby(["Superintendencia", "Regiao"])["Numero_Matriculas"].sum().reset_index()
    
    fig_super = px.bar(
        matriculas_por_super,
        x="Superintendencia", y="Numero_Matriculas",
        color="Regiao",
        title="Total de Matrículas por Superintendência Regional",
        labels={"Superintendencia": "Superintendência", "Numero_Matriculas": "Número de Matrículas"}
    )
    st.plotly_chart(fig_super, use_container_width=True)

def mostrar_banco():
    st.title("💾 **Base de Dados**")
    st.subheader("**Visão Geral dos Dados**")
    st.dataframe(df_filtrado_global.head())
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Registros", len(df_filtrado_global))
        st.metric("Colunas", len(df_filtrado_global.columns))
    with col2:
        st.metric("Total Matrículas", f"{df_filtrado_global['Numero_Matriculas'].sum():,.0f}")
        st.metric("Período", f"{df_filtrado_global['Ano_Matricula'].min()} - {df_filtrado_global['Ano_Matricula'].max()}")

def mostrar_etapas():
    st.title("🚀 **Próximas Etapas**")
    st.markdown("""
    ### 📅 **Roadmap 2026**
    
    | Mês | Tarefa | Status |
    |-----|--------|--------|
    | Nov/25 | Aplicação na Base de Dados Real | ⏳ Planejado |
    | Dez/25 | Melhorias no Front | ⏳ Planejado |
    | Jan/26 | Relatórios Automáticos | ⏳ Planejado |
    | Fev/26 | Publicação | ⏳ Planejado |
    
    **Recursos Necessários:**
    - Base de Dados Verdadeira
    """)

def mostrar_dev():
    st.title("👨‍💻 **Sobre o Desenvolvedor**")
    st.markdown("""
    **João Batista Guedes Neto**  
    *Analista de TI*
    *SEDU - Gerência de Tecnologia da Informação*
        
    
    **Stack Técnico:**
    | Frontend | Backend | Dados |
    |----------|---------|-------|
    | Streamlit | Python | Pandas |
    | Plotly | Django |  |
    """)

# === EXECUTAR PÁGINA SELECIONADA ===
if selected_page == "🏠 Apresentação do Projeto":
    mostrar_apresentacao()
elif selected_page == "📈 Dashboard Regional":
    mostrar_regional()
elif selected_page == "🏫 Dashboard por Escola":
    mostrar_escola()
elif selected_page == "🏛️ Dashboard por Superintendência":
    mostrar_superintendencia()
elif selected_page == "💾 Base de dados":
    mostrar_banco()
elif selected_page == "🚀 Próximas Etapas":
    mostrar_etapas()
elif selected_page == "👨‍💻 Desenvolvedor":
    mostrar_dev()

# Footer na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("*Desenvolvido com 😩 em Python | 2025*")