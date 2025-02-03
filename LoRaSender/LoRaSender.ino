//Heltec Automation LoRa Sender with ACK Handling */

#include <Wire.h>               
#include "HT_SSD1306Wire.h"
#include "LoRaWan_APP.h"
#include "Arduino.h"
#include <HardwareSerial.h>
#include <HT_TinyGPS++.h>
 
#define RF_FREQUENCY                                915000000 // Hz
#define TX_OUTPUT_POWER                             14        // dBm
#define LORA_BANDWIDTH                              0         // [0: 125 kHz, 1: 250 kHz, 2: 500 kHz, 3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false
#define RX_TIMEOUT_VALUE                            1000
#define BUFFER_SIZE                                 64 // Define the payload size
#define MAX_RETRIES 3

static SSD1306Wire  display(0x3c, 500000, SDA_OLED, SCL_OLED, GEOMETRY_128_64, RST_OLED); // addr , freq , i2c group , resolution , rst
HardwareSerial SerialGPS(2);
TinyGPSPlus gps;

static const int RXPin = 21;
static const int TXPin = 26;
static const uint32_t GPSBaud = 9600;

char txpacket[BUFFER_SIZE];
bool lora_idle = true;
bool ackReceived = false;
int retries = 0;
double txNumber = 0;
int intentos = 0;
float coordinates[3] = {};

/*uint32_t licenseKey[4] = {
  0x7C6D0ECA,
  0x16AE1A3E,
  0xFD0B71B6,
  0x7E0868FA
};*/
bool gpsUpdate = false;
// LoRa radio event callbacks
static RadioEvents_t RadioEvents;
void OnTxDone(void);
void OnTxTimeout(void);
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr);

void setup() {
    Serial.begin(115200);
    VextON();
    //Mcu.setlicense(licenseKey,HELTEC_BOARD);
    Mcu.begin(HELTEC_BOARD, SLOW_CLK_TPYE);
    display.init();
    display.setFont(ArialMT_Plain_10);
    SerialGPS.begin(GPSBaud, SERIAL_8N1, RXPin, TXPin);

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
}

void loop() {
      
    while(SerialGPS.available()>0)
    {
     gps.encode(SerialGPS.read());
    
     
     if (gps.location.isUpdated())
     {
      Serial.print("Latitud: ");
      Serial.println(gps.location.lat(), 6);
      coordinates[0] = gps.location.lat();
      Serial.print("Longitud: ");
      Serial.println(gps.location.lng(), 6);
      coordinates[1] = gps.location.lng();     
      Serial.print("Sats: ");
      Serial.println(gps.satellites.value());
      Serial.print("Alt (m): ");
      Serial.println(gps.altitude.meters());
      coordinates[2] = gps.altitude.meters();
      gpsUpdate = true;
      Serial.println();
     }
    }

    if (lora_idle) {
        ackReceived = false; // Reset ACK flag
        retries = 0;         // Reset retries counter

        while (retries < MAX_RETRIES && !ackReceived) {
            
            if(gpsUpdate == false)
            {
              sprintf(txpacket, "Hello world number %.2f" , txNumber);
              Serial.printf("\r\nSending packet: \"%s\", length %d\r\n", txpacket, strlen(txpacket));
              drawTextFlowDemo();
              // Send the message
              Radio.Send((uint8_t *)txpacket, strlen(txpacket));
              lora_idle = false;
            } else 
            {
              sprintf(txpacket, "Lat=%.6f,Lon=%.6f,Alt=%.2f", coordinates[0], coordinates[1], coordinates[2]);
              drawTextFlowDemo();
              // Send the message
              Radio.Send((uint8_t *)txpacket, strlen(txpacket));
              lora_idle = false;
              gpsUpdate = false;
            }
            // Wait for ACK or timeout
            unsigned long start = millis();
            while (millis() - start < 1000) { // Wait up to 1 second for ACK
                Radio.IrqProcess(); // Handle LoRa interrupts
                if (ackReceived) {
                    intentos ++;
                    drawTextFlowDemo();
                    break; // Exit early if ACK is received
                }
            }

            if (!ackReceived) {
                retries++;
                Serial.println("No ACK received. Retrying...");
            } else {
                Serial.println("Message sent successfully!");
                txNumber += 0.01; // Increment the message number
            }
        }

        if (!ackReceived) {
            Serial.println("Failed to send message after maximum retries.");
        }

        lora_idle = true; // Reset LoRa status
        Radio.Rx(0);      // Switch back to receive mode
    }
    Radio.IrqProcess();
}

// Callback when transmission is done
void OnTxDone(void) {
    Serial.println("TX done...");
    Radio.Rx(0); // Switch to RX mode to listen for ACK
    lora_idle = true;
}

// Callback when transmission times out
void OnTxTimeout(void) {
    Serial.println("TX timeout...");
    lora_idle = true;
}

// Callback when a message is received
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) {
    payload[size] = '\0'; // Null-terminate the received message
    Serial.printf("Received: %s | RSSI: %d | SNR: %d\n", (char *)payload, rssi, snr);

    if (strncmp((char *)payload, "ACK", 3) == 0) {
        Serial.println("ACK received!");
        ackReceived = true; // Set a flag to indicate ACK reception
    }
    Radio.Sleep(); // Put the radio in sleep mode to save power
}

void drawTextFlowDemo() 
{
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawStringMaxWidth(0, 0, 128,"Se recibio el mensaje");
  String mensajes = "Mensajes recibidos: " + String(intentos);
  display.drawStringMaxWidth(0, 40, 128, mensajes);
  display.display();
  delay(2000);  
  display.clear();
  display.display();
}

void VextON(void)
{
  pinMode(Vext,OUTPUT);
  digitalWrite(Vext, LOW);
}