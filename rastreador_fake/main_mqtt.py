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
import json
import time
import sys

MSG_HEARTBEAT = 1
MSG_SEND = 2

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

# 2. Abre o publicador MQTT 
pub = ufr.Publisher("@new mqtt @coder msgpack @host 177.153.62.174 @topic /ufpr/intercampi")

# 3. Publica todas as coordenadas, uma a cada 5 segundos
for coordinate in rota['coordinates']:
    longitude = coordinate[0]
    latidude = coordinate[1]
    pub.put("%d %s %f %f\n", MSG_SEND, 'onibus_falso', latidude, longitude)
    time.sleep(5)

# 4. Fecha o publicador
pub.close()
