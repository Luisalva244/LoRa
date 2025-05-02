#ifndef MESSAGE_SENDER_H
#define MESSAGE_SENDER_H

#include "Arduino.h"
#include "LoRaSender.h"  

// Clase que maneja el envío de distintos mensajes
class MessageSender {
public:
    
    // Envía payload de datos
    void sendDataMessage(const cropData &cropData);
    
    // Envía un mensaje de comando 
    void sendCommandMessage(const requestHour &requestHour);
    
    void sendHourMessage(const nodehourData &nhData);

};



#endif // MESSAGE_SENDER_H