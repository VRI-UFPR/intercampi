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

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.IBinder;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.os.Handler;
import android.os.Looper;

// =================================================================================================
//  Main
// =================================================================================================

public class MainActivity extends AppCompatActivity {
    // Componentes da tela
    public TextView statusText;
    public TextView onibusText;
    public TextView rotaText;
    public TextView lastSentText;
    private Button startButton;
    private Button stopButton;

    // Servico de fundo do GPS junto com o MQTT
    public LocationService gps;

    // Usado para mostrar as variaveis vindo do servico GPS
    private Handler handler;

    // log
    private final String TAG = "Main";

    // =============================================================================================
    //  Callbacks
    // =============================================================================================

    /** Callback para o evento de inicialização do aplicativo. Esta função é chamado automaticamente
     * pelo Android quando o aplicativo é inicializado.
     *
     * @param savedInstanceState If the activity is being re-initialized after
     *     previously being shut down then this Bundle contains the data it most
     *     recently supplied in {@link #onSaveInstanceState}.  <b><i>Note: Otherwise it is null.</i></b>
     *
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Get view objects
        statusText = (TextView) findViewById(R.id.statusText);
        onibusText = (EditText) findViewById(R.id.onibusText);
        rotaText = (EditText) findViewById(R.id.rotaText);
        lastSentText = (TextView) findViewById(R.id.lastSentText);
        startButton = (Button) findViewById(R.id.startButton);
        stopButton = (Button) findViewById(R.id.stopButton);

        checkLocationPermissions();

        // start automatically
        startButton.setEnabled(false);
        rotaText.setEnabled(false);
        onibusText.setEnabled(false);

        // Actions when start button is clicked
        startButton.setOnClickListener(v -> {
            if ( gps != null ) {
                gps.startTracking(
                        onibusText.getText().toString(),
                        rotaText.getText().toString(),
                        this);
                startButton.setEnabled(false);
                stopButton.setEnabled(true);
                statusText.setText("conectando");
                rotaText.setEnabled(false);
                onibusText.setEnabled(false);
            } else {
                Toast.makeText(this, "Erro no serviço de GPS", Toast.LENGTH_LONG).show();
                Log.e(TAG, "GPS está nulo, ocorreu um erro ao criar o serviço de GPS");
            }
        });

        // Actions when stop button is clicked
        stopButton.setOnClickListener(v -> {
            if ( gps != null ) {
                gps.stopTracking();
                startButton.setEnabled(true);
                stopButton.setEnabled(false);
                statusText.setText("desligado");
                rotaText.setEnabled(true);
                onibusText.setEnabled(true);
            } else {
                Toast.makeText(this, "Erro no serviço de GPS", Toast.LENGTH_LONG).show();
                Log.e(TAG, "GPS está nulo, ocorreu um erro ao criar o serviço de GPS");
            }
        });

        handler = new Handler(Looper.getMainLooper());
    }

    /**
     * Callback para o evento de pedido de permissão. Esta função é chamado pelo Android quando
     * o sistema requer alguma permissão do usuario, como o acesso ao GPS
     *
     * @param requestCode The request code passed in {@link #requestPermissions(
     * android.app.Activity, String[], int)}
     * @param permissions The requested permissions. Never null.
     * @param grantResults The grant results for the corresponding permissions
     *     which is either {@link android.content.pm.PackageManager#PERMISSION_GRANTED}
     *     or {@link android.content.pm.PackageManager#PERMISSION_DENIED}. Never null.
     *
     */
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        Log.i("CODE", String.valueOf(requestCode));
        for (String p : permissions)
            Log.i("PERMISSIONS", String.valueOf(p));
        for (int g : grantResults)
            Log.i("RESULTS", String.valueOf(g));
        boolean granted = false;
        if (requestCode == 1) {
            //For each permission requested
            for (int i = 0, len = permissions.length; i < len; i++) {
                String permission = permissions[i];
                // If user denied the permission
                if (grantResults[i] == PackageManager.PERMISSION_DENIED) {
                    //Check if you asked for the same permissions before
                    boolean showRationale = shouldShowRequestPermissionRationale(permission);
                    //If user cheked "nevers ask again"
                    if (!showRationale) {
                        startButton.setEnabled(false);
                        stopButton.setEnabled(false);
                        statusText.setText("No access to GPS");
                        Toast.makeText(this, "GPS Location access was rejected", Toast.LENGTH_LONG);
                    }
                    //If user hasn't checked for "never ask again"
                    else checkLocationPermissions();
                }
                //user grants permissions
                else granted = true;
            }
            //If user grants permissions
            if(granted) startLocationService();

        }
    }

    // =============================================================================================
    //  Funcoes Auxiliares
    // =============================================================================================

    /**
     * Funcao privada que cria a janelinha pedindo a permissao do GPS do aparelho
     */
    private void checkLocationPermissions() {
        //if we have permission to access to gps location
        if (ContextCompat.checkSelfPermission(this,
                android.Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED &&
                ContextCompat.checkSelfPermission(this,
                        android.Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {

            // start location service
            startLocationService();
        } else {
            //If do not have location access then request permissions
            ActivityCompat.requestPermissions(this, new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION}, 1);
        }

    }

    /**
     * Cria o serviço de GPS. A função é chamado após a permissão do usuario para usar o GPS
     */
    private void startLocationService() {
        final Intent locationIntent = new Intent(this.getApplication(), LocationService.class);
        this.getApplication().startService(locationIntent);
        this.getApplication().bindService(locationIntent, serviceConnection, Context.BIND_AUTO_CREATE);
    }

    /**
     * Funcao para MQTT Service para atualizar o campo StatusText
     * @param message Mensagem a ser escrita no campo StatusTextText
     */
    public void updateStatusText(String message) {
        handler.post(() -> statusText.setText(message));
    }

    /**
     * Funcao para MQTT Service para atualizar o campo LastSent
     * @param message Mensagem a ser escrita no campo LastSentText
     */
    public void updateLastSentText(String message) {
        handler.post(() -> lastSentText.setText(message));
    }

    // =============================================================================================
    //  Funcoes para a inicializacao do Serviço GPS no background
    // =============================================================================================

    // Atributo privado que constroi a conexão com serviço GPS e atribui as funções para os eventos
    private ServiceConnection serviceConnection = new ServiceConnection() {
        /**
         *
         * @param className The concrete component name of the service that has
         * been connected.
         *
         * @param service The IBinder of the Service's communication channel,
         * which you can now make calls on.
         */
        public void onServiceConnected(ComponentName className, IBinder service) {
            String name = className.getClassName();
            if (name.endsWith("LocationService")) {
                gps = ((LocationService.LocationServiceBinder) service).getService();
                statusText.setText("conectando");
                gps.startTracking(
                        onibusText.getText().toString(),
                        rotaText.getText().toString(),
                        MainActivity.this);
                startButton.setEnabled(false);
                stopButton.setEnabled(true);
            }
        }

        /**
         * NUNCA é chamado, mas deveria quando o serviço fosse desconetado
         */
        public void onServiceDisconnected(ComponentName className) {
            if (className.getClassName().equals("LocationService")) {
                gps = null;
                statusText.setText("desconectado");
                startButton.setEnabled(false);
                stopButton.setEnabled(true);
            }
        }
    };
}