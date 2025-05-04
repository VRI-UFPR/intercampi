# This file is part of the Intercampi Project (https://github.com/)
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

# =============================================================================
#  Main
# =============================================================================

pub = ufr.Publisher("@new mqtt @coder text @host 185.159.82.136 @topic intercampi")
log = 23.000
while True:
    mensagem = {'rota': 'intercampi_falso', 'veiculo': 'onibus_falso', 'lat': 12.333, 'log': log}
    texto_json = json.dumps(mensagem)
    print(texto_json)
    pub.put("s\n", texto_json)
    time.sleep(5)

    log += 0.0001


