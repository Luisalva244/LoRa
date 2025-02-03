/* Heltec Automation LoRa Receiver with ACK Response */

#include "LoRaWan_APP.h"
#include "Arduino.h"

#define RF_FREQUENCY                                920000000 // Hz
#define LORA_BANDWIDTH                              0         // [0: 125 kHz, 1: 250 kHz, 2: 500 kHz, 3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false
#define BUFFER_SIZE                                 64 // Define the payload size

char rxpacket[BUFFER_SIZE];

// LoRa radio event callbacks
static RadioEvents_t RadioEvents;
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr);
void OnTxDone(void);

void setup() 
{
  Serial.begin(115200);
  Mcu.begin(HELTEC_BOARD, SLOW_CLK_TPYE);

  // Initialize radio events
  RadioEvents.RxDone = OnRxDone;
  RadioEvents.TxDone = OnTxDone;

  Radio.Init(&RadioEvents);
  Radio.SetChannel(RF_FREQUENCY);

  // Set reception configuration
  Radio.SetRxConfig(MODEM_LORA, LORA_BANDWIDTH, LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      0, LORA_PREAMBLE_LENGTH, LORA_SYMBOL_TIMEOUT,
                      LORA_FIX_LENGTH_PAYLOAD_ON, 0, true, 0, 0,
                      LORA_IQ_INVERSION_ON, true);

  // Set transmission configuration
  Radio.SetTxConfig(MODEM_LORA, 14, 0, LORA_BANDWIDTH,
                      LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                      LORA_PREAMBLE_LENGTH, LORA_FIX_LENGTH_PAYLOAD_ON,
                      true, 0, 0, LORA_IQ_INVERSION_ON, 3000);

  Serial.println("Starting receiver...");
  Radio.Rx(0); // Start continuous RX
}

void loop() 
{
  Radio.IrqProcess(); // Handle LoRa interrupts
}

// Callback when a message is received
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) 
{
  payload[size] = '\0'; // Null-terminate the received message
  Serial.printf("Received message: %s | RSSI: %d | SNR: %d\n", (char *)payload, rssi, snr);
}

// Callback when transmission is done
void OnTxDone(void) 
{
  Serial.println("ACK sent successfully.");
  Radio.Rx(0); // Switch back to RX mode
}
