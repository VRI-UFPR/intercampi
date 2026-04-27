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

import ufr
import requests
from datetime import datetime
import pathlib
from datetime import datetime

HOST_URL = "http://200.17.212.40:1883/api"

# =============================================================================
#  Funções Privadas
# =============================================================================

def send_http_server(rota, onibus, latitude, longetude):
    mensagem = {
        'rota': rota, 
        'veiculo': onibus, 
        'lat': latitude, 'log': longetude,
        'vbat': -1
    }

    # 2.2. envia a mensagem
    response_json = requests.post(HOST_URL, json=mensagem)
    if response_json.status_code == 200:
        message = response_json.json()
        if message['status'] != 'ok':
            print(mensagem)
    else:
        print(f"Error: {response_json.status_code} - {response_json.text}")


class Database:
    def __init__(self, path_to_directory: str):
        self.root = pathlib.Path(path_to_directory)
        pathlib.Path(self.root).mkdir(parents=True, exist_ok=True)

    def save(self, rota: str, latidude: float, longitude: float):
        # cria a pasta para a rota
        rota_path = self.root / rota
        pathlib.Path(rota_path).mkdir(parents=True, exist_ok=True)

        # Salva a mensagem no arquivo
        time = datetime.now()
        current_day = time.strftime("%Y-%m-%d")
        file = rota_path / f"{current_day}.csv"
        fd = open(file, "a+")
        current_time = time.strftime("%H-%M-%S")
        fd.write( f"{current_time}; {latidude}; {longitude}\n" )
        fd.close()

# =============================================================================
#  Main
# =============================================================================

database = Database("./database")
link = ufr.subscriber("@new mqtt @coder msgpack @host 177.153.62.174 @topic /ufpr/intercampi")

while ufr.loop():
    pack = link.get("> %d %s")
    if pack[0] == 1:
        now = datetime.now()
        rota = pack[1]
        bateria = link.get("%d")
        print(f"[{now}] HB {rota} {bateria}")
    else:
        now = datetime.now()
        rota = pack[1]
        pack = link.get("%f %f")
        latidude = pack[0]
        longitude = pack[1]
        print(now, rota, pack)
        database.save(rota, latidude, longitude)
        send_http_server(rota, rota, latidude, longitude)