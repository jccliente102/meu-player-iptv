import streamlit as st
from streamlit_player import st_player
import requests

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="JC VIP Player", layout="wide")

# --- LOGIN DO APLICATIVO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 JC VIP - Acesso Restrito")
    senha = st.text_input("Senha da Playlist:", type="password")
    if st.button("Entrar"):
        if senha == "12345":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- BARRA LATERAL (CONEXÃO) ---
with st.sidebar:
    st.title("📺 JC VIP")
    with st.expander("⚙️ CONFIGURAR PAINEL", expanded=False):
        dns = st.text_input("DNS", value="http://ka23.in")
        user = st.text_input("Usuário", value="jefferson01699")
        pw = st.text_input("Senha", type="password")
        if st.button("Conectar e Atualizar"):
            st.session_state.url_base = f"{dns.strip('/')}/player_api.php?username={user}&password={pw}"
            st.session_state.dns_puro = dns.strip('/')
            st.session_state.user_puro = user
            st.session_state.pw_puro = pw
            st.session_state.conectado = True
            st.cache_data.clear()
            st.success("Conectado!")

    if "conectado" not in st.session_state:
        st.warning("Configure o painel acima 👆")
        st.stop()
    
    menu = st.radio("Navegar", ["📡 TV Ao Vivo", "🎬 Filmes", "📺 Séries"])

# --- FUNÇÃO DE BUSCA NA API ---
@st.cache_data(ttl=600)
def chamar_api(acao):
    try:
        url = f"{st.session_state.url_base}&action={acao}"
        r = requests.get(url, timeout=10)
        return r.json()
    except:
        return []

# --- EXIBIÇÃO: TV AO VIVO ---
if menu == "📡 TV Ao Vivo":
    st.header("📡 Canais de TV")
    busca = st.text_input("🔍 Buscar canal...")
    
    canais = chamar_api("get_live_streams")
    
    if canais:
        # Filtro de busca
        lista_filtrada = [c for c in canais if busca.lower() in c['name'].lower()] if busca else canais[:50]
        
        for canal in lista_filtrada[:30]: # Limitado a 30 para carregar rápido
            col_img, col_txt, col_btn = st.columns([1, 4, 2])
            with col_img:
                st.image(canal.get('stream_icon', ''), width=50) if canal.get('stream_icon') else st.write("📺")
            with col_txt:
                st.subheader(canal['name'])
            with col_btn:
                # Link direto para o fluxo de vídeo
                url_stream = f"{st.session_state.dns_puro}/{st.session_state.user_puro}/{st.session_state.pw_puro}/{canal['stream_id']}"
                if st.button("Assistir", key=f"live_{canal['stream_id']}"):
                    st_player(url_stream)
    else:
        st.error("Nenhum canal encontrado. Verifique seus dados de login.")

# --- EXIBIÇÃO: FILMES ---
elif menu == "🎬 Filmes":
    st.header("🎬 Biblioteca de Filmes")
    filmes = chamar_api("get_vod_streams")
    
    if filmes:
        busca_f = st.text_input("🔍 Nome do filme...")
        lista_f = [f for f in filmes if busca_f.lower() in f['name'].lower()] if busca_f else filmes[:20]
        
        cols = st.columns(4)
        for idx, filme in enumerate(lista_f):
            with cols[idx % 4]:
                st.image(filme.get('stream_icon', ''), use_container_width=True)
                st.caption(filme['name'])
                url_f = f"{st.session_state.dns_puro}/movie/{st.session_state.user_puro}/{st.session_state.pw_puro}/{filme['stream_id']}.mp4"
                if st.button("Play", key=f"vod_{filme['stream_id']}"):
                    st_player(url_f)

# --- EXIBIÇÃO: SÉRIES ---
elif menu == "📺 Séries":
    st.header("📺 Séries")
    series = chamar_api("get_series")
    if series:
        st.write(f"Total de séries encontradas: {len(series)}")
        st.info("Selecione uma categoria ou pesquise para listar.")
