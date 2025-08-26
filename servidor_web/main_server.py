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
import sqlite3

g_app = Flask(__name__)

# =============================================================================
#  Database
# =============================================================================

class Database:
    def __init__(self, filename):
        self.filename = filename

    def todos_onibus(self):
        # Executa o SQL
        conn = sqlite3.connect(f'file:{self.filename}?mode=ro', uri=True)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rota,veiculo,latitude,longitude,timestamp FROM coordenadas 
                WHERE (rota, timestamp) IN 
                    (SELECT rota, MAX(timestamp) FROM coordenadas GROUP BY rota);  
        """)
        
        # Prepara uma lista de dicionarios
        rows = cursor.fetchall()
        result = []
        for row in rows:
            val = {
                'rota': row[0], 
                'veiculo': row[1], 
                'coordenadas': (row[2],row[3]), 
                'timestamp': row[4]
            }
            result.append(val)

        # Retorna o resultado
        return result

    def historico_do_onibus(self, onibus):
        conn = sqlite3.connect(f'file:{self.filename}?mode=ro', uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordenadas WHERE veiculo = ?", (onibus,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

G_DB = Database('basedados.sqlite')

# =============================================================================
#  Rotas HTML
# =============================================================================

@g_app.route('/api')
def get_api():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor em um dicionario
    '''
    dados = G_DB.todos_onibus()
    return json.dumps(dados)

@g_app.route('/api/rotas')
def get_api_rotas():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor em um vetor
    '''

    rotas = []
    for item in G_DB.todos_onibus():
        rotas.append({'nome': item['veiculo'], "coordenadas": item['coordenadas'], "descricao": item['timestamp']})
    return json.dumps(rotas)

@g_app.route('/', methods=["GET"])
def get_map():
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

g_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),  # Procura templates na pasta 'templates'
    autoescape=True  # Ativa escape automático para segurança
)

if __name__ == '__main__':
    g_app.run(debug=True)