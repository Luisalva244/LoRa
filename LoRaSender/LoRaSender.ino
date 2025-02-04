//Heltec Automation LoRa Sender with ACK Handling */

#include <Wire.h>               
#include "HT_SSD1306Wire.h"
#include "LoRaWan_APP.h"
#include "Arduino.h"
#include <HardwareSerial.h>
#include <HT_TinyGPS++.h>
 
#define RF_FREQUENCY                                920000000 // Hz
#define TX_OUTPUT_POWER                             20        // dBm
#define LORA_BANDWIDTH                              0         // [0: 125 kHz, 1: 250 kHz, 2: 500 kHz, 3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5, 2: 4/6, 3: 4/7, 4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false
#define RX_TIMEOUT_VALUE                            1000
#define BUFFER_SIZE                                 64 // Define the payload size

static SSD1306Wire  display(0x3c, 500000, SDA_OLED, SCL_OLED, GEOMETRY_128_64, RST_OLED); // addr , freq , i2c group , resolution , rst

HardwareSerial SerialGPS(2);
TinyGPSPlus gps;

static const int RXPin = 21;
static const int TXPin = 26;
static const uint32_t GPSBaud = 9600;

char txpacket[BUFFER_SIZE];
int txNumber = 0;        // Contador de mensajes
char nodeNumber = '1';

enum options
{
  HUMIDITY,
  GPS
};

/*Flags*/
bool gpsUpdate = false;     // Hay datos nuevos GPS
bool lora_idle = true;      // Radio lista
bool ackReceived = false;   // Flag de ACK


#pragma pack(push, 1)
struct payLoad 
{
  char  node;       
  float humidity;  
  float latituded;  
  float longituded; 
  float altitude;   
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

void GPSLocation();
void drawText(char node, options op);
void sendMessage(options op);
void VextON(void);

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

void loop() 
{

  GPSLocation();

  if (lora_idle) 
  {
    ackReceived = false; // Reset ACK flag

    if (!gpsUpdate) {
      sendMessage(HUMIDITY);
    } else {
      sendMessage(GPSDATA);
      gpsUpdate = false; 
    }

    unsigned long start = millis();
    while (millis() - start < 1000) {
      Radio.IrqProcess(); // manejar interrupciones
      if (ackReceived) {
        Serial.println("ACK received => Success!");
        txNumber ++; // Increment the message number
        break;
      }
    }

    if (!ackReceived) {
      Serial.println("No ACK received. Retrying...");
    }  
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

void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) 
{
  payload[size] = '\0';
  Serial.printf("Received: %s | RSSI: %d | SNR: %d\n", (char *)payload, rssi, snr);

  if (strncmp((char *)payload, "ACK", 3) == 0) 
  {
    ackReceived = true;
  }
  Radio.Sleep();
}

void drawText(char node, options op) 
{
  display.clear();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);

  if (op == HUMIDITY)
  {     
    
    //String(humidity)
    String message = "Humidity: " + String(20) + "Node: " + String(node);
    display.drawStringMaxWidth(0, 0, 128,messsage);

    // TODO function to handle this hardcode xdd and dirtty code 
    float alt = LoRaPayLoad.altitude;
    String altMsg = "Alt=" + String(alt);
    display.drawStringMaxWidth(0, 20, 128, altMsg);

    float lon = LoRaPayLoad.longituded;
    String lonMsg = "Lon=" + String(lon);
    display.drawStringMaxWidth(60, 20, 128, lonMsg);

    float lat = LoRaPayLoad.latituded;
    String latMsg = "Lat=" + String(lat);
    display.drawStringMaxWidth(0, 40, 128, latMsg);

    String messagesCompleted = "txNumber=" + String(txNumber);
    display.drawStringMaxWidth(60, 40, 128, messagesCompleted);

  } else if (op == GPS)
  {
    
    String message = "Humidity: " + String(40) + "Node: " + String(node);
    display.drawStringMaxWidth(0, 0, 128,messsage);

    float alt = LoRaPayLoad.altitude;
    String altMsg = "Alt=" + String(alt);
    display.drawStringMaxWidth(0, 20, 128, altMsg);

    float lon = LoRaPayLoad.longituded;
    String lonMsg = "Lon=" + String(lon);
    display.drawStringMaxWidth(60, 20, 128, lonMsg);

    float lat = LoRaPayLoad.latituded;
    String latMsg = "Lat=" + String(lat);
    display.drawStringMaxWidth(0, 40, 128, latMsg);

    String messagesCompleted = "txNumber=" + String(txNumber);
    display.drawStringMaxWidth(60, 40, 128, messagesCompleted);

  }
  
  display.display();    

}

void VextON(void)
{
  pinMode(Vext,OUTPUT);
  digitalWrite(Vext, LOW);
}

void GPSLocation(void)
{
  if (txNumber > 100)
  {
    while(SerialGPS.available()>0)
    {
     gps.encode(SerialGPS.read());

     if (gps.location.isUpdated())
     {
      LoRaPayLoad.latituded  = gps.location.lat();
      LoRaPayLoad.longituded = gps.location.lng();
      LoRaPayLoad.altitude   = gps.altitude.meters();

      Serial.print("Lat: ");
      Serial.println(LoRaPayLoad.latituded, 6);
      Serial.print("Lon: ");
      Serial.println(LoRaPayLoad.longituded, 6);
      Serial.print("Alt: ");
      Serial.println(LoRaPayLoad.altitude, 2);
      Serial.print("Sats: ");
      Serial.println(gps.satellites.value());
      Serial.println();

      gpsUpdate = true;
      }
    }
    txNumber = 0;
  }
}

void sendMessage(options op)
{
  LoRaPayLoad.node = nodeNumber;

  switch(op)
  {
    case HUMIDITY:
      LoRaPayLoad.humidity = 20;  
      LoRaPayLoad.latituded  = 0;
      LoRaPayLoad.longituded = 0;
      LoRaPayLoad.altitude   = 0;
      drawText(nodeNumber, HUMIDITY);

      break;
    
    case GPSDATA:
      LoRaPayLoad.humidity = 40; 
      drawText(nodeNumber, GPSDATA);

      break;
    

  } 

  Radio.Send((uint8_t*)&LoRaPayLoad, sizeof(LoRaPayLoad));
  lora_idle = false;
  Serial.printf("Sending struct [node=%c hum=%d lat=%.6f lon=%.6f alt=%.2f]\n",
                LoRaPayLoad.node,
                LoRaPayLoad.humidity,
                LoRaPayLoad.latituded,
                LoRaPayLoad.longituded,
                LoRaPayLoad.altitude);
}