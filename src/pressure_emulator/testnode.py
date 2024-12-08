#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import math
import time

class SmoothPressurePublisher(Node):
    def __init__(self):
        super().__init__('smooth_pressure_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'pressure_values', 10)
        self.timer = self.create_timer(0.1, self.publish_pressure_values)  # Publish every 0.1 seconds
        self.start_time = time.time()

    def publish_pressure_values(self):
        # Time since the node started
        elapsed_time = time.time() - self.start_time

        # Generate pressure values based on sine wave (oscillating between 0 and 100)
        pressure_values = [
            50 + 50 * math.sin(elapsed_time + i) for i in range(5)  # Offset each sensor by `i`
        ]

        # Create and publish the message
        msg = Float32MultiArray()
        msg.data = pressure_values
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published pressure values: {pressure_values}")

def main(args=None):
    rclpy.init(args=args)
    node = SmoothPressurePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
