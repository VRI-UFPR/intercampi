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

g_app = Flask(__name__)

# =============================================================================
#  Rotas HTML
# =============================================================================

@g_app.route('/')
def index():
    '''
        Retorna a lista de todos os intercampi e suas ultimas posições GPS
        recebidas pelo servidor.
    '''
    return 'Hello, World!'

@g_app.route('/', methods=["PUT"])
def put_location():
    '''
        Adiciona posicao de um onibus para a base de dados
    '''
    return 'Hello, World!'

g_app.run()