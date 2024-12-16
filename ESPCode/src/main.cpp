#include <Arduino.h>
#include <micro_ros_arduino.h>
#include "BMP160.h"
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/float32_multi_array.h>
#include <TCA9548.h>

// Define publishing period in milliseconds
int publishing_period_ms = 1000;

// Define multiplexer and BMP sensors
TCA9548 mp(0x70);
BMPSensor bmp1(7, &mp);
BMPSensor bmp2(6, &mp);
BMPSensor bmp3(5, &mp);
BMPSensor bmp4(3, &mp);
BMPSensor bmp5(2, &mp);

// Define pressures for sensors
float press1 = 0, press2 = 0, press3 = 0, press4 = 0, press5 = 0;

// Micro-ROS structures
rcl_node_t node;
rcl_publisher_t publisher;
std_msgs__msg__Float32MultiArray msg;

void setup()
{
    // Initialize serial and I2C
    Wire.begin();
    Serial.begin(115200);

    // Set up Micro-ROS transport
    set_microros_transports();

    rcl_allocator_t allocator = rcl_get_default_allocator();
    rclc_support_t support;
    rclc_support_init(&support, 0, NULL, &allocator);

    // Initialize ROS node and publisher
    rclc_node_init_default(&node, "bmp_sensor_node", "", &support);

    rclc_publisher_init_default(
        &publisher,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32MultiArray),
        "sensor/pressures");

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

    msg.data.size = 5;
    msg.data.capacity = 5;
    msg.data.data = (float *)malloc(5 * sizeof(float));

    for (size_t i = 0; i < msg.data.size; i++)
    {
        msg.data.data[i] = 0.0f; // Set initial values to zero
    }
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

    // Update the Float32MultiArray message data
    msg.data.data[0] = press1;
    msg.data.data[1] = press2;
    msg.data.data[2] = press3;
    msg.data.data[3] = press4;
    msg.data.data[4] = press5;

    // Publish the message
    rcl_publish(&publisher, &msg, NULL);

    // Delay for the publishing period
    //delay(publishing_period_ms);
}
