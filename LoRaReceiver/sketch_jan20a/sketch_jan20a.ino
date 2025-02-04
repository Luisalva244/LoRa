/* Heltec Automation LoRa Receiver: Decodifica la estructura payLoad en crudo */

#include "LoRaWan_APP.h"
#include "Arduino.h"

#define RF_FREQUENCY        920000000
#define LORA_BANDWIDTH      0
#define LORA_SPREADING_FACTOR 7
#define LORA_CODINGRATE     1
#define LORA_PREAMBLE_LENGTH 8
#define LORA_SYMBOL_TIMEOUT  0
#define LORA_FIX_LENGTH_PAYLOAD_ON false
#define LORA_IQ_INVERSION_ON false
#define BUFFER_SIZE         64

#pragma pack(push, 1)
struct payLoad {
  char  node;
  float humidity;
  float latituded;
  float longituded;
  float altitude;
} __attribute__((packed));
#pragma pack(pop)

char rxpacket[BUFFER_SIZE];
static RadioEvents_t RadioEvents;
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr);
void OnTxDone(void);

void setup() {
  Serial.begin(115200);
  Mcu.begin(HELTEC_BOARD, SLOW_CLK_TPYE);

  RadioEvents.RxDone = OnRxDone;
  RadioEvents.TxDone = OnTxDone;

  Radio.Init(&RadioEvents);
  Radio.SetChannel(RF_FREQUENCY);

  // Rx config
  Radio.SetRxConfig(MODEM_LORA,
                    LORA_BANDWIDTH,
                    LORA_SPREADING_FACTOR,
                    LORA_CODINGRATE,
                    0,
                    LORA_PREAMBLE_LENGTH,
                    LORA_SYMBOL_TIMEOUT,
                    LORA_FIX_LENGTH_PAYLOAD_ON,
                    0,
                    true,
                    0,
                    0,
                    LORA_IQ_INVERSION_ON,
                    true);

  // Tx config (para enviar ACK o algo si quieres)
  Radio.SetTxConfig(MODEM_LORA,
                    20, // dBm
                    0,
                    LORA_BANDWIDTH,
                    LORA_SPREADING_FACTOR,
                    LORA_CODINGRATE,
                    LORA_PREAMBLE_LENGTH,
                    LORA_FIX_LENGTH_PAYLOAD_ON,
                    true,
                    0,
                    0,
                    LORA_IQ_INVERSION_ON,
                    3000);

  Serial.println("Starting receiver...");
  Radio.Rx(0); // modo recepción continuo
}

void loop() {
  Radio.IrqProcess(); 
}

// Callback al recibir un mensaje
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) {
  // Ver si el tamaño coincide con la estructura
  if (size == sizeof(payLoad)) {
    // Copiamos el payload a una instancia local de la estructura
    payLoad rxData;
    memcpy(&rxData, payload, sizeof(payLoad));

    // Mostrar cada campo
    Serial.println("Recibido estructura payLoad:");
    Serial.print(" Node: ");
    Serial.println(rxData.node);
    Serial.print(" Humidity: ");
    Serial.println(rxData.humidity);
    Serial.print(" Lat: ");
    Serial.println(rxData.latituded, 6);
    Serial.print(" Lon: ");
    Serial.println(rxData.longituded, 6);
    Serial.print(" Alt: ");
    Serial.println(rxData.altitude, 2);

    const char ack[] = "ACK";
    Serial.println("Sending ACK...");
    Radio.Send((uint8_t*)ack, strlen(ack));

  } 
  else {
    // En caso de que sea un mensaje ASCII (por ejemplo "Hello"), o no coincida
    payload[size] = '\0'; 
    Serial.printf("Received (ASCII?): %s | size=%d | RSSI=%d SNR=%d\n", 
                  (char*)payload, size, rssi, snr);
  }
}

void OnTxDone(void) {
  Serial.println("TX done.");
  Radio.Rx(0);
}