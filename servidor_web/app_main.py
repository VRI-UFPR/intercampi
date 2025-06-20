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

from flask import Flask
import threading
import time
import ufr
import json
import jinja2

g_app = Flask(__name__)
g_data = {}

# =============================================================================
#  Collector Thread
# =============================================================================

def main_coletor():
    global g_data
    sub = ufr.Subscriber("@new mqtt  @coder text  @host 185.159.82.136 @topic intercampi")
    while True:
        mensagem_json = sub.get("^s")
        # print(mensagem_json)
        mensagem = json.loads(mensagem_json)
        rota = mensagem['rota']
        veiculo = mensagem['veiculo']
        latitude = mensagem['lat']
        longitude = mensagem['log']
        g_data[rota] = {'coordenadas': [latitude,longitude], 'timestamp': time.now()}
        print("Coletor:", rota, g_data[rota])

# =============================================================================
#  Rotas HTML
# =============================================================================

@g_app.route('/api')
def get_api():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor em um dicionario
    '''
    return json.dumps(g_data)

@g_app.route('/api/rotas')
def get_api_rotas():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor em um vetor
    '''
    rotas = []
    for nome, item in g_data.items():
        rotas.append({'nome': nome, "coordenadas": item['coordenadas'], "descricao": item['timestamp']})
    return json.dumps(rotas)

@g_app.route('/', methods=["GET"])
def get_map():
    '''
        Mostra a posicao dos Onibus em um Mapa OpenStreet
    '''
    global g_env

    # renderiza o template mapa com os dados
    template = g_env.get_template('map.html')
    return template.render({'rotas': rotas})

# =============================================================================
#  Main
# =============================================================================

g_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),  # Procura templates na pasta 'templates'
    autoescape=True  # Ativa escape automático para segurança
)
g_thread_coletor = threading.Thread(target=main_coletor)
g_thread_coletor.start()

if __name__ == '__main__':
    g_app.run(debug=True)