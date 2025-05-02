#include <WiFi.h>
#include "LoRaSender.h"
#include "MessageSender.h"
#include "esp_wifi.h"
#include "driver/rtc_io.h"
#include "DHT.h"

#define DHTPIN 5
#define DHTTYPE DHT22

// Inicialización de variables globales
RTC_DATA_ATTR int readsPerHour = 119;
RTC_DATA_ATTR uint64_t wakeupTime = 3600000000ULL / readsPerHour;
RTC_DATA_ATTR int messagesCounter = 0; 
RTC_DATA_ATTR uint8_t hour = 5;
RTC_DATA_ATTR bool lightSleep = false;
RTC_DATA_ATTR long tiempoUltimaLectura=0;

bool lora_idle = true;
bool messageReceived = false;

MessageSender msgSender;
requestHour requestHourPayLoad;
RadioEvents_t RadioEvents;
DHT dht(DHTPIN, DHTTYPE);

uint8_t macAddr[6];
char senderMAC[18];
char receiverMAC[] = "48:CA:43:B6:A8:0C";

void setupLoRaSender() 
{
    Serial.begin(115200);
    dht.begin();
    delay(1000);

    Mcu.begin(HELTEC_BOARD, SLOW_CLK_TPYE);
    delay(1000);

     
    WiFi.mode(WIFI_STA);
    esp_wifi_get_mac(WIFI_IF_STA, macAddr);
    sprintf(senderMAC, "%02X:%02X:%02X:%02X:%02X:%02X",
            macAddr[0], macAddr[1], macAddr[2],
            macAddr[3], macAddr[4], macAddr[5]);

    // Inicializa eventos de radio
    RadioEvents.TxDone = OnTxDone;
    RadioEvents.TxTimeout = OnTxTimeout;
    RadioEvents.RxDone = OnRxDone;

    Radio.Init(&RadioEvents);
    Radio.SetChannel(RF_FREQUENCY);

    // Configuración de transmisión
    Radio.SetTxConfig(MODEM_LORA, TX_OUTPUT_POWER, 0, LORA_BANDWIDTH,
                      LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      LORA_PREAMBLE_LENGTH, LORA_FIX_LENGTH_PAYLOAD_ON,
                      true, 0, 0, LORA_IQ_INVERSION_ON, 3000);

    // Configuración de recepción
    Radio.SetRxConfig(MODEM_LORA, LORA_BANDWIDTH, LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      0, LORA_PREAMBLE_LENGTH, LORA_SYMBOL_TIMEOUT,
                      LORA_FIX_LENGTH_PAYLOAD_ON, 0, true, 0, 0,
                      LORA_IQ_INVERSION_ON, true);

    pinMode(SOIL_HUMIDITY, INPUT);

    Radio.Rx(0);
}

void loopLoRaSender() 
{

    if (lora_idle) 
    {
        cropData cropPayLoad;
        strncpy(cropPayLoad.receiverAddress,receiverMAC, sizeof(cropPayLoad.receiverAddress));
        strncpy(cropPayLoad.senderAddress, senderMAC, sizeof(cropPayLoad.senderAddress));

        SoilHumidity(SOIL_HUMIDITY, &cropPayLoad);  
        DhtValues(&cropPayLoad);  

        messagesCounter++;

        msgSender.sendDataMessage(cropPayLoad); 

        esp_sleep_enable_timer_wakeup(wakeupTime);
        esp_deep_sleep_start();         
    }

    Radio.IrqProcess();  // Handle interrupts

}

void OnTxDone(void) {
    Serial.println("TX done...");
    lora_idle = true;
}

void OnTxTimeout(void)
{
    Serial.println("TX timeout...");
    lora_idle = true;
}


void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) 
{

}


void SoilHumidity(int pin, struct cropData *data) 
{
    int sensor_analog = analogRead(pin);
    float moisture_percentage = 100.0 - ((sensor_analog / 1023.0) * 100.0);
    data->soilHumidity = moisture_percentage;
}

void DhtValues(struct cropData *data)
{
      delay(500);
      float h = dht.readHumidity(); 
      float t = dht.readTemperature(); 

      data->Humidity = h;
      data->Temperature = t;
}


