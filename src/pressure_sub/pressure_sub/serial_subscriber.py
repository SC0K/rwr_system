import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import serial

class SerialFloatPublisher(Node):
    def __init__(self):
        super().__init__('serial_float_publisher')
        self.publisher = self.create_publisher(Float32MultiArray, 'pressure_data', 10)
        self.serial_port = '/dev/ttyACM0'  # Replace with your serial port
        self.baud_rate = 115200
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Read every 1 second

    def timer_callback(self):
        # Read a line from the serial port
        line = self.ser.readline().decode('utf-8').strip()

        # Split the line into individual float values (assuming space-separated floats)
        try:
            float_values = [float(val) for val in line.split()]
            if len(float_values) == 5:  # Ensure there are exactly 5 floats
                # Create a Float32MultiArray message
                msg = Float32MultiArray()
                msg.data = float_values
                self.publisher.publish(msg)
                self.get_logger().info(f'Publishing: {msg.data}')
            else:
                self.get_logger().warn(f'Invalid data received: {line}')
        except ValueError:
            self.get_logger().warn(f'Failed to convert data to floats: {line}')

def main(args=None):
    rclpy.init(args=args)
    node = SerialFloatPublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
