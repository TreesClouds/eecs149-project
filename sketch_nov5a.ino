#include <SoftwareSerial.h>
SoftwareSerial BTserial(2, 3); // RX on Pin 2, TX on Pin 3

char c = ' '; 
char buf[8];  // Buffer size of 8 to hold incoming characters
int bufIndex = 0;  // Index to track position in the buffer

void setup()
{
    Serial.begin(9600);
    Serial.print("Sketch:   ");   Serial.println(__FILE__);
    Serial.print("Uploaded: ");   Serial.println(__DATE__);
    Serial.println(" ");

    BTserial.begin(9600);
    Serial.println("BTserial started at 9600");
    pinMode(LED_BUILTIN, OUTPUT);


}

void loop()
{
    // Read from the Bluetooth module and send to the Arduino Serial Monitor
    if (BTserial.available())
    {
        c = BTserial.read();
        buf[bufIndex++] = c;

        if (bufIndex >= sizeof(buf)) {
          bufIndex = 0;
        }
        
    if (bufIndex >= 5 && strncmp(buf + bufIndex - 5, "light", 5) == 0) {
      digitalWrite(LED_BUILTIN, HIGH);  // Turn on the LED
      bufIndex = 0;  // Reset the buffer for the next command
    } else{
          digitalWrite(LED_BUILTIN, LOW);
        }
        Serial.write(c);
    }

    //Read from the Serial Monitor and send to the Bluetooth module
    if (Serial.available())
    {
        c = Serial.read();
        BTserial.write(c);
        Serial.write(c);
    }
}