#include <Arduino.h>
#include <ESP32Servo.h>
#include <micro_ros_arduino.h>
#include <rmw_microros/rmw_microros.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <rcutils/allocator.h>
#include <WiFi.h>
#include <std_msgs/msg/int32_multi_array.h>

// Wi-Fi credentials
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// Servo instances
Servo servo1, servo2, servo3, servo4, servo5;

// Servo positions
int pos = 0;
int sensor_positions[5] = {0, 0, 0, 0, 0};

// ROS variables
rcl_subscription_t subscriber;
std_msgs__msg__Int32MultiArray msg;
rclc_executor_t executor;

// Function prototypes
void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5);
void servo_positions_callback(const void *msg_in);
bool transport_custom_open(struct uxrCustomTransport * transport);
bool transport_custom_close(struct uxrCustomTransport * transport);
size_t transport_custom_write(struct uxrCustomTransport* transport, const uint8_t* buf, size_t len, uint8_t* err);
size_t transport_custom_read(struct uxrCustomTransport* transport, uint8_t* buf, size_t len, int timeout, uint8_t* err);

void setup() {
    // Initialize serial communication
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to Wi-Fi");

    // Initialize micro-ROS
    rmw_uros_set_custom_transport(
        false,
        (void *)NULL,
        transport_custom_open,
        transport_custom_close,
        transport_custom_write,
        transport_custom_read
    );

    rcl_allocator_t allocator = rcl_get_default_allocator();
    rclc_support_t support;
    rclc_support_init(&support, 0, NULL, &allocator);

    rcl_node_t node;
    rclc_node_init_default(&node, "esp32_node", "", &support);

    rclc_subscription_init_default(
        &subscriber,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32MultiArray),
        "servo_positions"
    );

    rclc_executor_init(&executor, &support.context, 1, &allocator);
    rclc_executor_add_subscription(
        &executor,
        &subscriber,
        &msg,
        &servo_positions_callback,
        ON_NEW_DATA
    );

    // Initialize servos
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    ESP32PWM::allocateTimer(2);
    ESP32PWM::allocateTimer(3);

    servo1.setPeriodHertz(50);
    servo2.setPeriodHertz(50);
    servo3.setPeriodHertz(50);
    servo4.setPeriodHertz(50);
    servo5.setPeriodHertz(50);

    servo1.attach(12, 500, 2400);
    servo2.attach(14, 500, 2400);
    servo3.attach(27, 500, 2400);
    servo4.attach(26, 500, 2400);
    servo5.attach(25, 500, 2400);
}

void loop() {
    rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
    write_servos(
        sensor_positions[0],
        sensor_positions[1],
        sensor_positions[2],
        sensor_positions[3],
        sensor_positions[4]
    );
}

void servo_positions_callback(const void *msg_in) {
    const std_msgs__msg__Int32MultiArray *msg = (const std_msgs__msg__Int32MultiArray *)msg_in;

    if (msg->data.size >= 5) {
        for (int i = 0; i < 5; i++) {
            sensor_positions[i] = msg->data.data[i];
        }
    }
}

void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5) {
    servo1.write(pos1);
    servo2.write(pos2);
    servo3.write(pos3);
    servo4.write(pos4);
    servo5.write(pos5);
}

// Custom transport functions for Micro-ROS
bool transport_custom_open(struct uxrCustomTransport * transport) {
    return true;
}

bool transport_custom_close(struct uxrCustomTransport * transport) {
    return true;
}

size_t transport_custom_write(struct uxrCustomTransport* transport, const uint8_t* buf, size_t len, uint8_t* err) {
    return WiFiClient().write(buf, len);
}

size_t transport_custom_read(struct uxrCustomTransport* transport, uint8_t* buf, size_t len, int timeout, uint8_t* err) {
    return WiFiClient().readBytes(buf, len);
}
