import streamlit as st
import ollama
import pandas as pd

# 1. Identidade Visual
st.set_page_config(
    page_title="CORTEX | Motor de Análise de Risco", page_icon="🧠", layout="wide")

# 2. CSS
st.markdown("""
    <style>
    /* Fundo Escuro Profundo */
    .stApp { 
        background-color: #0a0b10; 
        color: #e0e6ed;
    }
    
    /* Container do Título Principal */
    .header-container {
        text-align: center;
        padding: 40px 0px;
        background: radial-gradient(circle, rgba(0,242,255,0.05) 0%, rgba(10,11,16,1) 70%);
        border-bottom: 1px solid #1a1c24;
        margin-bottom: 30px;
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        letter-spacing: 15px;
        color: #00f2ff;
        text-shadow: 0px 0px 25px rgba(0, 242, 255, 0.7);
        margin-bottom: 0px;
    }
    
    .sub-title {
        font-size: 1.3rem;
        letter-spacing: 8px;
        color: #505050;
        text-transform: uppercase;
        margin-top: -5px;
        font-weight: 300;
    }

    /* Abas Customizadas com Efeito Neon */
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: transparent;
        color: #505050;
        border: none;
        font-size: 1rem;
        letter-spacing: 2px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        color: #00f2ff !important;
        border-bottom: 2px solid #00f2ff !important;
        text-shadow: 0px 0px 10px rgba(0, 242, 255, 0.8);
    }

    /* Botão Estilo "Cyber-Tech" */
    .stButton>button {
        width: 100%;
        background: rgba(0, 242, 255, 0.05);
        color: #00f2ff;
        border: 1px solid #00f2ff;
        border-radius: 0px;
        padding: 15px;
        font-weight: bold;
        letter-spacing: 3px;
        transition: all 0.5s ease;
    }
    .stButton>button:hover {
        background: #00f2ff !important;
        color: #000 !important;
        box-shadow: 0px 0px 40px rgba(0, 242, 255, 0.5);
    }

    /* Estilização de Campos de Texto e Upload */
    .stTextArea textarea { background-color: #0d1117; color: #00f2ff; border: 1px solid #1f2937; }
    [data-testid="stFileUploader"] { 
        background-color: #0d1117; 
        border: 1px dashed #00f2ff; 
        color: #00f2ff;
    }
    
    /* Barra de Progresso Neon */
    .stProgress > div > div > div > div {
        background-color: #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Renderização do Header
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">CORTEX</h1>
        <p class="sub-title">Análise de Risco</p>
    </div>
    """, unsafe_allow_html=True)

# Definição das Abas em Português
aba1, aba2 = st.tabs(["◈ ENTRADA NEURAL", "◈ PROCESSAMENTO DE MATRIZ"])

# --- ABA 1: ENTRADA NEURAL (Análise Individual) ---
with aba1:
    conversa = st.text_area("FLUXO DE DADOS (TEXTO BRUTO):", height=150,
                            placeholder="Insira o conteúdo para análise sistêmica...")
    if st.button("EXECUTAR VARREDURA NEURAL"):
        if conversa:
            with st.spinner("🧠 CORTEX: Decompondo padrões de risco..."):
                prompt_unico = f"""
                Atue como o motor CORTEX. 
                Analise o relato: '{conversa}'
                Regras de Classificação:
                - NORMAL: Elogios, dúvidas simples ou agradecimentos.
                - GRAVE: Ameaças jurídicas, menção a 'advogado', 'justiça', 'PROCON' ou danos.
                Determine a GRAVIDADE e o RISCO DE PROCESSO.
                Retorne uma análise técnica, curta e precisa.
                """
                response = ollama.generate(model='llama3', prompt=prompt_unico)
                st.markdown(f"### ⚡ Resultado do Diagnóstico")
                st.info(response['response'])

# --- ABA 2: PROCESSAMENTO DE MATRIZ (Análise em Lote) ---
with aba2:
    st.write("### 📂 Importar Matriz de Dados")

    # configurado totalmente em português
    arquivo = st.file_uploader(
        "Selecione o arquivo de origem (CSV ou XLSX)",
        type=['csv', 'xlsx'],
        help="Arraste o arquivo para esta área ou clique para navegar nas pastas."
    )

    if arquivo is not None:
        try:
            # Leitura inteligente baseada na extensão
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo, encoding='latin1',
                                 sep=None, engine='python')
            else:
                df = pd.read_excel(arquivo)

            # Saneamento de dados
            df = df.replace(to_replace=r'\btão\b',
                            value='estão', regex=True).fillna('')

            # Unificação de colunas para análise global
            df['Relato Cliente'] = df.apply(lambda row: " ".join(
                [str(val) for val in row.values if str(val).lower() not in ['', 'none']]), axis=1)

            st.write("🔍 **Estrutura de Matriz Detectada:**")
            st.dataframe(df[['Relato Cliente']].head(),
                         use_container_width=True)

            if st.button("🚀 ATIVAR PROTOCOLO EM MASSA"):
                resultados = []
                barra_progresso = st.progress(0)
                status_texto = st.empty()
                total_linhas = len(df)

                for i, row in df.iterrows():
                    relato = row['Relato Cliente']
                    status_texto.text(
                        f"📡 CORTEX: Processando segmento {i+1}/{total_linhas}")

                    # Engenharia de Prompt para o motor CORTEX
                    prompt_lote = f"""
                    Atue como o motor de inteligência CORTEX. 
                    Analise: "{relato}"
                    Regras: 
                    1. NORMAL: Elogios, notas altas, agradecimentos ou dúvidas.
                    2. GRAVE: Ameaças judiciais, menção a advogado, PROCON ou danos críticos.
                    Saída obrigatória: [GRAVIDADE] | [ANÁLISE] | [RISCO]
                    """

                    response = ollama.generate(
                        model='llama3', prompt=prompt_lote)
                    resultados.append(response['response'])
                    barra_progresso.progress((i + 1) / total_linhas)

                # Armazenamento persistente do resultado
                df['Análise CORTEX'] = resultados
                st.session_state['resultado_cortex'] = df[[
                    'Relato Cliente', 'Análise CORTEX']]
                st.success("✅ PROTOCOLO FINALIZADO COM SUCESSO.")

        except Exception as e:
            st.error(f"FALHA NA MATRIX: {e}")

    # Exibição e exportação dos dados processados
    if 'resultado_cortex' in st.session_state:
        df_exibir = st.session_state['resultado_cortex']
        st.markdown("---")
        st.write("### 📊 Relatório de Inteligência Gerado")
        st.dataframe(df_exibir, use_container_width=True)

        csv_data = df_exibir.to_csv(index=False).encode('latin1')
        st.download_button(
            label="📥 EXPORTAR DATASET ANALISADO",
            data=csv_data,
            file_name='analise_cortex_final.csv',
            mime='text/csv'
        )
