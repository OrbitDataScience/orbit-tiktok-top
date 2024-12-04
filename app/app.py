import streamlit as st
from scripts import *
import os
import base64
import streamlit.components.v1 as components
import pkg_resources

st.set_page_config(page_title="Orbit TikTok Tops", page_icon="🚀", layout="centered")
st.title('Orbit TikTok Tops')

with st.form(key='my_form'):
    keyword = st.text_input('Palavra-chave:')
    date = st.selectbox('Data das postagens', ['Tudo', 'Últimas 24 horas', 'Última semana', 'Último mês', 'Últimos 3 meses', 'Últimos 6 meses'])
    submit = st.form_submit_button(label='Buscar')


if submit:
    get_api(keyword, date)
    df = pd.read_excel('tiktok.xlsx')
    df_ordenado = df.sort_values(by='Visualizações', ascending=False)
    df_ordenado.to_excel('arquivo_ordenado.xlsx', index=False)

     # Fornece o arquivo para download automaticamente
    with open('arquivo_ordenado.xlsx', "rb") as f:
                bytes_data = f.read()
                b64 = base64.b64encode(bytes_data).decode()
                href = f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}'
                download_script = f'''
                <html>
                    <body>
                        <a id="download_link" href="{href}" download="arquivo_ordenado.xlsx"></a>
                        <script>
                            document.getElementById('download_link').click();
                        </script>
                    </body>
                </html>
                '''
                components.html(download_script)


