/*
 *  Rastreador do Intercampi UFPR
 *  Copyright (C) 2025 Visao Robotica e Imagem (VRI)
 *  - Felipe Gustavo Bombardelli <felipebombardelli@gmail.com>
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 * * */

// =================================================================================================
//  Header
// =================================================================================================

package com.ufpr.rastreador;

import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import com.google.gson.Gson;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.StandardCharsets;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

// =================================================================================================
//  Public Class MqttService
// =================================================================================================

public class MqttService {
    // Atributos publicos
    public boolean isConnected = false;

    // Constates Configuraveis

    // IP e Porta do servidor MQTT - mantenha o padrão IP:PORT
    private final String HOST_PORT = "185.159.82.136:1883";

    // Nome do topico para o envio da localização do veiculo
    private final String TOPIC = "location";

    // Nome do topico que recebe os comandos do servidor terminal
    private final String TOPIC_CMD_REQ = "command_req";

    // Nome do topico que envia o resultado dos comandos recebidos pelo TOPIC_CMD_REQ
    private final String TOPIC_CMD_ANS = "command_ans";

    // Variaveis de Reconexao
    private int reconnectDelay = 1000;
    private final int maxReconnectDelay = 60000;

    // Log
    private String TAG = "MQTT";

    // Atributos inicializados pelos parametros do construtor
    private String onibus_id;
    private String rota_id;

    // Atributos privados
    private MqttClient client;   //< conexao com o MQTT
    private Gson gson = new Gson();
    private Handler handler;
    private MainActivity main_activity = null;
    private SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss dd/MM/yyyy",
            Locale.getDefault());

    /**
     * Construtor do objeto para envio dos dados via MQTT
     *
     * @param onibus_id id do onibus
     * @param rota_id id da rota
     * @param context ponteiro da atividade MainActivity usado para atualizar as informações da tela
     */
    public MqttService(String onibus_id, String rota_id, MainActivity context) {
        this.onibus_id = onibus_id;
        this.rota_id = rota_id;
        this.main_activity = context;
        this.handler = new Handler(Looper.getMainLooper());
    }

    /**
     * Conecta o objeto MQTT com o servidor
     */
    public void connect() {
        String connectionUri = "tcp://" + HOST_PORT;
        String clientId = MqttClient.generateClientId();
        try {
            // Conecta ao servidor MQTT
            client = new MqttClient(connectionUri, "onibus1", null);
            MqttConnectOptions options = new MqttConnectOptions();
            options.setKeepAliveInterval(180);
            options.setConnectionTimeout(30);
            client.connect(options);

            // Envia para MainActivity a mensagem para mostrar na tela
            handler.post(() -> main_activity.updateStatusText( HOST_PORT ));

            // Assina o topico de comando
            client.subscribe(TOPIC_CMD_REQ, 0);

            // Associa os callbacks para os eventos
            client.setCallback(new MqttCallbackExtended() {
                @Override
                public void connectComplete(boolean reconnect, String serverUri) {
                    isConnected = true;
                    reconnectDelay = 1000; // Reseta o delay após conexão bem-sucedida
                    Log.d("MQTT", "Conectado! Reconexão automática: " + reconnect);
                }

                @Override
                public void connectionLost(Throwable cause) {
                    isConnected = false;
                    Log.e("MQTT", "Conexão perdida. Tentando reconectar...");
                    handler.post(() -> main_activity.updateStatusText( "reconectando" ));
                    scheduleReconnect();
                }

                @Override
                public void messageArrived(String topic, MqttMessage message) {
                    String payload = new String(message.getPayload());
                    Log.d("MQTT", "Mensagem recebida: " + payload.length() + " [Tópico: " + topic + "]");

                    if ( payload.substring(0,4).equals("ping") ) {
                        handler.post(() -> main_activity.updateStatusText("ping"));
                        pub_answer("OK");
                    } else {
                        Log.d("MQTT", "Comando nao encontrado");
                    }

                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {
                    // Log.d("MQTT", "Entrega da mensagem concluída");
                }
            });

        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * Desconecta o cliente do servidor MQTT
     */
    public void disconnect() {
        if (client != null && client.isConnected()) {
            try {
                client.disconnect();
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * Envia uma string como resposta a uma requisição do servidor MQTT
     *
     * @param msg mensagem a ser enviada
     */
    public void pub_answer(String msg) {
        try {
            client.publish(TOPIC_CMD_ANS, msg.getBytes(), 0, false);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * Publica a localização do veiculo
     *
     * @param lat latitude do veiculo
     * @param log longitude do veiculo
     */
    public void pub_location(double lat, double log) {
        try {
            Coordinates coordinates = new Coordinates(this.onibus_id, lat, log);
            String json = gson.toJson(coordinates);
            Log.i("JSON",json);
            MqttMessage message = new MqttMessage(json.getBytes(StandardCharsets.UTF_8));
            client.publish(TOPIC, message);

            // Envia o horario para MainActivity para mostrar na tela
            String horaAtual = sdf.format(new Date());
            handler.post(() -> main_activity.updateLastSentText( horaAtual ));
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * Reconecta o cliente MQTT
     */
    private void scheduleReconnect() {
        if (!isConnected) {
            handler.postDelayed(() -> {
                Log.d("MQTT", "Tentando reconectar... Delay: " + reconnectDelay + "ms");
                try {
                    if (client != null && !client.isConnected()) {
                        client.reconnect();
                        handler.post(() -> main_activity.updateStatusText( HOST_PORT ));
                    }
                } catch (MqttException e) {
                    Log.e("MQTT", "Falha na reconexão: " + e.getMessage());
                    // Aumenta o delay exponencialmente (com limite máximo)
                    reconnectDelay = Math.min(reconnectDelay * 2, maxReconnectDelay);
                    scheduleReconnect();
                }
            }, reconnectDelay);
        }
    }

}