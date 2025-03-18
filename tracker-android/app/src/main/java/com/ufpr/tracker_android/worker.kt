package com.ufpr.tracker_android

import android.content.Context
import android.util.Log
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import kotlinx.coroutines.tasks.await
import org.eclipse.paho.client.mqttv3.MqttClient
import org.eclipse.paho.client.mqttv3.MqttConnectOptions
import org.eclipse.paho.client.mqttv3.MqttMessage


class LocationWorker(appContext: Context, workerParams: WorkerParameters) :
    CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        Log.e("Worker", "Inicio da execucao do Servico (15m)")

        val fusedLocationClient = LocationServices.getFusedLocationProviderClient(applicationContext)

        val sharedPreferences = applicationContext.getSharedPreferences("MyAppPrefs", Context.MODE_PRIVATE)
        val currentCount = sharedPreferences.getInt("messageCount", 0)
        sharedPreferences.edit().putInt("messageCount", currentCount+1).apply()

        val latitude = 24.123
        val longitude = 45.123
        val mqttMessage = "{Lat:$latitude,Lon:$longitude}"
        sendMqttMessage(mqttMessage)

        try {
            val location = fusedLocationClient.getCurrentLocation(
                Priority.PRIORITY_HIGH_ACCURACY,
                null
            ).await()

            /*if (location != null) {
                val latitude = location.latitude
                val longitude = location.longitude
                val mqttMessage = "Lat: $latitude, Lon: $longitude"
                sendMqttMessage(mqttMessage)
            }*/
        } catch (e: Exception) {
            return Result.retry()
        }

        return Result.success()
    }

    private fun sendMqttMessage(message: String) {
        val clientId = MqttClient.generateClientId()

        // no momento, mantenha persistence = NULL, caso contrario dara erro
        val client = MqttClient("tcp://185.159.82.136:1883", clientId, null)
        val options = MqttConnectOptions().apply {
            isCleanSession = true
        }

        client.connect(options)
        client.publish("location", MqttMessage(message.toByteArray()))
        client.disconnect()
    }
}