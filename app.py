import streamlit as st
from streamlit_player import st_player
import requests

st.set_page_config(page_title="JC VIP Player", layout="wide")

# --- LOGIN SIMPLES ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔒 JC VIP")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if senha == "12345":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- CONFIGURAÇÃO NA LATERAL ---
with st.sidebar:
    st.header("⚙️ Configuração")
    dns = st.text_input("DNS (ex: http://ka23.in)", value="http://ka23.in")
    user = st.text_input("Usuário", value="jefferson01699")
    pw = st.text_input("Senha", type="password")
    
    if st.button("Conectar e Testar"):
        # Limpa cache para forçar nova busca
        st.cache_data.clear()
        st.session_state.url_base = f"{dns.strip('/')}/player_api.php?username={user}&password={pw}"
        st.session_state.credenciais = {"dns": dns.strip('/'), "user": user, "pw": pw}
        st.session_state.conectado = True
        st.success("Configuração Salva!")

if "conectado" not in st.session_state:
    st.info("Preencha os dados ao lado e clique em Conectar.")
    st.stop()

# --- FUNÇÃO DE BUSCA COM DIAGNÓSTICO ---
def buscar_dados(acao):
    url = f"{st.session_state.url_base}&action={acao}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro no Servidor: Código {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Erro de Conexão: {e}")
        return []

# --- MENU ---
aba = st.tabs(["📺 TV Ao Vivo", "🎬 Filmes", "🛠️ Diagnóstico"])

with aba[0]:
    st.header("Canais")
    if st.button("Carregar Canais Agora"):
        dados = buscar_dados("get_live_streams")
        if not dados:
            st.warning("O servidor não retornou canais. Verifique Usuário/Senha.")
        else:
            st.success(f"{len(dados)} canais encontrados!")
            for c in dados[:20]: # Mostra os primeiros 20
                with st.expander(f"▶️ {c['name']}"):
                    url_stream = f"{st.session_state.credenciais['dns']}/{st.session_state.credenciais['user']}/{st.session_state.credenciais['pw']}/{c['stream_id']}"
                    st_player(url_stream)

with aba[1]:
    st.header("Filmes")
    if st.button("Carregar Filmes"):
        filmes = buscar_dados("get_vod_streams")
        if filmes:
            st.success(f"{len(filmes)} filmes encontrados!")
            # Criar colunas para as capas
            cols = st.columns(4)
            for i, f in enumerate(filmes[:12]):
                with cols[i % 4]:
                    st.image(f.get('stream_icon', ''), use_container_width=True)
                    st.caption(f['name'])

with aba[2]:
    st.header("Painel de Controle")
    st.write("Link de Teste gerado:")
    st.code(f"{st.session_state.url_base}&action=get_live_streams")
    if st.button("Testar Resposta Bruta"):
        res = requests.get(f"{st.session_state.url_base}&action=get_live_streams")
        st.text(res.text[:500]) # Mostra os primeiros 500 caracteres da resposta
