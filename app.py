import streamlit as st
from streamlit_player import st_player
import requests
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="JC VIP Player", layout="wide", initial_sidebar_state="expanded")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; }
    .movie-card { background-color: #1e1e1e; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "vistos" not in st.session_state: st.session_state.vistos = []
if "dados_conectados" not in st.session_state: st.session_state.dados_conectados = False

# --- 1. TELA DE PROTEÇÃO (SENHA DO APP) ---
if not st.session_state.autenticado:
    st.title("🔒 JC VIP - Acesso Restrito")
    senha_acesso = st.text_input("Digite a senha da Playlist:", type="password")
    if st.button("Acessar Player"):
        if senha_acesso == "12345": # Mude aqui sua senha master
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- 2. BARRA LATERAL (CONFIGURAÇÃO E NAVEGAÇÃO) ---
with st.sidebar:
    st.title("📺 JC VIP")
    
    with st.expander("⚙️ CONEXÃO XTREAM (ADMIN)"):
        dns = st.text_input("DNS/URL", placeholder="http://exemplo.com:8080")
        user = st.text_input("Usuário")
        pw = st.text_input("Senha", type="password")
        if st.button("Conectar Painel"):
            st.session_state.dns = dns.strip("/")
            st.session_state.user = user
            st.session_state.pw = pw
            st.session_state.dados_conectados = True
            st.success("Conectado!")

    st.divider()
    menu = st.radio("Navegar", ["🏠 Início", "🎬 Filmes", "📺 Séries"])
    
    if st.button("🧹 Limpar Cache"):
        st.cache_data.clear()
        st.toast("Cache Limpo!")

# --- 3. LÓGICA DE CONTEÚDO ---
if not st.session_state.dados_conectados:
    st.warning("⚠️ Por favor, configure os dados do seu painel na barra lateral para carregar o conteúdo.")
    st.stop()

# URLs base do Xtream Codes
base_url = f"{st.session_state.dns}/player_api.php?username={st.session_state.user}&password={st.session_state.pw}"

# --- ABA FILMES ---
if menu == "🎬 Filmes":
    st.header("🎬 Catálogo de Filmes")
    busca = st.text_input("🔍 Pesquisar filme...")
    
    # Exemplo de Grid (Na integração total, faríamos o request das categorias aqui)
    col1, col2, col3, col4 = st.columns(4)
    # Exemplo funcional de interface de detalhes
    with col1:
        st.image("https://via.placeholder.com/300x450.png?text=Filme+Exemplo", use_container_width=True)
        if st.button("Ver Detalhes", key="f1"):
            st.session_state.selecionado = "filme_exemplo"

    if st.session_state.get("selecionado") == "filme_exemplo":
        st.divider()
        c1, c2 = st.columns([1, 2])
        with c1: st.image("https://via.placeholder.com/300x450.png?text=Filme+Exemplo")
        with c2:
            st.subheader("Sinopse")
            st.write("Aqui o app mostrará a sinopse real vinda do seu servidor.")
            b_play, b_vlc = st.columns(2)
            stream_url = f"{st.session_state.dns}/movie/{st.session_state.user}/{st.session_state.pw}/ID_DO_FILME.mp4"
            with b_play:
                if st.button("▶️ Assistir Agora"): st_player(stream_url)
            with b_vlc:
                st.link_button("🧡 Abrir no VLC", f"vlc://{stream_url}")

# --- ABA SÉRIES ---
elif menu == "📺 Séries":
    st.header("📺 Séries Separadas")
    busca_s = st.text_input("🔍 Pesquisar série...")
    
    # Simulação de marcação de assistido
    st.subheader("Episódios")
    for i in range(1, 4):
        ep_id = f"serie1_ep{i}"
col_n, col_v, col_p = st.columns([3, 1, 1])
        with col_n: st.write(f"Episódio {i} - O Despertar")
        with col_v: 
            status = "✅ Assistido" if ep_id in st.session_state.vistos else "⬜ Pendente"
            st.write(status)
        with col_p:
            if st.button("Play", key=ep_id):
                if ep_id not in st.session_state.vistos: st.session_state.vistos.append(ep_id)
                st.rerun()

# --- ABA INÍCIO (AVISOS) ---
else:
    st.title("Bem-vindo ao seu Player VIP")
    st.info("📅 Seu acesso está ativo. Vencimento: 03/06/2026")
    # Lógica de aviso de 3 dias (Exemplo)
    st.warning("⚠️ Atenção: Sua assinatura vence em 3 dias. Entre em contato para renovar!")
