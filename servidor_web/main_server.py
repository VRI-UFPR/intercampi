# This file is part of the Intercampi (https://github.com/VRI-UFPR/intercampi)
# Copyright (c) 2025 VRI
#  - Felipe Gustavo Bombardelli
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# =============================================================================
#  Header
# =============================================================================

import os
import threading
import time
import json
import jinja2

from flask import Flask, request
from flask_cors import CORS
from datetime import datetime

g_app = Flask(__name__)
g_cors = CORS(g_app)

g_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./templates'),
    autoescape=True  # Ativa escape automático para segurança
)

# =============================================================================
#  Database
# =============================================================================

class Database:
    def __init__(self):
        self.dados = {}

    def salva_coordenadas(self, rota, veiculo, latitude, longetude):       
        timestamp = datetime.now().timestamp()

        # cria e guarda em um dicionario global
        item = {'nome': rota, 'veiculo': veiculo}
        item['coordenadas'] = (latitude, longetude)
        item['timestamp'] = str(timestamp)
        item['vbat'] = 0
        self.dados[rota] = item
        
        # salva os dados em um arquivo
        item_json = json.dumps(item)
        fd = open(f"./database/{rota}", "w")
        fd.write(item_json)
        fd.close()

    def onibus(self, rota):
        """
            Retorna um dicionario com os dados de um onibus especifico com 
            sua ultima posição de GPS registrada.

            {'rota': %s, 'veiculo': %s, 'coordenadas': (latidude, longetude), vbat: %f, 'timestamp': %s}
        """

        if rota in self.dados:
            resultado = self.dados[rota]
        else:
            resultado = {'nome': '', 'veiculo': '', 'latitude': 0, 'longitude': 0, 'vbat': 0, 'timestamp': 0}
        return resultado

    def todos_onibus(self):
        return self.dados.values()


G_DB = Database()

# =============================================================================
#  API HTML
# =============================================================================

@g_app.route('/api/onibus')
def get_api_onibus():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor em um vetor

        [
            {'rota': %s, 'veiculo': %s, 'coordenadas': (latidude, longetude), 'vbat': %f, 'timestamp': %s}
            ...
            {'rota': %s, 'veiculo': %s, 'coordenadas': (latidude, longetude), 'vbat': %f, 'timestamp': %s}
        ]

        timestamp: (String) => %Y-%m-%d %H:%M:%S
    '''

    rotas = []
    for item in G_DB.todos_onibus():
        rotas.append({
            'nome': item['veiculo'], 
            "coordenadas": item['coordenadas'], 
            "descricao": item['timestamp']
        })
    return json.dumps(rotas)

@g_app.route('/api/onibus/<onibus_id>')
def get_api_onibus_id(onibus_id):
    '''
        Retorna a lista de um onibus especifico e sua ultima posição do GPS 
        recebidas pelo servidor.

        {'rota': %s, 'veiculo': %s, 'coordenadas': (latidude, longetude), 'vbat': %f, 'timestamp': %s}
    '''

    onibus = G_DB.onibus(onibus_id)
    return json.dumps(onibus)

@g_app.route('/api/rotas')
def get_api_rotas():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor em um vetor
    '''

    return json.dumps([])

@g_app.route('/api', methods=["POST"])
def post_api():
    '''
        Insere um nova rota
    '''

    try:
        data = request.get_json()
        rota = data["rota"]
        veiculo = data["veiculo"]
        latitude = data["lat"]
        longetude = data["log"]
        G_DB.salva_coordenadas(rota,veiculo,latitude,longetude)
        return json.dumps({'status': 'ok'})
    except Exception as error:
        return json.dumps({'status': 'error', 'message': str(error)})


# =============================================================================
#  Paginas HTML
# =============================================================================

@g_app.route('/', methods=["GET"])
def get_index():
    '''
        Mostra a posicao dos Onibus em um Mapa OpenStreet
    '''
    global g_env

    # renderiza o template mapa com os dados
    template = g_env.get_template('map.html')
    dados = G_DB.todos_onibus()
    return template.render({'rotas': dados})

# =============================================================================
#  Main
# =============================================================================

if __name__ == '__main__':
    g_app.run(debug=True)