#ifndef LORA_SENDER_H
#define LORA_SENDER_H

#include "LoRaWan_APP.h"
#include "Arduino.h"
#include "driver/rtc_io.h"
#include <driver/gpio.h>
#include <stdint.h>


// Definiciones del modulo LoRA
#define RF_FREQUENCY                                869250000 // Hz
#define TX_OUTPUT_POWER                             22        // dBm
#define LORA_BANDWIDTH                              0         // [0: 125 kHz, 1: 250 kHz, 2: 500 kHz, 3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         
#define LORA_SYMBOL_TIMEOUT                         0        
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false

// Definiciones de pines utilizados en el ESP32 para los sensores 
#define SOIL_HUMIDITY                               20
#define DHTPIN                                      5
#define DHTTYPE                                     DHT22

// Variables globales
RTC_DATA_ATTR extern uint64_t wakeupTime;  



// Estructura para la informacion del cultivo
#pragma pack(push, 1)
struct cropData
{
  char  receiverAddress[18];
  char  senderAddress[18];       
  float soilHumidity;  
  float Humidity;  
  float Temperature; 
} __attribute__((packed));
#pragma pack(pop)


#pragma pack(push, 1)
struct nodehourData
{
  char  node[18];       
  uint8_t hour;  
} __attribute__((packed));
#pragma pack(pop)

#pragma pack(push, 1)
struct requestHour
{
  char  node[18];       
  char  command[8];  
} __attribute__((packed));
#pragma pack(pop)

#pragma pack(push, 1)
struct HandshakeRequest {
    char node[18];  // MAC address or identifier (e.g., "01:23:45:67:89:AB")
    char command[14];  // Command type (e.g., "HANDSHAKE_REQ")
};
#pragma pack(pop)

#pragma pack(push, 1)
struct HandshakeAck {
    char node[18];  // MAC address or identifier (same as sender's MAC)
    char command[12];  // Command type (e.g., "HANDSHAKE_ACK")
};
#pragma pack(pop)


// Funciones
void setupLoRaSender();
void loopLoRaSender();
void OnTxDone(void);
void OnTxTimeout(void);
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr);
void SendMessage();
void SoilHumidity(int pin, struct cropData *data);
void DhtValues(struct cropData *data);  


#endif 