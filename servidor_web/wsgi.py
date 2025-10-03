# wsgi.py
import sys
import logging

# Configura o log para WSGI (útil para depuração)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# Adicione o diretório do seu projeto ao PYTHONPATH
sys.path.insert(0, "/usr/local/lib/python3.10/site-packages")
sys.path.insert(0, '/app')

## Ative o ambiente virtual
## Substitua '/var/www/meuprojeto_flask/venv' pelo caminho real do seu venv
# activate_this = '/var/www/intercampi/servidor_web/venv/bin/activate_this.py'
# with open(activate_this) as f:
#    exec(f.read(), dict(__file__=activate_this))

# Importe sua aplicação Flask
# Certifique-se de que 'g_app' corresponde ao nome da sua instância Flask no app_main.py
from main_server import g_app as application
