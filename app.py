import streamlit as st
from streamlit_player import st_player
import requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="JC VIP Player", layout="wide")

# --- LOGIN DO APP ---
if "autenticado" not in st.session_state: st.session_state.autenticado = False
if not st.session_state.autenticado:
    st.title("🔒 JC VIP - Acesso Restrito")
    senha = st.text_input("Senha da Playlist:", type="password")
    if st.button("Entrar"):
        if senha == "12345": st.session_state.autenticado = True; st.rerun()
    st.stop()

# --- CONEXÃO XTREAM ---
with st.sidebar.expander("⚙️ CONFIGURAR PAINEL"):
    dns = st.text_input("DNS", placeholder="http://exemplo.com:8080")
    user = st.text_input("Usuário")
    pw = st.text_input("Senha", type="password")
    if st.button("Conectar e Atualizar"):
        st.session_state.url_base = f"{dns.strip('/')}/player_api.php?username={user}&password={pw}"
        st.session_state.conectado = True
        st.success("Conectado!")

if "conectado" not in st.session_state:
    st.warning("Acesse o menu lateral para conectar seu painel.")
    st.stop()

# --- NAVEGAÇÃO ---
menu = st.sidebar.radio("Navegar", ["🎬 Filmes", "📺 Séries", "📡 TV Ao Vivo"])

# --- FUNÇÃO PARA PEGAR DADOS ---
@st.cache_data
def carregar_dados(acao):
    try:
        r = requests.get(f"{st.session_state.url_base}&action={acao}")
        return r.json()
    except:
        return []

# --- EXIBIÇÃO DE FILMES ---
if menu == "🎬 Filmes":
    st.header("Biblioteca de Filmes")
    # Puxa categorias reais do seu servidor
    categorias = carregar_dados("get_vod_categories")
    cat_nomes = [c['category_name'] for c in categorias]
    escolha_cat = st.selectbox("Escolha uma Categoria", ["Todos"] + cat_nomes)
    
    # Aqui o código buscaria os filmes daquela categoria (simplificado para teste)
    st.info(f"Carregando filmes da categoria: {escolha_cat}...")
    st.write("Dica: Clique em 'Conectar e Atualizar' na lateral se a lista não carregar.")

# --- EXIBIÇÃO DE TV ---
elif menu == "📡 TV Ao Vivo":
    st.header("Canais de TV")
    canais = carregar_dados("get_live_streams")
    if canais:
        busca = st.text_input("🔍 Buscar Canal")
        # Mostra os primeiros 12 canais para não travar o navegador
        for c in canais[:12]:
            if busca.lower() in c['name'].lower():
                col_n, col_p = st.columns([3, 1])
                with col_n: st.write(f"📺 {c['name']}")
                with col_p:
                    # Link real do stream para o player
                    url_stream = f"{dns}/{user}/{pw}/{c['stream_id']}"
                    if st.button("Assistir", key=c['stream_id']):
                        st_player(url_stream)

# --- INÍCIO ---
else:
    st.title("Bem-vindo ao seu Player VIP")
    st.write("Selecione uma opção no menu lateral para começar a assistir.")
