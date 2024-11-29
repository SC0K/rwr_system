#include "BMP160.h"

// Constructor
BMPSensor::BMPSensor(uint8_t bus_num, uint8_t address): bus_num(bus_num), i2c_address(address), initialized(false) {
    i2c = new TwoWire(bus_num); // Create a new TwoWire instance
}

// Destructor
BMPSensor::~BMPSensor() {
    delete i2c;
}

// Initialize the sensor
bool BMPSensor::begin() {
    i2c->begin(sda_pin, scl_pin);
    delay(10); // Allow time for the sensor to stabilize
    initialized = bmp.begin(i2c_address, i2c);
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
    return bmp.readPressure();
}

// Read temperature in Celsius
float BMPSensor::readTemperature() {
    if (!initialized) {
        Serial.println("Error: Sensor not initialized!");
        return -1;
    }
    return bmp.readTemperature();
}
