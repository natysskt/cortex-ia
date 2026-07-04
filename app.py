import streamlit as st
import pandas as pd
import google.generativeai as genai
import plotly.graph_objects as go

# Configura a Chave Mestra automaticamente
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="CORTEX - Intel", layout="wide")

# (Mantenha o CSS original aqui...)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .side-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 16px; }
    .card-title { font-size: 11px; font-weight: 600; letter-spacing: 2px; color: #8b949e; text-transform: uppercase; margin-bottom: 6px; }
    .center-container { text-align: center; padding-top: 15px; }
    .tech-circle { width: 140px; height: 140px; margin: 20px auto 40px auto; border: 2px dashed rgba(88, 166, 255, 0.4); border-radius: 50%; box-shadow: 0 0 30px rgba(56, 139, 253, 0.15); display: flex; align-items: center; justify-content: center; position: relative; animation: pulse 3s infinite; }
    .brand-title { font-size: 52px; font-weight: 800; letter-spacing: 16px; color: #f0f6fc; margin: 0; font-family: monospace; }
    .brand-subtitle { font-size: 12px; letter-spacing: 8px; color: #58a6ff; text-transform: uppercase; margin-top: 6px; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(88, 166, 255, 0.4); } 70% { box-shadow: 0 0 0 20px rgba(88, 166, 255, 0); } 100% { box-shadow: 0 0 0 0 rgba(88, 166, 255, 0); } }
    </style>
""", unsafe_allow_html=True)

# Estados
if 'taxa_risco' not in st.session_state:
    st.session_state.taxa_risco = 0
if 'dados_finais' not in st.session_state:
    st.session_state.dados_finais = None

# Layout
col_esq, col_cen, col_dir = st.columns([1.2, 2, 1.2])

with col_esq:
    st.markdown('<div class="side-card"><div class="card-title">▩ INGESTÃO DE DADOS</div></div>',
                unsafe_allow_html=True)
    # AQUI O CAMPO DE INPUT DA CHAVE FOI REMOVIDO!
    arquivo = st.file_uploader("Upload da Base", type=["csv", "xlsx"])

    if arquivo and st.button("⚡ INICIAR VARREDURA (20K)"):
        df = pd.read_csv(arquivo) if arquivo.name.endswith(
            '.csv') else pd.read_excel(arquivo)
        st.session_state.taxa_risco = 42.5
        st.session_state.dados_finais = df
        st.rerun()

with col_cen:
    st.markdown("""
        <div class="center-container">
            <div class="tech-circle">
                <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a9 9 0 0 1 9 9v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 9-9z"></path>
                    <circle cx="9" cy="11" r="1" fill="#58a6ff"></circle>
                    <circle cx="15" cy="11" r="1" fill="#58a6ff"></circle>
                    <path d="M8 15h8"></path>
                </svg>
            </div>
            <h1 class="brand-title">CORTEX</h1>
            <div class="brand-subtitle">análise de risco</div>
        </div>
    """, unsafe_allow_html=True)

with col_dir:
    st.markdown('<div class="side-card"><div class="card-title">TAXA DE RISCO GLOBAL</div></div>',
                unsafe_allow_html=True)
    # Medidor (simplificado)
    fig = go.Figure(go.Indicator(mode="gauge+number",
                    value=st.session_state.taxa_risco))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20),
                      paper_bgcolor="rgba(0,0,0,0)", font={'color': "#c9d1d9"})
    st.plotly_chart(fig, use_container_width=True)

if st.session_state.dados_finais is not None:
    st.markdown("---")
    st.dataframe(st.session_state.dados_finais, use_container_width=True)
