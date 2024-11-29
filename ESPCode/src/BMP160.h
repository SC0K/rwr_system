#include <Adafruit_BMP085.h>
#include <Wire.h>
#include <TCA9548.h>

class BMPSensor {
private:
    Adafruit_BMP085 bmp;  // BMP085 instance
    TCA9548 *mp;          // Pointer to the I2C multiplexer	
    uint8_t i2c_address;  // I2C address of the sensor
    uint8_t bus_num;      // I2C bus number
    bool initialized;     // Status of sensor initialization

public:
    // Constructor
    BMPSensor(uint8_t bus_num, TCA9548 *mp, uint8_t address = 0x77);

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
