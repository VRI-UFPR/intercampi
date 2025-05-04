# Armazenador 

Este script em python monitora um topico especifico do MQTT e guarda em um arquivo SQLITE todas as mensagens recebidas.

## Dependencias

1. Instalar a biblioteca Mosquisto-dev
```
sudo apt install mosquitto-dev
```

2. Instalar a biblioteca UFR 
```
git clone https://github.com/VRI-UFPR/ufr
cd ufr
mkdir build
cmake ..
make
sudo make install
```

3. Instalar o wrapper da biblioteca UFR
```shell
pip3 install ufr
```

## Execucao

```
python3 main.py
```