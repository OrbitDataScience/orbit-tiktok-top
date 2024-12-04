import streamlit as st
import hashlib
from scripts import *
import os
import base64
import streamlit.components.v1 as components
import pkg_resources

st.set_page_config(page_title="Orbit TikTok API", page_icon="🚀", layout="centered")

# Função simples de hash
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Senhas reais (antes do hashing)
raw_passwords = {
    "@orbitdatascience": "psswd@123",  # Exemplo de senha para user1
}

# Gerando os hashes das senhas reais
user_credentials = {user: hash_password(pwd) for user, pwd in raw_passwords.items()}

# Verificando se o usuário já está autenticado
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Condicional para exibir o formulário de login ou o conteúdo
if not st.session_state['authenticated']:
    st.header("Orbit TikTok API")
    st.divider()
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username in user_credentials and hash_password(password) == user_credentials[username]:
            st.session_state['authenticated'] = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")

else:
    st.header("Orbit TikTok API")
    st.divider()

    with st.form(key='my_form'):
        keyword = st.text_input('Palavra-chave:')
        date = st.selectbox('Data das postagens', ['Tudo', 'Últimas 24 horas', 'Última semana', 'Último mês', 'Últimos 3 meses', 'Últimos 6 meses'])
        order = st.selectbox('Ordem', ['Relevância', 'Mais Likes', 'Mais novos'])
        submit = st.form_submit_button(label='Buscar')

    if submit:
        get_api(keyword, date, order)
        main_filename = 'tiktok.xlsx'
        # Fornece o arquivo para download automaticamente
        with open(main_filename, "rb") as f:
                    bytes_data = f.read()
                    b64 = base64.b64encode(bytes_data).decode()
                    href = f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}'
                    download_script = f'''
                    <html>
                        <body>
                            <a id="download_link" href="{href}" download="{main_filename}"></a>
                            <script>
                                document.getElementById('download_link').click();
                            </script>
                        </body>
                    </html>
                    '''
                    components.html(download_script)
