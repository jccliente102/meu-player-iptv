import streamlit as st
from streamlit_player import st_player
import requests

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="JC VIP Player", layout="wide")

if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "conectado" not in st.session_state: st.session_state.conectado = False

# --- LOGIN APP ---
if not st.session_state.autenticado:
    st.title("🔒 JC VIP")
    if st.text_input("Senha:", type="password") == "12345":
        if st.button("Entrar"):
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- CONFIGURAÇÃO PAINEL ---
with st.sidebar:
    st.header("⚙️ Conexão")
    dns = st.text_input("DNS", value="http://ka23.in")
    user = st.text_input("Usuário", value="jefferson01699")
    pw = st.text_input("Senha", type="password")
    if st.button("Conectar"):
        st.session_state.url_base = f"{dns.strip('/')}/player_api.php?username={user}&password={pw}"
        st.session_state.dados = {"dns": dns.strip('/'), "user": user, "pw": pw}
        st.session_state.conectado = True
        st.success("Configurado!")

if not st.session_state.conectado:
    st.info("Configure os dados na lateral.")
    st.stop()

# --- FUNÇÃO COM "DISFARCE" (USER-AGENT) ---
def buscar_dados_v2(acao):
    url = f"{st.session_state.url_base}&action={acao}"
    # Cabeçalhos que fingem ser um app real
    headers = {
        'User-Agent': 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) Mag200 sb.app.html (SmartersPlayer)'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"O Servidor ainda bloqueia: {response.status_code}")
            return []
    except:
        return []

# --- INTERFACE ---
aba1, aba2 = st.tabs(["📡 Canais", "🎬 Filmes"])

with aba1:
    if st.button("🔄 Carregar Lista de Canais"):
        with st.spinner("Buscando canais..."):
            canais = buscar_dados_v2("get_live_streams")
            if canais:
                st.success(f"{len(canais)} Canais carregados!")
                for c in canais[:25]:
                    with st.expander(f"📺 {c['name']}"):
                        stream = f"{st.session_state.dados['dns']}/{st.session_state.dados['user']}/{st.session_state.dados['pw']}/{c['stream_id']}"
                        st_player(stream)
            else:
                st.warning("A lista voltou vazia. Verifique se o seu usuário está ativo no painel.")

with aba2:
    if st.button("🔄 Carregar Filmes"):
        filmes = buscar_dados_v2("get_vod_streams")
        if filmes:
            cols = st.columns(4)
            for i, f in enumerate(filmes[:12]):
                with cols[i % 4]:
                    st.image(f.get('stream_icon', ''), use_container_width=True)
                    st.caption(f['name'])
