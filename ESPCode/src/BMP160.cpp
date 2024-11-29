#include "BMP160.h"
#include <TCA9548.h>
#include <Wire.h>

// Constructor
BMPSensor::BMPSensor(uint8_t bus_num, TCA9548 *mp, uint8_t address): bus_num(bus_num), mp(mp), i2c_address(address), initialized(false) {

}

// Destructor
BMPSensor::~BMPSensor() {
    delete mp;
}

// Initialize the sensor
bool BMPSensor::begin() {
    mp->selectChannel(bus_num);
    initialized = bmp.begin(i2c_address, &Wire);
    return initialized;
}

// Check if the sensor is initialized
bool BMPSensor::isInitialized() const {
    return initialized;
}

// Read pressure in Pascals
float BMPSensor::readPressure() {
    if (!initialized) {
        Serial.println("Error: Sensor not initialized!");
        return -1;
    }
    mp->selectChannel(bus_num);
    return bmp.readPressure();
}

// Read temperature in Celsius
float BMPSensor::readTemperature() {
    if (!initialized) {
        Serial.println("Error: Sensor not initialized!");
        return -1;
    }
    mp->selectChannel(bus_num);
    return bmp.readTemperature();
}
