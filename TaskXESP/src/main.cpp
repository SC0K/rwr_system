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
int min_pos = 160;
int max_pos = 70;

// Pressure sensor min and max values (adjust as needed)
float pressure_min[5] = {124674.0, 137000.0, 138261.0, 129000.0, 143000.0};
float pressure_max[5] = {160000.0, 169000.0, 181000.0, 166000.0, 150000.0};

float norm[5];
int pos[5];

// ROS-related objects
rcl_subscription_t subscriber = rcl_get_zero_initialized_subscription();
rclc_executor_t executor = rclc_executor_get_zero_initialized_executor();
std_msgs__msg__Float32MultiArray msg;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node = rcl_get_zero_initialized_node();

// Function prototypes
void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5);
void servo_positions_callback(const void * msg_in);
float normalize(float value, float min_value, float max_value);
float scale(float normalized, int min_pos, int max_pos);

// Callback to handle received pressure values
void servo_positions_callback(const void *msg_in) {

    // Debug message
    Serial2.println("Callback triggered!");
    const std_msgs__msg__Float32MultiArray *msg_copy = (const std_msgs__msg__Float32MultiArray *)msg_in;
    Serial2.printf("Received message with %zu elements\n", msg_copy->data.size);
    for (size_t i = 0; i < msg_copy->data.size; i++) {
        Serial2.printf("Data[%zu]: %f\n", i, msg_copy->data.data[i]);
    }

    // Normalize and scale pressure values to servo positions
    Serial2.print("Normalized values:");
    for (size_t i = 0; i < 5; i++) {
        norm[i] = normalize(msg_copy->data.data[i], pressure_min[i], pressure_max[i]);
        Serial2.print(norm[i]);
        Serial2.print(" ");
    }

    for (size_t i = 0; i < 5; i++) {
        pos[i] = scale(norm[i], min_pos, max_pos);
    }

    write_servos(pos[0], pos[1], pos[2], pos[3], pos[4]);
}

// Write positions to all servos
void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5) {
    servo1.write(pos1);
    servo2.write(pos2);
    servo3.write(pos3);
    servo4.write(pos4);
    servo5.write(pos5);

    Serial2.printf("Servo positions written: %d, %d, %d, %d, %d\n", pos1, pos2, pos3, pos4, pos5);
}

// Normalize a value between 0 and 1
float normalize(float value, float min_value, float max_value) {
    return (value - min_value) / (max_value - min_value);
}

// Scale a normalized value to the servo range
float scale(float normalized, int min_pos, int max_pos) {
    return min_pos + normalized * (max_pos - min_pos);
}

void setup() {
    // Initialize serial communication
    Serial2.begin(115200);
    Serial2.println("Initializing Micro-ROS...");

    // Initialize Micro-ROS
    set_microros_transports();
    allocator = rcl_get_default_allocator();

    // Create support and node
    rclc_support_init(&support, 0, NULL, &allocator);
    rclc_node_init_default(&node, "servo_controller_node", "", &support);

    rclc_subscription_init_default(
        &subscriber, 
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32MultiArray),
        "/sensor/pressures");


    // Allocate memory for the array (adjust size as needed)
    size_t array_size = 5;  // Example: an array with 10 elements
    msg.data.data = (float *)malloc(array_size * sizeof(float));
    msg.data.capacity = array_size;
    msg.data.size = array_size;
    

    // Initialize executor
    rclc_executor_init(&executor, &support.context, 1, &allocator);
    rclc_executor_add_subscription(
        &executor,
        &subscriber,
        &msg,
        &servo_positions_callback,
        ON_NEW_DATA
    );

    Serial2.println("Micro-ROS initialized successfully.");

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
    delay(1000);
    Serial2.println("Servos attached and setup complete.");
}

void loop() {
    int feedback = rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
    if(feedback != RCL_RET_OK){
        Serial2.println("Error in spin_some()");
    }
    
}
