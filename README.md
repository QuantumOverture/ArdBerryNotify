Web App:

* Main Index Page that describes the purpose of this app.

* Account Page to setup account and get APIKey
    * Need special password from me to get an account.
    * Account Page Also allows you to add API keys(and other required info) for the supported APIs.
    * Delete account,reset password options as well.

* User homepage -> hub website with all the API data displayed and request log.
    * Display API key here

* Requests are outputted in an Arduino friendly manner.
    * NLP in background + filtering => ML -> part of classifier of importance of important emails (if possible + messages)
    * Get weather data as well.
    * If missing an API key for a specific service -> transmit part of request

Raspberry PI:

* Python Script that runs on startup and stops with button press(not connected to ardiuno, done by Ras PI switch
   -> Raspberry PI also turns off/shutdown) => turn off completely by finally switching power switch.
* Python Script sets up serial connection between Arduino and feeds data into it.

Arduino:

* Turns on lights:
    * RBG for messages.
    * RGB for environment status.
        * LCD for more info.
            * Tells you what is wrong in banner style(NYSE style).
    * Red light for classes.

(IF TIME):

* Android APP that also request data and outputs results
