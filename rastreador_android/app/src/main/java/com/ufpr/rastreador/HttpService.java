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

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.io.IOException;

// =================================================================================================
//  Public Class MqttService
// =================================================================================================

public class HttpService {

    private final OkHttpClient client = new OkHttpClient();

    // Atributos publicos
    public boolean isConnected = false;

    // Constates Configuraveis

    // IP e Porta do servidor HTTP
    private final String URL = "http://10.4.0.2:5000/api";

    // Log
    private String TAG = "HTTP";

    public static final MediaType JSON = MediaType.get("application/json; charset=utf-8");

    // Atributos inicializados pelos parametros do construtor
    private String onibus_id;
    private String rota_id;

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
    public HttpService(String onibus_id, String rota_id, MainActivity context) {
        this.onibus_id = onibus_id;
        this.rota_id = rota_id;
        this.main_activity = context;
        this.handler = new Handler(Looper.getMainLooper());

        //teste this.pub_location(10.0, 10.0);
    }

    /**
     * Publica a localização do veiculo
     *
     * @param lat latitude do veiculo
     * @param log longitude do veiculo
     */
    public void pub_location(double lat, double log) {
        Coordinates coordinates = new Coordinates(this.rota_id, this.onibus_id, lat, log);
        String json = gson.toJson(coordinates);
        Log.i(TAG, json);

        // Cria o corpo da requisição com o JSON
        RequestBody body = RequestBody.create(json, JSON);

        // Constrói a requisição POST
        Request request = new Request.Builder()
            .url(URL)
            .post(body)
            .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                // Erro na requisição (ex: sem conexão, timeout)
                Log.e(TAG, "Falha na requisição POST", e);
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                // A resposta foi recebida do servidor
                if (response.isSuccessful()) {
                    // A resposta foi bem-sucedida (código 2xx)
                    String responseBody = response.body().string();
                    Log.d(TAG, "Resposta do servidor: " + responseBody);

                    // Envia o horario para MainActivity para mostrar na tela
                    String horaAtual = sdf.format(new Date());
                    handler.post(() -> main_activity.updateLastSentText( horaAtual ));
                } else {
                    // O servidor respondeu com um erro (código 3xx, 4xx, 5xx)
                    Log.e(TAG, "Resposta inesperada do servidor: " + response);
                }
            }
        });
    }

}