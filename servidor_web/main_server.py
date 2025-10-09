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
import psycopg2

from flask import Flask, request
from flask_cors import CORS
from datetime import datetime

## Habilitar essas variaveis, caso execute via docker 
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

## Habilitar essa variaveis caso execute diretamente
# POSTGRES_HOST = '10.2.0.2'
# POSTGRES_DB = 'vri'
# POSTGRES_USER = 'vri'
# POSTGRES_PASSWORD = 'mudar123'

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
        self.create_tables_if_not_exists()

    def get_connection(self):
        if POSTGRES_HOST == "":
            raise Exception("POSTGRES_HOST nao está definido")

        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        return conn

    def create_tables_if_not_exists(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coordenadas (
                rota VARCHAR(256) NOT NULL,
                veiculo VARCHAR(256) NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.close()
        conn.commit()
        conn.close()

    def insere_coordenadas(self, rota, veiculo, latitude, longitude):
        conn = self.get_connection()
        cursor = conn.cursor()
        sql_command = f"INSERT INTO coordenadas (rota, veiculo, latitude, longitude) VALUES (%s, %s, %s, %s);"
        cursor.execute(sql_command, (rota, veiculo, latitude, longitude))
        cursor.close()
        conn.commit()
        conn.close()

    def onibus(self, onibus_id):
        """
            Retorna um dicionario com os dados de um onibus especifico com 
            sua ultima posição de GPS registrada.
        """

        # Executa o SQL
        conn = self.get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT rota,veiculo,latitude,longitude,timestamp FROM coordenadas 
                WHERE veiculo = %s and (rota, timestamp) IN 
                    (SELECT rota, MAX(timestamp) FROM coordenadas GROUP BY rota);
        """
        cursor.execute(sql, (onibus_id,))
        
        # Prepara uma lista de dicionarios
        rows = cursor.fetchall()
        if len(rows) == 0:
            return {}

        for row in rows:
            val = {
                'rota': row[0], 
                'veiculo': row[1], 
                'coordenadas': (row[2],row[3]), 
                'timestamp': row[4].strftime("%Y-%m-%d %H:%M:%S")
            }
            print(val)

        # Retorna o resultado
        return val

    def todos_onibus(self):
        # Executa o SQL
        conn = self.get_connection()
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
                'timestamp': row[4].strftime("%Y-%m-%d %H:%M:%S")
            }
            result.append(val)

        # Retorna o resultado
        return result

    def historico_do_onibus(self, onibus):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coordenadas WHERE veiculo = %s", (onibus,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)

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
            {'veiculo': %s, 'rota': %s, 'coordenadas': (latidude, longetude), 'timestamp': %s}
            ...
            {'veiculo': %s, 'rota': %s, 'coordenadas': (latidude, longetude), 'timestamp': %s}
        ]
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

        {'veiculo': %s, 'rota': %s, 'coordenadas': (latidude, longetude), 'timestamp': %s}
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
        longitude = data["log"]
        G_DB.insere_coordenadas(rota,veiculo,latitude,longitude)
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