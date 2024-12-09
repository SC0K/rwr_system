#include <Arduino.h>
#include <ESP32Servo.h>
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/float32_multi_array.h>

// Servo instances
Servo servo1, servo2, servo3, servo4, servo5;

// Servo position range
int min_pos = 70;
int max_pos = 160;

// Pressure sensor min and max values (adjust as needed)
float pressure_min[5] = {10.0, 20.0, 15.0, 5.0, 25.0};
float pressure_max[5] = {100.0, 90.0, 80.0, 50.0, 120.0};

// ROS-related objects
rcl_subscription_t subscriber;
std_msgs__msg__Float32MultiArray msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

// Function prototypes
void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5);
void servo_positions_callback(const void *msg_in);
float normalize(float value, float min_value, float max_value);
float scale(float normalized, int min_pos, int max_pos);

void setup() {
    // Initialize serial communication
    Serial.begin(115200);

    // Initialize Micro-ROS
    set_microros_transports(); // Ensure you have the correct transport setup
    allocator = rcl_get_default_allocator();

    // Create support and node
    rclc_support_init(&support, 0, NULL, &allocator);
    rclc_node_init_default(&node, "servo_controller_node", "", &support);

    // Initialize subscriber
    rclc_subscription_init_default(
        &subscriber,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32MultiArray),
        "pressure_values"
    );

    // Initialize executor
    rclc_executor_init(&executor, &support.context, 1, &allocator);
    rclc_executor_add_subscription(
        &executor,
        &subscriber,
        &msg,
        &servo_positions_callback,
        ON_NEW_DATA
    );

    // Attach servos
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

    Serial.println("Setup complete.");
}

void loop() {
    // Spin the Micro-ROS executor
    rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
}

// Callback to handle received pressure values
void servo_positions_callback(const void *msg_in) {
    const std_msgs__msg__Float32MultiArray *msg = (const std_msgs__msg__Float32MultiArray *)msg_in;

    if (msg->data.size == 5) {
        // Normalize and scale pressure values for each servo
        int scaled_positions[5];
        for (int i = 0; i < 5; i++) {
            float normalized = normalize(msg->data.data[i], pressure_min[i], pressure_max[i]);
            scaled_positions[i] = (int)scale(normalized, min_pos, max_pos);
        }

        // Write to servos
        write_servos(
            scaled_positions[0],
            scaled_positions[1],
            scaled_positions[2],
            scaled_positions[3],
            scaled_positions[4]
        );
    } else {
        Serial.println("Received invalid data size!");
    }
}

// Write positions to all servos
void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5) {
    servo1.write(pos1);
    servo2.write(pos2);
    servo3.write(pos3);
    servo4.write(pos4);
    servo5.write(pos5);
}

// Normalize a value between 0 and 1
float normalize(float value, float min_value, float max_value) {
    return (value - min_value) / (max_value - min_value);
}

// Scale a normalized value to the servo range
float scale(float normalized, int min_pos, int max_pos) {
    return min_pos + normalized * (max_pos - min_pos);
}
