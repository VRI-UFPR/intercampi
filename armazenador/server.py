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
#  Main
# =============================================================================

print("Inicializando")
req = ufr.server("@new zmq @coder msgpack @host 0.0.0.0")
conn = sqlite3.connect('file:basedados.sqlite?mode=ro')
cursor = conn.cursor()

print("Pronto")
while ufr.loop():
    mensagem_json = req.get("^s\n")
    req.put("s#", "OK")

req.close()
