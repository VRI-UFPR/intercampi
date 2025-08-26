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

import ufr
import sqlite3
import json

# =============================================================================
#  Funcoes
# =============================================================================

def abre_sqlite():
    """Cria a tabela no banco de dados se ela não existir"""
    conn = sqlite3.connect('basedados.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS coordenadas (
        rota VARCHAR(256) NOT NULL,
        veiculo VARCHAR(256) NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        timestamp DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    return conn


# =============================================================================
#  Main
# =============================================================================

print("Inicializando")
sub = ufr.Subscriber("@new mqtt  @coder text  @host 185.159.82.136 @topic intercampi")
conn = abre_sqlite()
cursor = conn.cursor()

print("Pronto")
while True:
    mensagem_json = sub.get("^s")
    # print(mensagem_json)
    mensagem = json.loads(mensagem_json)
    rota = mensagem['rota']
    veiculo = mensagem['veiculo']
    latitude = mensagem['lat']
    longitude = mensagem['log']
    print(mensagem)

    cursor.execute('''INSERT INTO coordenadas (rota, veiculo, latitude, longitude) VALUES (?, ?, ?, ?)''', 
        (rota, veiculo, latitude, longitude))
    conn.commit()
