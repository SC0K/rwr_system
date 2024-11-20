#include <Arduino.h>
#include <micro_ros_arduino.h>
#include "BMP160.h"
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <std_msgs/msg/float32.h>

// Define BMP sensors
BMPSensor bmp1(27, 14, 0);
//BMPSensor bmp1(35, 34, 0);

// ROS variables
rcl_node_t node;
rcl_publisher_t publisher_bmp1;
std_msgs__msg__Float32 msg;

void setup() {
    Serial.begin(115200);
    delay(100);

    // Initialize Micro-ROS
    set_microros_serial_transports(Serial);
    rcl_allocator_t allocator = rcl_get_default_allocator();
    rclc_support_t support;
    rclc_support_init(&support, 0, NULL, &allocator);
    rclc_node_init_default(&node, "bmp_sensor_node", "", &support);

    // Initialize publishers
    rclc_publisher_init_default(&publisher_bmp1, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32), "sensor/bmp1/pressure");

    // Initialize sensors
    if (!bmp1.begin()) Serial.println("Failed to initialize BMP1!");
}

void loop() {
    // Publish pressure data for each sensor with serial debug
    if (bmp1.isInitialized()) {
        msg.data = bmp1.readPressure();
        rcl_publish(&publisher_bmp1, &msg, NULL);
        Serial.print(">pressure1:");
        Serial.println(msg.data);
    }

    delay(1000); // Publish at 1Hz
}
