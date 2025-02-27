//Heltec Automation LoRa Sender with ACK Handling */

#include "LoRaWan_APP.h"
#include "Arduino.h"
#include "driver/rtc_io.h"
#include <driver/gpio.h>
 
#define RF_FREQUENCY                                869250000 // Hz
#define TX_OUTPUT_POWER                             22        // dBm
#define LORA_BANDWIDTH                              0         // [0: 125 kHz, 1: 250 kHz, 2: 500 kHz, 3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false
#define RX_TIMEOUT_VALUE                            1000
#define SOIL_HUMIDITY                               20

RTC_DATA_ATTR int wakeupTime = 10 * 1000000;  

char nodeNumber = '1';

/*Flags*/
bool lora_idle = true;      // Radio lista


#pragma pack(push, 1)
struct payLoad 
{
  char  node;       
  float soilHumidity;  
  float Humidity;  
  float Temperature; 
} __attribute__((packed));
#pragma pack(pop)

payLoad LoRaPayLoad;

/* In case esp32 gets flash
uint32_t licenseKey[4] = 
{
  0x7C6D0ECA,
  0x16AE1A3E,
  0xFD0B71B6,
  0x7E0868FA
};
*/

// LoRa radio event callbacks
static RadioEvents_t RadioEvents;
void OnTxDone(void);
void OnTxTimeout(void);
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr);
void SendMessage();


void setup() {
    Serial.begin(115200);
    //Mcu.setlicense(licenseKey,HELTEC_BOARD);
    Mcu.begin(HELTEC_BOARD, SLOW_CLK_TPYE);

    // Initialize radio events
    RadioEvents.TxDone = OnTxDone;
    RadioEvents.TxTimeout = OnTxTimeout;
    RadioEvents.RxDone = OnRxDone;

    Radio.Init(&RadioEvents);
    Radio.SetChannel(RF_FREQUENCY);

    // Set transmission configuration
    Radio.SetTxConfig(MODEM_LORA, TX_OUTPUT_POWER, 0, LORA_BANDWIDTH,
                      LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      LORA_PREAMBLE_LENGTH, LORA_FIX_LENGTH_PAYLOAD_ON,
                      true, 0, 0, LORA_IQ_INVERSION_ON, 3000);

    // Set reception configuration
    Radio.SetRxConfig(MODEM_LORA, LORA_BANDWIDTH, LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      0, LORA_PREAMBLE_LENGTH, LORA_SYMBOL_TIMEOUT,
                      LORA_FIX_LENGTH_PAYLOAD_ON, 0, true, 0, 0,
                      LORA_IQ_INVERSION_ON, true);
    
    pinMode(SOIL_HUMIDITY, INPUT); 

}

void loop() 
{

  if (lora_idle) 
  {
    SendMessage();
    delay(500);
    esp_sleep_enable_timer_wakeup(wakeupTime);
    esp_deep_sleep_start(); 
  }

}
// Callback when transmission is done
void OnTxDone(void) {
    Serial.println("TX done...");
    lora_idle = true;
}

// Callback when transmission times out
void OnTxTimeout(void) {
    Serial.println("TX timeout...");
    lora_idle = true;
}

void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) 
{
  payload[size] = '\0';
  Serial.printf("Received: %s | RSSI: %d | SNR: %d\n", (char *)payload, rssi, snr);
}


void SendMessage()
{
  LoRaPayLoad.node = nodeNumber;

  LoRaPayLoad.soilHumidity = SoilHumidity(SOIL_HUMIDITY);  
  LoRaPayLoad.Humidity  = 0;
  LoRaPayLoad.Temperature = 0;

  Radio.Send((uint8_t*)&LoRaPayLoad, sizeof(LoRaPayLoad));
  lora_idle = false;
  Serial.printf("Sending struct [node=%c soilHum=%.2f Hum=%.2f Temp=%.2f]\n",
                LoRaPayLoad.node,
                LoRaPayLoad.soilHumidity,
                LoRaPayLoad.Humidity,
                LoRaPayLoad.Temperature);
}


float SoilHumidity(int pin)
{
  int sensor_analog = analogRead(pin);
  float moisture_percentage = ( 100 - ( (sensor_analog/1023.00) * 100 ) );
  Serial.print("Moisture Percentage = ");
  Serial.print(moisture_percentage);
  Serial.print("%\n\n");
  
  return moisture_percentage;
}

