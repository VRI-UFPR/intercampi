package com.ufpr.tracker_android

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import java.util.concurrent.TimeUnit
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import android.content.Context
import androidx.activity.viewModels
import androidx.lifecycle.Observer
import android.widget.TextView

class MessageViewModel : ViewModel() {
    private val _messageCount = MutableLiveData<Int>()
    val messageCount: LiveData<Int> get() = _messageCount

    fun loadMessageCount(context: Context) {
        val sharedPreferences = context.getSharedPreferences("MyAppPrefs", Context.MODE_PRIVATE)
        _messageCount.value = sharedPreferences.getInt("messageCount", 0)
    }
}


class MainActivity : AppCompatActivity() {
    private val viewModel: MessageViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val tvCounter = findViewById<TextView>(R.id.tvCounter)
        tvCounter.text = "Mensagens enviadas: 0"

        // Carregar o contador salvo
        viewModel.loadMessageCount(this)

        // Observar mudanças no contador e atualizar a UI
        viewModel.messageCount.observe(this, Observer { count ->
            tvCounter.text = "Mensagens enviadas aaa: $count"
        })

        val locationWorkRequest = PeriodicWorkRequestBuilder<LocationWorker>(
            1, TimeUnit.SECONDS
        ).build()

        WorkManager.getInstance(this).enqueueUniquePeriodicWork(
            "LocationWork",
            ExistingPeriodicWorkPolicy.UPDATE,
            locationWorkRequest
        )


    }
}