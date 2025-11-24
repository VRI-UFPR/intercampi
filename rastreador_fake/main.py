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

import requests
import json
import time
import sys

HOST = "172.19.0.3"
HOST_URL = f"http://{HOST}:5000/api"

# =============================================================================
#  Main
# =============================================================================

# 0. Le os parametros de entrada (Nome da Rota e do Onibus)
try:
    nome_rota = sys.argv[1]
except:
    nome_rota = "intercampi_falso"

try:
    nome_onibus = sys.argv[2]
except:
    nome_onibus = "onibus_falso"

# 1. Le os dados da rota a partir de um JSON
fd = open('rota1.json')
rota = json.loads(fd.read())
fd.close()

# 2. Publica todas as coordenadas, uma a cada 5 segundos
for coordinate in rota['coordinates']:
    # 2.1. monta a mensagem
    mensagem = {
        'rota': nome_rota, 
        'veiculo': nome_onibus, 
        'lat': coordinate[1], 'log': coordinate[0],
        'vbat': 40
    }

    # 2.2. envia a mensagem
    response_json = requests.post(HOST_URL, json=mensagem)
    if response_json.status_code == 200:
        message = response_json.json()
        if message['status'] == 'ok':
            print(mensagem)
        else:
            print(message)
    else:
        print(f"Error: {response_json.status_code} - {response_json.text}")

    # 2.3. espera 5 segundos    
    time.sleep(5)