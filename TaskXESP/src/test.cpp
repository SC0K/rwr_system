#include <Arduino.h>
#include <ESP32Servo.h>


// Servo instances
Servo servo1, servo2, servo3, servo4, servo5;

int min_pos = 160;
int max_pos = 70;
// Servo positions
int pos = 0;
int sensor_positions[5] = {0, 0, 0, 0, 0};

// Function prototypes
void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5);
void servo_positions_callback(const void *msg_in);

void setup() {
    // Initialize serial communication
    Serial.begin(115200);

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
    // Gradually increase servo positions to 90 degrees
    if (true){
    for (int pos = min_pos; pos >= max_pos; pos--) {

        write_servos(pos, pos, pos, pos, pos);
        delay(15); // Adjust speed of movement (15 ms delay per step)
    }

    // Gradually decrease servo positions back to 0 degrees
    for (int pos = max_pos; pos <= min_pos; pos++) {
        write_servos(pos, pos, pos, pos, pos);
        delay(15); // Adjust speed of movement (15 ms delay per step)
    }}
    else{
        pos = 180;
        write_servos(pos, pos, pos, pos, pos);
    }
}
void write_servos(int pos1, int pos2, int pos3, int pos4, int pos5) {
    servo1.write(pos1);
    servo2.write(pos2);
    servo3.write(pos3);
    servo4.write(pos4);
    servo5.write(pos5);
}
