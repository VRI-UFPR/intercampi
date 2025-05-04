# Rastreador Fake 

Este script em python que envia posicoes falsas de um veiculo fantasma. Esse script pode ser usado para testar o armazenador e o servidor.

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