import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import csv
import time

class PressureRecorder(Node):
    def __init__(self):
        super().__init__('pressure_recorder')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'pressure_data',
            self.pressure_callback,
            10
        )
        self.subscription  # prevent unused variable warning

        # Open a CSV file to record the data
        self.csv_file = open('pressure_data.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Pressure1', 'Pressure2', 'Pressure3', 'Pressure4', 'Pressure5'])

        # Timer to control recording frequency (every 0.5 seconds)
        self.last_record_time = time.time()

    def pressure_callback(self, msg: Float32MultiArray):
        current_time = time.time()
        if current_time - self.last_record_time >= 0.5:  # Record every 0.5 seconds
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
            row = [timestamp] + list(msg.data)
            self.csv_writer.writerow(row)
            self.get_logger().info(f'Recorded data: {row}')
            self.last_record_time = current_time

    def destroy_node(self):
        # Close the CSV file when the node is destroyed
        self.csv_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = PressureRecorder()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()