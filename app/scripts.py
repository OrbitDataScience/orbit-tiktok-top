import requests
import streamlit as st
import pandas as pd
import json
import csv
from datetime import datetime

def get_api(keyword, date):

    headers = {
            "x-rapidapi-key": "88b5804da0mshaec086ad3147560p16ac64jsn608ec3c7f56c",
            "x-rapidapi-host": "tiktok-video-no-watermark10.p.rapidapi.com"
    }
    
    
    has_more = True
    cursor = "0"
    responses_list = []

    switcher = {
        'Tudo': 0,
        'Últimas 24 horas': 1,
        'Última semana': 7,
        'Último mês': 30,
        'Últimos 3 meses': 90,
        'Últimos 6 meses': 180
    }
    date = switcher.get(date, 0)
    
    while has_more:
        url = "https://tiktok-video-no-watermark10.p.rapidapi.com/index/Tiktok/searchVideoListByKeywords"

        querystring = {"keywords":{keyword},"cursor":cursor,"region":"BR","publish_time":{date},"count":"30","sort_type":"0"}

        response = requests.get(url, headers=headers, params=querystring)
        json_response = response.json()
       
        # Adiciona os dados da resposta atual à lista de todas as respostas.
        responses_list.append(json_response['data'])
        # Atualiza a variável 'has_more' com o valor correspondente da resposta para determinar se há mais páginas a serem solicitadas.
        has_more = json_response['data']['hasMore']
        # Atualiza o cursor com o valor correspondente da resposta para a próxima paginação.
        cursor = json_response['data']['cursor']
       
    # Calcula o número de páginas de dados coletados.
    pages = cursor // 30
    return filtrar_json(responses_list, pages)


def salvar_csv(dados):
    # Converter o dicionário para DataFrame
    df = pd.DataFrame.from_dict(dados, orient='index')
    st.success('Arquivo salvo com sucesso!')
    # Salvar o DataFrame em um arquivo CSV
    df.to_excel("tiktok" + '.xlsx', index_label='Video')


# Converte o timestamp do epoch para o formato de data e hora.
def converte_para_data(epoch_timestamp):
    date_time = datetime.fromtimestamp(epoch_timestamp)
    formatted_date = date_time.strftime('%d-%m-%Y %H:%M:%S')  # Formato: YYYY-MM-DD HH:MM:SS
    
    return formatted_date


def filtrar_json(dados_json, pages):
        count = 0
        info = {}

        # Loop para percorrer cada página de dados.
        for i in range(pages):
            # Loop para percorrer cada vídeo da página atual.
            for video in dados_json[i]['videos']:
                if video['region'] != 'BR':
                    continue
                nickname = video['author']['nickname'].replace(" ", "")
                code_video = video['video_id']
                link = f'https://www.tiktok.com/@{nickname}/video/{code_video}'
                visualizations = video['play_count']
                like = video['digg_count']
                downloads = video['download_count']
                comments = video['comment_count']
                shares = video['share_count']
                id_user = video['author']['id']
                region = video['region']
                time = video['create_time']
                title = video['title']
                # Adiciona os dados do vídeo atual ao dicionário 'info'.
                info[f'Vídeo: {count}'] = {
                    'Link' : link,
                    'Visualizações' : visualizations,
                    'Curtidas' : like,
                    'Comentários' : comments,
                    'Downloads' : downloads,
                    'Compartilhamentos' : shares,
                    'Data' : converte_para_data(time),
                    'ID Usuário' : id_user,
                    'Região' : region,
                    'Título' : title
                    }

                count += 1
        # Salva os dados coletados em um arquivo CSV.
        salvar_csv(info)

        return info