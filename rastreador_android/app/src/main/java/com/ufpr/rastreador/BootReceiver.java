package com.ufpr.rastreador;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

// =================================================================================================
//  BootReceiver
// =================================================================================================

public class BootReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) {
            // Start your desired activity or service here
            Intent launchIntent = new Intent(context, MainActivity.class);
            // Required for starting an activity from a non-activity context
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(launchIntent);
        }
    }
}