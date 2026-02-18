import streamlit as st
from streamlit_player import st_player
import requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="JC VIP Player", layout="wide", initial_sidebar_state="expanded")

# --- ESTADO DO APP ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "dados_conectados" not in st.session_state:
    st.session_state.dados_conectados = False
if "vistos" not in st.session_state:
    st.session_state.vistos = []

# --- 1. TELA DE ACESSO (SENHA PLAYLIST) ---
if not st.session_state.autenticado:
    st.title("🔒 JC VIP - Acesso Restrito")
    senha_acesso = st.text_input("Digite a senha da Playlist:", type="password")
    if st.button("Acessar Player"):
        if senha_acesso == "12345":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()

# --- 2. BARRA LATERAL (ADMIN E MENU) ---
with st.sidebar:
    st.title("📺 JC VIP")
    
    with st.expander("⚙️ CONEXÃO PAINEL (ADMIN)"):
        dns_input = st.text_input("DNS/URL", placeholder="http://exemplo.com:8080")
        user_input = st.text_input("Usuário")
        pw_input = st.text_input("Senha", type="password")
        if st.button("Conectar"):
            st.session_state.dns = dns_input.strip("/")
            st.session_state.user = user_input
            st.session_state.pw = pw_input
            st.session_state.dados_conectados = True
            st.success("Conectado!")

    st.divider()
    menu = st.radio("Navegar", ["🏠 Início", "🎬 Filmes", "📺 Séries"])

# --- 3. VERIFICAÇÃO DE DADOS ---
if not st.session_state.dados_conectados:
    st.warning("⚠️ Configure os dados do seu painel na lateral para carregar o conteúdo.")
    st.stop()

# --- ABA FILMES ---
if menu == "🎬 Filmes":
    st.header("🎬 Catálogo de Filmes")
    busca = st.text_input("🔍 Pesquisar filme...")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("https://via.placeholder.com/300x450.png?text=Filme+Exemplo", use_container_width=True)
        if st.button("Ver Detalhes", key="f_ex"):
            st.session_state.detalhe_filme = True

    if st.session_state.get("detalhe_filme"):
        st.divider()
        c1, c2 = st.columns([1, 2])
        with c1:
            st.image("https://via.placeholder.com/300x450.png?text=Filme+Exemplo")
        with c2:
            st.subheader("Sinopse do Filme")
            st.write("Aqui aparecerá a descrição vinda do seu servidor.")
            b_play, b_vlc = st.columns(2)
            url_stream = f"{st.session_state.dns}/movie/{st.session_state.user}/{st.session_state.pw}/1.mp4"
            with b_play:
                if st.button("▶️ DAR O PLAY"):
                    st_player(url_stream)
            with b_vlc:
                st.link_button("🧡 Abrir no VLC", f"vlc://{url_stream}")

# --- ABA SÉRIES ---
elif menu == "📺 Séries":
    st.header("📺 Catálogo de Séries")
    st.write("---")
    
    # Exemplo de Episódios com correção de espaços
    for i in range(1, 4):
        ep_id = f"s1_ep{i}"
        col_n, col_v, col_p = st.columns([3, 1, 1])
        with col_n:
            st.write(f"Episódio {i} - O Despertar")
        with col_v:
            status = "✅ Assistido" if ep_id in st.session_state.vistos else "⬜ Pendente"
            st.write(status)
        with col_p:
            if st.button("Play", key=ep_id):
                if ep_id not in st.session_state.vistos:
                    st.session_state.vistos.append(ep_id)
                st.rerun()

# --- ABA INÍCIO ---
else:
    st.title("Bem-vindo ao seu Player VIP")
    st.info("📅 Seu acesso está ativo até: 03/06/2026")
    st.warning("⚠️ Sua assinatura vence em 3 dias. Lembre-se de renovar!")
