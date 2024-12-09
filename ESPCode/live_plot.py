#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import matplotlib.pyplot as plt
import threading

class LivePlot(Node):
    def __init__(self, topic_name):
        super().__init__('live_plot')
        self.data = [[] for _ in range(5)]  # One list for each sensor
        self.lock = threading.Lock()
        self.topic_name = topic_name

        # Create a subscriber
        self.subscription = self.create_subscription(
            Float32MultiArray,
            self.topic_name,
            self.callback,
            10
        )

        # Start plotting thread
        self.plot_thread = threading.Thread(target=self.plot_data)
        self.plot_thread.daemon = True
        self.plot_thread.start()

    def callback(self, msg):
        """Callback to handle incoming messages."""
        with self.lock:
            for i in range(5):
                self.data[i].append(msg.data[i])
                if len(self.data[i]) > 100:
                    self.data[i] = self.data[i][-100:]  # Keep only the last 100 points

    def plot_data(self):
        """Function to continuously update the plot."""
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()

        while rclpy.ok():
            with self.lock:
                current_data = [list(sensor_data) for sensor_data in self.data]

            ax.clear()
            for i, sensor_data in enumerate(current_data):
                ax.plot(sensor_data, label=f'Sensor {i+1}')

            ax.set_title(f'Live Data from {self.topic_name}')
            ax.set_xlabel('Time Step')
            ax.set_ylabel('Value')
            ax.set_xlim(0, 100)
            ax.legend()
            plt.pause(0.1)

if __name__ == '__main__':
    try:
        rclpy.init()
        topic_name = '/sensor/pressures'  # Replace with your topic name
        node = LivePlot(topic_name)

        # Spin the node to keep it alive
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()