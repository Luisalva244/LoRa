#include "MessageSender.h"
#include "LoRaSender.h"  // Para obtener la definición de nodehourData
#include <string.h>



void MessageSender::sendDataMessage(const cropData &cropData) 
{
    Radio.Send((uint8_t*)&cropData, sizeof(cropData));
    Serial.printf("Enviando payload [receiverNode=%s, senderNode=%s,soilHum=%.2f, Hum=%.2f, Temp=%.2f]\n",
                  cropData.receiverAddress,
                  cropData.senderAddress,
                  cropData.soilHumidity,
                  cropData.Humidity,
                  cropData.Temperature);
}

void MessageSender::sendCommandMessage(const requestHour &requestHour) 
{
    Radio.Send((uint8_t*)&requestHour, sizeof(requestHour));
    Serial.printf("Enviando comando [node=%s, command=%s]\n",
                  requestHour.node,
                  requestHour.command);
} 

void MessageSender::sendHourMessage(const nodehourData &nhData) {
    // Envía el mensaje usando la función de Radio (asegúrate de que Radio.Send esté definida)
    Radio.Send((uint8_t*)&nhData, sizeof(nhData));
    Serial.printf("Sent hour message: node %s, hour %d\n", nhData.node, nhData.hour);
}

