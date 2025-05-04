# Intercampi

O Projeto consiste em 3 componentes: Rastreador, Armazenador e o Servidor Web.

## Componente 1: Rastreador

Transmite a informaçao do GPS para um determininado topico do servidor MQTT
  - ./rastreador_android: rastreador para celulares android
  - ./rastreador_fake: rastreador usado para testes

## Componente 2: Armazenador

Le o topico e armazena todos os dados recebidos em um arquivo SQLite3

./armazenador: implementaçao em python do armazenador

## Componente 3: Servidor Web

Le o topico e publica os dados atualizados sobre uma API REST 

./servidor_web: implementaçao em Python e Flask

## Requisitos
- [Rastreador]: O aplicativo enviar mensagem quando houver alteraçao de posicao de mais de 20m
- [Rastreador]: O aplicativo deve ter a menor quantidade de interacao com o motorista. E principalmente estar funcionando quando ligar o celular.
- [Rastreador]: O motorista pode alterar o nome da rota
- [Rastreador]: O motorista pode alterar o nome do onibus
- [ServidorWeb]: Mostrar a posicao (Latidude e Longitude) de todos os veiculos
- [ServidorWeb]: Mostrar a posicao (Latidude e Longitude) de um veiculo
- [ServidorWeb]: Mostrar quando foi o ultimo envio da posicao de um veiculo
- [ServidorWeb][depuracao]: Mostrar a posicao (Latidude e Longitude) de todos os veiculos em um mapa openstreetmap
- [ServidorWeb]: Mostrar a trajetoria de um veiculo durante todo um especifico dia

## Tarefas
- [Rastreador_fake]: Fazer uma rota usando o Android Studio. E depois exportar os dados do GPS dessa rota para um arquivo. Entao ler esse arquivo no python e publicar esses dados para o MQTT via python.

## Testes
- [ServidorWeb]: colocar o rastreador fake e verificar se o servidor web estah recebendo os dados