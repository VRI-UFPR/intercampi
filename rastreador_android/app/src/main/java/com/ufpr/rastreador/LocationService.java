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

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.os.Binder;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;

// =================================================================================================
//  class LocationService extends Service
// =================================================================================================

public class LocationService extends Service {
    // Constantes configuraveis
    private final int LOCATION_INTERVAL_MS = 5000;  // 5000ms atualizacao do GPS
    private final int LOCATION_DISTANCE = 20;    // 20m de mudanca

    // Objetos Dependentes
    private MqttService mqtt = null;
    private final LocationServiceBinder binder = new LocationServiceBinder();

    // Metodos privados
    private LocationListener locationListener;
    private LocationManager locationManager;
    private NotificationManager notificationManager;

    // log
    private final String TAG = "LocationService";

    // =============================================================================================
    //  Metodos Publicos
    // =============================================================================================

    /**
     * Ativa o rastreio do onibus
     * @param onibus_id id no onibus, exemplo: "onibus1"
     * @param rota_id id da rota, exemplo: "intercampi1"
     * @param p_main_activity ponteiro da atividade main para atualizar as informações lá
     */
    public void startTracking(String onibus_id, String rota_id, MainActivity p_main_activity) {
        // Inicializa o serviço de tracking
        initializeLocationManager();
        locationListener = new LocationListener(LocationManager.GPS_PROVIDER);
        if ( locationListener == null ) {
            return;
        }

        // Inicializa o serviço do GPS para atualizar quando houver mudança na leitura ou por
        // periodo
        try {
            locationManager.requestLocationUpdates(
                    LocationManager.GPS_PROVIDER,
                    LOCATION_INTERVAL_MS,
                    LOCATION_DISTANCE,
                    locationListener);
        } catch (SecurityException ex) {
            Log.i(TAG, "fail to request location update, ignore", ex);
        } catch (IllegalArgumentException ex) {
            Log.d(TAG, "gps provider does not exist " + ex.getMessage());
        }

        // Inicializa a Comunicaçao MQTT
        mqtt = new MqttService(onibus_id, rota_id, p_main_activity);
        mqtt.connect();
    }

    /**
     * Desativa o rastreio
     */
    public void stopTracking() {
        mqtt.disconnect();
        this.onDestroy();
    }

    // =============================================================================================
    //  Metodos Auxiliares
    // =============================================================================================

    public class LocationServiceBinder extends Binder {
        public LocationService getService() {
            return LocationService.this;
        }
    }

    private void initializeLocationManager() {
        Log.i(TAG, "initializeLocationManager - LOCATION_INTERVAL: " +
                LOCATION_INTERVAL_MS + " LOCATION_DISTANCE: " + LOCATION_DISTANCE);
        if (locationManager == null) {
            locationManager = (LocationManager) getApplicationContext()
                    .getSystemService(Context.LOCATION_SERVICE);
        }
    }

    /**
     * Nao sei para que serve, mas eh necessario
     * @return
     */
    private Notification getNotification() {
        NotificationChannel channel = new NotificationChannel("channel_01", "GPS Channel",
                NotificationManager.IMPORTANCE_DEFAULT);
        NotificationManager notificationManager = getSystemService(NotificationManager.class);
        notificationManager.createNotificationChannel(channel);
        Notification.Builder builder = new Notification.Builder(getApplicationContext(),
                "channel_01").setAutoCancel(true);
        return builder.build();
    }

    // =============================================================================================
    //  Metodos Callbacks
    // =============================================================================================

    @Override
    public IBinder onBind(Intent intent) {
        return binder;
    }

    /**
     * Callback para o evento de criação do Serviço
     */
    @Override
    public void onCreate() {
        Log.i(TAG, "Created");
        startForeground(12345678, getNotification());
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (locationManager != null)
            try {
                locationManager.removeUpdates(locationListener);
            } catch (Exception ex) {
                Log.i(TAG, "fail to remove location listners, ignore", ex);
            }
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        super.onStartCommand(intent, flags, startId);
        return START_NOT_STICKY;
    }

    // =============================================================================================
    //  Subclasse LocationListener
    // =============================================================================================

    private class LocationListener implements android.location.LocationListener {
        private final String TAG = "LocationListener";
        private Location lastLocation;

        /**
         * Construtor de LocationListener
         * @param provider
         */
        public LocationListener(String provider) {
            lastLocation = new Location(provider);
        }

        // =========================================================================================
        //  Callbacks para a subclasse LocationListener
        // =========================================================================================

        /**
         * Evento executado quando a posicao do GPS muda mais do que 20m ()
         * @param[in] location the updated location
         */
        @Override
        public void onLocationChanged(Location location) {
            lastLocation = location;
            mqtt.pub_location( location.getLatitude(), location.getLongitude() );
        }

        /**
         * Chamado quando o Provedor com o qual este ouvinte está registrado fica desativado.
         * @param provider the name of the location provider
         */
        @Override
        public void onProviderDisabled(String provider) {
            Log.e(TAG, "onProviderDisabled: " + provider);
        }

        /**
         * Chamado quando um provedor com o qual este ouvinte está registrado é ativado.
         * @param provider the name of the location provider
         */
        @Override
        public void onProviderEnabled(String provider) {
            Log.e(TAG, "onProviderEnabled: " + provider);
        }

        /**
         * Este método foi descontinuado na API de Nível 29. Este retorno de chamada nunca será
         * invocado no Android Q e superior.
         *
         * @param provider
         * @param status
         * @param extras
         */
        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
            Log.e(TAG, "onStatusChanged: " + status);
        }
    }
}
