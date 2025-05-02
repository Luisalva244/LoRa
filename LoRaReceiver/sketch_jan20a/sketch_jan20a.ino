#include "LoRaWan_APP.h"
#include "Arduino.h"
#include "../../LoRaSender/LoRaSender.h"
#include "MAC.h"
#include <WiFi.h>
#include <driver/rtc_io.h>
#include "esp_wifi.h"
#include "../../LoRaSender/MessageSender.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"

#define RF_FREQUENCY                                869250000 // Hz
#define TX_OUTPUT_POWER                             22        // dBm
#define LORA_BANDWIDTH                              0         // [0: 125 kHz, 1: 250 kHz, 2: 500 kHz, 3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         
#define LORA_SYMBOL_TIMEOUT                         0        
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false
#define SOIL_HUMIDITY                               20


uint8_t macAddr[6]; // Array to store the MAC address
char macAddress[18]; 

MessageSender msgSender;
QueueHandle_t cropDataQueue;
static RadioEvents_t RadioEvents;


void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr);
void OnTxDone(void);

void setup() {
  Serial.begin(115200);
  Mcu.begin(HELTEC_BOARD, SLOW_CLK_TPYE);

  RadioEvents.RxDone = OnRxDone;
  RadioEvents.TxDone = OnTxDone;

  WiFi.mode(WIFI_STA);
  esp_wifi_get_mac(WIFI_IF_STA, macAddr);
  sprintf(macAddress, "%02X:%02X:%02X:%02X:%02X:%02X",
    macAddr[0], macAddr[1], macAddr[2],
    macAddr[3], macAddr[4], macAddr[5]);

  Serial.printf("MAC Address: %s", macAddress);   

  Radio.Init(&RadioEvents);
  Radio.SetChannel(RF_FREQUENCY);

  // Configure TX
  Radio.SetTxConfig(MODEM_LORA, TX_OUTPUT_POWER, 0, LORA_BANDWIDTH,
                      LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      LORA_PREAMBLE_LENGTH, LORA_FIX_LENGTH_PAYLOAD_ON,
                      true, 0, 0, LORA_IQ_INVERSION_ON, 3000);

  // Configure RX
  Radio.SetRxConfig(MODEM_LORA, LORA_BANDWIDTH, LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      0, LORA_PREAMBLE_LENGTH, LORA_SYMBOL_TIMEOUT,
                      LORA_FIX_LENGTH_PAYLOAD_ON, 0, true, 0, 0,
                      LORA_IQ_INVERSION_ON, true);

  cropDataQueue = xQueueCreate(10, sizeof(cropData)); 
  
  if (cropDataQueue == NULL) 
  {
   Serial.println("Error: No se pudo crear la cola");
  }

  Serial.println("Starting receiver...");
  Radio.Rx(0); 
}

void loop() 
{
  Radio.IrqProcess();

  cropData receivedMsg;
  if (xQueueReceive(cropDataQueue, &receivedMsg, 0) == pdTRUE) {
    // Procesar mensaje
    uint8_t foundNode = 0;
    for (int i = 0; i < NUM_NODES; i++) 
    {
      if (strcmp(receivedMsg.senderAddress, nodeDefs[i].mac) == 0) 
      {
        foundNode = nodeDefs[i].nodeId;
        break;
      }
    }

    if (foundNode != 0) {
      Serial.print(" Node: ");
      Serial.println(foundNode);
      Serial.print(" soilHumidity: ");
      Serial.println(receivedMsg.soilHumidity);
      Serial.print(" Humidity: ");
      Serial.println(receivedMsg.Humidity);
      Serial.print(" Temperature: ");
      Serial.println(receivedMsg.Temperature);
    }
  }
}

void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) 
{

  if (size == sizeof(cropData)) 
  {
    cropData rxData;
    memcpy(&rxData, payload, sizeof(cropData));
      
    if (strcmp(rxData.receiverAddress,  macAddress) == 0) 
    {
      // Enviar el mensaje a la queue
      if (xQueueSend(cropDataQueue, &rxData, portMAX_DELAY) != pdPASS) 
      {
        Serial.println("Error: no se pudo poner el mensaje en la cola");
      }

    }
  }
  
    // Continue receiving
    Radio.Rx(0); 
}

void OnTxDone(void) 
{
  Serial.println("TX done.");
  Radio.Rx(0);  // Continue receiving after transmission
}
