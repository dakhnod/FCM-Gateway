# FCM-Gateway

## Introduction

![FCM Gateway flow](https://github.com/dakhnod/FCM-Gateway-Android-client/assets/26143255/9410dbdd-c136-4bf3-9a8f-a72fc212b3eb)

Ever wanted to 
- send an intent
- open an activity
to/of an app on your phone (like tasker, or your own app) while it's closed / in the background?

This project reduces that project to two steps:
1. Install the [FCM Gateway app](https://github.com/dakhnod/FCM-Gateway-Android-client/releases/latest) on your phone and copy the Token
2. Send a request to the FCM Gateway server

This application is part of the FCM Gateway infrastructure.
It allows you to receive FCM messages through the Gateway and forward them to other apps
as broadcastet intents.

To get this app up and running, you'll need to copy your own google-service.json into /app.
To acquire that one, just follow [this tutorial](https://firebase.google.com/docs/android/setup?hl=de#console).

## Usage
Once this app is running, whether it is through the Play store or from [here](https://github.com/dakhnod/FCM-Gateway-Android-client/releases/latest), you'll need
the app to generate a registration token. For that just open the app, the prompt should tell you how to 
obtain the token.
With that token, you can start sending messages to the API.

The app should work when closed or in background.

### Forwarding intents

The data received by this application through the gateway can contain the following fields

```
{
    "to": "The key you copied from the FCM Gateway on your phone",
    "type": "(optional) 'intent' for sending a broadcast, 'activity' for starting an activity.",
    "application": "(optional) the target package name to send the intent to. Broadcastet to all apps if left out",
    "action": "(optional) the action set for the intent",
    "class": "(optional) only relevant when type=="activity"; this class can specify what activity class to start; if omitted, the default launch activity will be started",
    "extras": {
        "EXTRA_KEY_1": "(optional) a first extra entry. Can contain ints, floats, booleans or strnings",
        "EXTRA_KEY_2": "(optional) a second extra entry. Can contain ints, floats, booleans or strnings",
        "EXTRA_KEY_3": "(optional) the whole 'extras' entry is optional",
    }
}
```

Just send the JSON to `https://fcm.nullco.de/api/fcm/send`. Don't forget to include the key from the Android APP in the "to" field.
