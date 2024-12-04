#include <Arduino.h>
#include <micro_ros_arduino.h>
#include "BMP160.h"
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/float32_multi_array.h>
#include <TCA9548.h>

// #define SERIAL // debug disables Serial debugging
bool serial = false;

int publishing_period_ms = 50;

TCA9548 mp(0x70);

BMPSensor bmp1(7, &mp);
BMPSensor bmp2(6, &mp);
BMPSensor bmp3(5, &mp);
BMPSensor bmp4(3, &mp);
BMPSensor bmp5(2, &mp);

float press1 = 0;
float press2 = 0;
float press3 = 0;
float press4 = 0;
float press5 = 0;

rcl_node_t node;
rcl_publisher_t publisher;
std_msgs__msg__Float32MultiArray msg;

void setup()
{
    if (serial) {
        Serial.begin(115200);
    }
    Wire.begin();

    if (!serial) {
        set_microros_transports();

        rcl_allocator_t allocator = rcl_get_default_allocator();
        rclc_support_t support;
        rclc_support_init(&support, 0, NULL, &allocator);

        rclc_node_init_default(&node, "bmp_sensor_node", "", &support);

        rclc_publisher_init_default(
            &publisher,
            &node,
            ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32MultiArray),
            "sensor/pressures");
    }

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

    msg.data.capacity = 5;
    msg.data.size = 5;
    msg.data.data = (float *)malloc(5 * sizeof(float));
}

void loop()
{
    if (bmp1.isInitialized())
    {
        press1 = bmp1.readPressure();
    }
    if (bmp2.isInitialized())
    {
        press2 = bmp2.readPressure();
    }
    if (bmp3.isInitialized())
    {
        press3 = bmp3.readPressure();
    }
    if (bmp4.isInitialized())
    {
        press4 = bmp4.readPressure();
    }
    if (bmp5.isInitialized())
    {
        press5 = bmp5.readPressure();
    }

    msg.data.data[0] = press1;
    msg.data.data[1] = press2;
    msg.data.data[2] = press3;
    msg.data.data[3] = press4;
    msg.data.data[4] = press5;

    if (serial) {
        Serial.print(">pressure1:");
        Serial.println(press1);
        Serial.print(">pressure2:");
        Serial.println(press2);
        Serial.print(">pressure3:");
        Serial.println(press3);
        Serial.print(">pressure4:");
        Serial.println(press4);
        Serial.print(">pressure5:");
        Serial.println(press5);
    }
    else {
        rcl_publish(&publisher, &msg, NULL);
    }

    delay(publishing_period_ms);
}
