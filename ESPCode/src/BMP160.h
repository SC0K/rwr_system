#include <Adafruit_BMP085.h>
#include <Wire.h>

class BMPSensor {
private:
    Adafruit_BMP085 bmp;  // BMP085 instance
    TwoWire *i2c;         // Pointer to the I2C interface
    uint8_t i2c_address;  // I2C address of the sensorC
    uint8_t bus_num;      // I2C bus number
    bool initialized;     // Status of sensor initialization

public:
    // Constructor
    BMPSensor(uint8_t bus_num, uint8_t address = 0x77);

    // Destructor
    ~BMPSensor();

    // Initialize the sensor
    bool begin();

    // Check if the sensor is initialized
    bool isInitialized() const;

    // Read pressure in Pascals
    float readPressure();

    // Read temperature in Celsius
    float readTemperature();
};

#endif // BMPSENSOR_H
