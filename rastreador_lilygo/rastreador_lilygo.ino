/**
 * Baseado sobre o exemplo de GPS
 * @file      GPS_BuiltIn.ino
 * @author    Lewis He (lewishe@outlook.com)
 * @license   MIT
 * @copyright Copyright (c) 2023  Shenzhen Xin Yuan Electronic Technology Co., Ltd
 * @date      2023-06-28
 * @note      GPS only supports A7670X/A7608X/SIM7000G/SIM7600 series (excluding A7670G and other versions that do not support positioning).
 */

// ============================================================================
//  Header
// ============================================================================

// install Arduino ESP32 by Espressif Systems 3.3.2
// install ArduinoHttpClient by Arduino 0.6.1


// Configura o TinyGSMClient,
#define TINY_GSM_MODEM_A7608           // A7608X is the same SIM7600
#include <TinyGsmClient.h>
#ifndef TINY_GSM_FORK_LIBRARY
#error "No correct definition detected, Please copy all the [lib directories](https://github.com/Xinyuan-LilyGO/LilyGO-T-A76XX/tree/main/lib) to the arduino libraries directory , See README"
#endif

#include <ArduinoHttpClient.h>         // install ArduinoHttpClient by Arduino 0.6.1

// Definições do LilyGO A7608X
#define MODEM_POWERON_PULSE_WIDTH_MS      (1000)
#define MODEM_POWEROFF_PULSE_WIDTH_MS     (3000)

#define MODEM_BAUDRATE                      (115200)
#define MODEM_DTR_PIN                       (25)
#define MODEM_TX_PIN                        (26)
#define MODEM_RX_PIN                        (27)
// The modem boot pin needs to follow the startup sequence.
#define BOARD_PWRKEY_PIN                    (4)
#define BOARD_BAT_ADC_PIN                   (35)
// The modem power switch must be set to HIGH for the modem to supply power.
#define BOARD_POWERON_PIN                   (12)
#define MODEM_RING_PIN                      (33)
#define MODEM_RESET_PIN                     (5)
#define BOARD_MISO_PIN                      (2)
#define BOARD_MOSI_PIN                      (15)
#define BOARD_SCK_PIN                       (14)
#define BOARD_SD_CS_PIN                     (13)

#define MODEM_RESET_LEVEL                   HIGH

// only version v1.1 or V2  has solar adc pin
#define BOARD_SOLAR_ADC_PIN                 (34)

// 127 is defined in GSM as the AUXVDD index
#define MODEM_GPS_ENABLE_GPIO               (127)
#define MODEM_GPS_ENABLE_LEVEL              (7)

#define OK       (0)


#define PRODUCT_MODEL_NAME                  "LilyGo-A7608X ESP32 Version"

#define TINY_GSM_RX_BUFFER 1024 // Set RX buffer to 1Kb

// Set serial for debug console (to the Serial Monitor, default speed 115200)
#define SerialMon          Serial     // UART para depuração
#define SerialAT           Serial1    // UART entre ESP32 e A7608SA

// Instance the GSM modem
TinyGsm  modem(SerialAT);

// Instance the HttpClient
const char server[]   = "200.17.212.40";
const char resource[] = "/api";
const int  port       = 1883;
TinyGsmClient gsm_client(modem);


// Your GPRS credentials, if any
const char apn[]      = "java.claro.com.br";
const char gprsUser[] = "Claro";
const char gprsPass[] = "Claro";

#define GSM_PIN ""

// ============================================================================
//  Setup
// ============================================================================

void setup_gsm_and_gnss() {
#ifdef BOARD_POWERON_PIN
    /* Set Power control pin output
    * * @note      Known issues, ESP32 (V1.2) version of T-A7670, T-A7608,
    *            when using battery power supply mode, BOARD_POWERON_PIN (IO12) must be set to high level after esp32 starts, otherwise a reset will occur.
    * */
    pinMode(BOARD_POWERON_PIN, OUTPUT);
    digitalWrite(BOARD_POWERON_PIN, HIGH);
#endif

    // Set modem reset pin ,reset modem
#ifdef MODEM_RESET_PIN
    pinMode(MODEM_RESET_PIN, OUTPUT);
    digitalWrite(MODEM_RESET_PIN, !MODEM_RESET_LEVEL); delay(100);
    digitalWrite(MODEM_RESET_PIN, MODEM_RESET_LEVEL); delay(2600);
    digitalWrite(MODEM_RESET_PIN, !MODEM_RESET_LEVEL);
#endif

    // Pull down DTR to ensure the modem is not in sleep state
    pinMode(MODEM_DTR_PIN, OUTPUT);
    digitalWrite(MODEM_DTR_PIN, LOW);

    // Turn on modem
    pinMode(BOARD_PWRKEY_PIN, OUTPUT);
    digitalWrite(BOARD_PWRKEY_PIN, LOW);
    delay(100);
    digitalWrite(BOARD_PWRKEY_PIN, HIGH);
    delay(MODEM_POWERON_PULSE_WIDTH_MS);
    digitalWrite(BOARD_PWRKEY_PIN, LOW);

    // Set modem baud 115200
    SerialAT.begin(115200, SERIAL_8N1, MODEM_RX_PIN, MODEM_TX_PIN);

    // Start modem
    Serial.println("Start modem...");
    delay(3000);

    // Test AT commands
    int retry = 0;
    while (!modem.testAT(1000)) {
        Serial.println(".");
        if (retry++ > 30) {
            digitalWrite(BOARD_PWRKEY_PIN, LOW);
            delay(100);
            digitalWrite(BOARD_PWRKEY_PIN, HIGH);
            delay(MODEM_POWERON_PULSE_WIDTH_MS);
            digitalWrite(BOARD_PWRKEY_PIN, LOW);
            retry = 0;
        }
    }
    Serial.println();
    delay(200);

    // Get Modem name
    String modemName = "UNKNOWN";
    while (1) {
        modemName = modem.getModemName();
        if (modemName == "UNKNOWN") {
            Serial.println("Unable to obtain module information normally, try again");
            delay(1000);
        } else if (modemName.startsWith("A7670E-FASE") || modemName.startsWith("A7670SA-FASE")) {
            Serial.println("Modem support built-in GPS function, keep running");
            break;
        } else if (modemName.startsWith("A7670E-LNXY-UBL")
                   || modemName.startsWith("A7670SA-LASE")
                   || modemName.startsWith("A7670SA-LASC")
                   ||  modemName.startsWith("A7670G-LLSE")
                   ||  modemName.startsWith("A7670G-LABE")
                   ||  modemName.startsWith("A7670E-LASE ")) {
            while (1) {
                Serial.println("The modem does not have built-in GPS function.");
                delay(1000);
            }
        } else {
            Serial.print("Model Name:");
            Serial.println(modemName);
            break;
        }
        delay(5000);
    }

    // Print modem software version
    String res;
    modem.sendAT("+SIMCOMATI");
    modem.waitResponse(10000UL, res);
    Serial.println(res);

    // Unlock your SIM card with a PIN if needed
    /*if (GSM_PIN && modem.getSimStatus() != 3) {
        modem.simUnlock(GSM_PIN);
    }*/

    // Conecta na rede 4G
    modem.gprsConnect(apn, gprsUser, gprsPass);
    SerialMon.println("Waiting for network...");
    if (!modem.waitForNetwork()) {
        SerialMon.println(" fail");
        return ;
    }

    if (modem.isNetworkConnected()) {
        SerialMon.println("Network connected");
    }

    // GPRS connection parameters are usually set after network registration
    SerialMon.print(F("Connecting to "));
    SerialMon.print(apn);
    if (!modem.gprsConnect(apn, gprsUser, gprsPass)) {
        SerialMon.println(" fail");
        return;
    }
    SerialMon.println(" success");

    // Verifica se tem internet
    while (!modem.isGprsConnected()) {
        // SerialMon.println("GPRS connected");
        SerialMon.print(".");
        delay(1000);
    }
    SerialMon.println("GPRS connected");

    // Habilita o GNSS
    Serial.println("Enabling GPS/GNSS/GLONASS");
    while (!modem.enableGPS(MODEM_GPS_ENABLE_GPIO, MODEM_GPS_ENABLE_LEVEL)) {
        Serial.print(".");
    }
    Serial.println();
    Serial.println("GPS Enabled");

    // Set GPS Baud to 115200
    modem.setGPSBaud(115200);
}

void setup() {
    Serial.begin(115200);
    setup_gsm_and_gnss();
}

// ============================================================================
//  Loop
// ============================================================================

int loop_get_gps(float& lat2, float& lon2) {
    float speed2    = 0;
    float alt2      = 0;
    int   vsat2     = 0;
    int   usat2     = 0;
    float accuracy2 = 0;
    int   year2     = 0;
    int   month2    = 0;
    int   day2      = 0;
    int   hour2     = 0;
    int   min2      = 0;
    int   sec2      = 0;
    uint8_t    fixMode   = 0;

    int i=0;
    for (; i<5; i++) {
        Serial.println("Requesting current GPS/GNSS/GLONASS location");
        if (modem.getGPS(&fixMode, &lat2, &lon2, &speed2, &alt2, &vsat2, &usat2, &accuracy2,
                         &year2, &month2, &day2, &hour2, &min2, &sec2)) {

            Serial.print("FixMode:"); Serial.println(fixMode);
            Serial.print("Latitude:"); Serial.print(lat2, 6); Serial.print("\tLongitude:"); Serial.println(lon2, 6);
            Serial.print("Speed:"); Serial.print(speed2); Serial.print("\tAltitude:"); Serial.println(alt2);
            Serial.print("Visible Satellites:"); Serial.print(vsat2);

            // GPS_BuiltIn cannot get the number of satellites in use, so it always returns 0
            Serial.print("\tUsed Satellites:"); Serial.println(usat2);
            Serial.print("Accuracy:"); Serial.println(accuracy2);

            Serial.print("Year:"); Serial.print(year2);
            Serial.print("\tMonth:"); Serial.print(month2);
            Serial.print("\tDay:"); Serial.println(day2);

            Serial.print("Hour:"); Serial.print(hour2);
            Serial.print("\tMinute:"); Serial.print(min2);
            Serial.print("\tSecond:"); Serial.println(sec2);
            break;
        } else {
            Serial.println("Couldn't get GPS/GNSS/GLONASS location, retrying in 15s.");
            delay(15000);
        }
    }
    if ( i >= 5 ) {
        return 1;
    }

    Serial.println("Retrieving GPS/GNSS/GLONASS location again as a string");
    String gps_raw = modem.getGPSraw();
    Serial.print("GPS/GNSS Based Location String:");
    Serial.println(gps_raw);
    return OK;
}


/**
@brief envia uma requisicao POST para o Servidor HTTP do Intercampi

*/
int loop_send_post(float lat, float lon) {
    if (!modem.isNetworkConnected()) {
        SerialMon.println("Network disconnected");
        return 1;
    }

    // Prepara a mensagem JSON
    char json_data[1024];
    snprintf(json_data, sizeof(json_data)-1, 
        "{\"rota\": \"teste1\", \"veiculo\": \"teste11\", \"lat\": %f, \"log\": %f}", lat, lon);

    // Inicializa a requisicao POST
    SerialMon.println(F("Performing HTTP POST request... "));
    SerialMon.println(json_data);
    HttpClient http(gsm_client, server, port);
    const char content_type[] = "application/json";
    int err = http.post(resource, content_type, json_data);
    if (err != 0) {
        SerialMon.println(F("failed to connect"));
        return 1;
    }

    // Espera receber a resposta do Servidor
    int status = http.responseStatusCode();
    SerialMon.print(F("Response status code: "));
    SerialMon.println(status);
    if (!status) {
        delay(10000);
        return 1;
    }

    // Mostra a resposta do Servidor
    SerialMon.println(F("Response Headers:"));
    while (http.headerAvailable()) {
        String headerName  = http.readHeaderName();
        String headerValue = http.readHeaderValue();
        SerialMon.println("    " + headerName + " : " + headerValue);
    }

    // 
    int length = http.contentLength();
    if (length >= 0) {
        SerialMon.print(F("Content length is: "));
        SerialMon.println(length);
    }
    if (http.isResponseChunked()) {
        SerialMon.println(F("The response is chunked"));
    }

    String body = http.responseBody();
    SerialMon.println(F("Response:"));
    SerialMon.println(body);

    SerialMon.print(F("Body length is: "));
    SerialMon.println(body.length());

    // Shutdown
    http.stop();
    return OK;
}


void loop() {
    float lat = 0.0;
    float lon = 0.0;
    if ( loop_get_gps(lat, lon) == OK ) {
        loop_send_post(lat, lon);
    }

    // Serial.println("Disabling GPS");
    // modem.disableGPS(MODEM_GPS_ENABLE_GPIO, !MODEM_GPS_ENABLE_LEVEL);

    // espera 30 segundos
    delay(30000);    
}