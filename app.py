import streamlit as st
from streamlit_player import st_player
import requests
from datetime import datetime

# --- CONFIGURAÇÕES INICIAIS ---
st.set_page_config(page_title="JC VIP Player", layout="wide", initial_sidebar_state="expanded")

# 1. COLOQUE SEUS DADOS DO PAINEL AQUI
DNS = "http://seu-servidor.com:8080" # Exemplo: http://painel.tv:8080
USER = "seu_usuario"
PASS = "sua_senha"
SENHA_ACESSO_APP = "12345" # Senha para o cliente entrar no app

# --- SISTEMA DE LOGIN E SEGURANÇA ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 JC VIP - Acesso Restrito")
    senha_dig = st.text_input("Digite sua senha de acesso:", type="password")
    if st.button("Entrar no Player"):
        if senha_dig == SENHA_ACESSO_APP:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- MEMÓRIA DE CONTEÚDO (ASSISTIDOS) ---
if "vistos" not in st.session_state:
    st.session_state.vistos = set()

def marcar_visto(id_video):
    st.session_state.vistos.add(id_video)

# --- INTERFACE PRINCIPAL ---
st.sidebar.title("📺 JC VIP STREAMING")
st.sidebar.caption(f"📅 Expira em: 03/06/2026") # Exemplo discreto

menu = st.sidebar.radio("Navegar por:", ["🎬 Filmes", "📺 Séries", "⚙️ Ajustes"])

# --- ABA DE FILMES ---
if menu == "🎬 Filmes":
    st.header("Biblioteca de Filmes")
    busca = st.text_input("🔍 Pesquisar filme...")
    
    # Simulação de Galeria (Na integração final, usaremos requests no DNS)
    col1, col2, col3, col4 = st.columns(4)
    
    # Exemplo de Card de Filme
    with col1:
        st.image("https://image.tmdb.org/t/p/w500/1E5baAa9S4fe96m0tqDlsSfqZBL.jpg", use_container_width=True)
        if st.button("Ver Detalhes", key="movie_1"):
            st.session_state.detalhe = "filme_1"

    if st.session_state.get("detalhe") == "filme_1":
        st.divider()
        c_capa, c_info = st.columns([1, 2])
        with c_capa:
            st.image("https://image.tmdb.org/t/p/w500/1E5baAa9S4fe96m0tqDlsSfqZBL.jpg")
        with c_info:
            st.subheader("Sinopse do Filme")
            st.write("Aqui aparecerá a descrição automática vinda do seu servidor Xtream Codes.")
            
            btn1, btn2 = st.columns(2)
            with btn1:
                if st.button("▶️ DAR O PLAY"):
                    st_player(f"{DNS}/movie/{USER}/{PASS}/1.mp4")
            with btn2:
                st.link_button("🧡 Abrir no VLC", f"vlc://{DNS}/movie/{USER}/{PASS}/1.mp4")

# --- ABA DE SÉRIES ---
elif menu == "📺 Séries":
    st.header("Séries e Documentários")
    busca_s = st.text_input("🔍 Buscar Série...")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.image("https://image.tmdb.org/t/p/w500/8Ul69S0NAU9XpU6pS2BM9mJ6o6Q.jpg", width=200)
        if st.button("Explorar Temporadas", key="serie_1"):
            st.session_state.serie_id = "serie_1"

    if st.session_state.get("serie_id") == "serie_1":
        st.write("---")
        temp = st.selectbox("Selecione a Temporada", ["Temporada 01", "Temporada 02"])
        
        # Lista de Episódios com Marcação de Assistido
        for i in range(1, 4):
            ep_key = f"S1E{i}"
            ce1, ce2, ce3 = st.columns([3, 1, 1])
            with ce1: st.write(f"Episódio {i} - Título do Episódio")
            with ce2: 
                status = "✅" if ep_key in st.session_state.vistos else "⬜"
                st.write(status)
            with ce3:
                if st.button("Play", key=ep_key):
                    marcar_visto(ep_key)
                    st.toast(f"Reproduzindo {ep_key}")
                    st_player(f"{DNS}/series/{USER}/{PASS}/{i}.mp4")

# --- AJUSTES ---
else:
    st.header("Configurações")
    if st.button("🧹 Limpar Cache do App"):
        st.cache_data.clear()
        st.success("Cache limpo com sucesso!")
    
    if st.button("🚪 Sair do Aplicativo"):
        st.session_state.autenticado = False
        st.rerun()
st.sidebar.divider()
st.sidebar.info("Dica: Use o ícone no vídeo para espelhar via Chromecast.")
