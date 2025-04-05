#include <Arduino.h>
#include "BMP160.h"
#include <TCA9548.h>

// Define publishing period in milliseconds
int publishing_period_ms = 10;

// Define multiplexer and BMP sensors
TCA9548 mp(0x70);
BMPSensor bmp1(7, &mp);
BMPSensor bmp2(6, &mp);
BMPSensor bmp3(5, &mp);
BMPSensor bmp4(3, &mp);
BMPSensor bmp5(2, &mp);

// Define pressures for sensors
float press1 = 0, press2 = 0, press3 = 0, press4 = 0, press5 = 0;

void setup()
{
    // Initialize serial and I2C
    Wire.begin();
    Serial.begin(115200);

    // Initialize sensors
    if (!bmp1.begin())
        Serial.println("Failed to initialize BMP1!");
    if (!bmp2.begin())
        Serial.println("Failed to initialize BMP2!");
    if (!bmp3.begin())
        Serial.println("Failed to initialize BMP3!");
    if (!bmp4.begin())
        Serial.println("Failed to initialize BMP4!");
    if (!bmp5.begin())
        Serial.println("Failed to initialize BMP5!");
}

void loop()
{
    // Read pressures from the sensors
    if (bmp1.isInitialized())
        press1 = bmp1.readPressure();
    if (bmp2.isInitialized())
        press2 = bmp2.readPressure();
    if (bmp3.isInitialized())
        press3 = bmp3.readPressure();
    if (bmp4.isInitialized())
        press4 = bmp4.readPressure();
    if (bmp5.isInitialized())
        press5 = bmp5.readPressure();

    // Output the pressure data to the serial port
    // Serial.print("Pressure1: ");
    Serial.print(press1);
    // Serial.print(", Pressure2: ");
    Serial.print(" ");
    Serial.print(press2);
    // Serial.print(", Pressure3: ");
    Serial.print(" ");
    Serial.print(press3);
    // Serial.print(", Pressure4: ");
    Serial.print(" ");
    Serial.print(press4);
    // Serial.print(", Pressure5: ");
    Serial.print(" ");
    Serial.println(press5);

    // Delay for the publishing period
    delay(publishing_period_ms);
}