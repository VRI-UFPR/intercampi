# VRI
# This file is part of the XXX distribution (https://github.com/xxxx 
# or http://xxx.github.io)
# Copyright (c) 2025 Felipe Gustavo Bombardelli
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

g_app = Flask(__name__)
g_data = {}

# =============================================================================
#  Collector thread
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
        g_data[rota] = [latitude,longitude]
        print("Coletor:", rota, g_data[rota])

# =============================================================================
#  Rotas HTML
# =============================================================================

@g_app.route('/')
def index():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor.
    '''
    return json.dumps(g_data)

@g_app.route('/', methods=["PUT"])
def put_location():
    '''
        Adiciona posicao de um onibus para a base de dados
    '''
    return 'Hello, World!'

# Criando a thread
# thread_coletor = threading.Thread(target=main_coletor, args=(,))
thread_coletor = threading.Thread(target=main_coletor)
thread_coletor.start()
g_app.run()