import streamlit as st
import ollama

st.set_page_config(page_title="Audit-AI: Auditoria de SAC", page_icon="🛡️")

st.title("🛡️ Audit-AI: Monitor de Riscos")
st.subheader("Foco em Segurança Jurídica e LGPD")

# Onde o usuário digita a conversa do SAC
conversa = st.text_area("Cole aqui a conversa ou reclamação do cliente:", placeholder="Ex: Vou processar vocês, o atendente me desrespeitou...")

if st.button("Analisar Risco"):
    if conversa:
        with st.spinner("IA analisando localmente... (Privacidade Garantida)"):
            # O "Segredo" está neste comando para a IA
            prompt = f"Analise se a frase a seguir oferece risco jurídico ou de imagem para uma empresa. Classifique como BAIXO, MÉDIO ou ALTO e explique o porquê: {conversa}"
            
            response = ollama.generate(model='llama3', prompt=prompt)
            
            st.markdown("### Resultado da Auditoria:")
            st.info(response['response'])
    else:
        st.warning("Por favor, cole alguma conversa para analisar.")

st.sidebar.info("Projeto desenvolvido para Auditoria Local de Dados (On-Premise).")