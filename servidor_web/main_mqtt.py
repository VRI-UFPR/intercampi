import ufr
import requests
from datetime import datetime

HOST_URL = "http://200.17.212.40:1883/api"


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
        if message['status'] == 'ok':
            print(mensagem)
        else:
            print(message)
    else:
        print(f"Error: {response_json.status_code} - {response_json.text}")







link = ufr.subscriber("@new mqtt @coder msgpack @host 177.153.62.174 @topic /ufpr/intercampi")

while ufr.loop():
    pack = link.get("> %d %s")
    if pack[0] == 1:
        now = datetime.now()
        print(f"[{now}] HB {pack[1]}")
    else:
        now = datetime.now()
        rota = pack[1]
        pack = link.get("%f %f")
        print(now, rota, pack)
        send_http_server(rota, rota, pack[0], pack[1])