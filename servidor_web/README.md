# Servidor Web do Rastreamento do Intercampi

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

4. Instalar o Flask e o Jinja2
```
pip3 install flask jinja2
```


## Execução

```
python3 main.py
```