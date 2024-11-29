#!/bin/env python3

import rclpy
from rclpy.node import Node
import rosbag2_py
import yaml
from pathlib import Path
from datetime import datetime
from std_msgs.msg import Float32MultiArray, Float32
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from bag2h5_converter import convert_to_h5
from rclpy.serialization import serialize_message

# Define supported topics and message types
topics_types = {
    "/franka/end_effector_pose": PoseStamped,
    "/hand/policy_output": Float32MultiArray,
    "/oakd_front_view/color": Image,
    "/oakd_side_view/color": Image,
    "/oakd_wrist_view/color": Image,
    "/sensor/bmp1/pressure": Float32,  # New pressure sensor topic
}

class DemoLogger(Node):
    def __init__(self, topics_to_record, base_path):
        super().__init__('demo_logger')
        print("DemoLogger.__init__")
        
        self.base_path = Path(base_path)
        self.task_name = None
        self.writer = None
        self.topics_to_record = topics_to_record
        
        if not self.topics_to_record:
            self.get_logger().error("No topics specified to record. Check the configuration file.")
            return

        # Ensure the base directory exists
        if not self.base_path.exists():
            self.base_path.mkdir(parents=True, exist_ok=True)
            self.get_logger().info(f"Base directory '{self.base_path}' created.")
        else:
            self.get_logger().info(f"Using existing base directory '{self.base_path}'.")

    def run_logger(self):
        # Get task name (subfolder within the base path)
        self.task_name = input("Enter the task name (this will be the output folder): ")
        task_folder = self.base_path / self.task_name
        
        # Create the task directory if it doesn't exist
        if not task_folder.exists():
            task_folder.mkdir(parents=True, exist_ok=True)
            self.get_logger().info(f"Directory '{task_folder}' created.")
        else:
            self.get_logger().info(f"Directory '{task_folder}' already exists.")
        
        # Confirm and start recording
        if input("Start recording? (y/n): ").strip().lower() == 'y':
            # folder inside the task folder
            task_folder_bag = task_folder / "rosbag2"
            self.start_recording(task_folder_bag)

            # Wait for user to stop recording
            input("Press Enter to stop recording...")
            self.stop_recording()

            # Ask to save or discard
            if input("Save recording? (y/n): ").strip().lower() == 'y':
                # Generate a unique name based on the current date and time
                h5_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".h5"
                h5_filepath = task_folder / h5_filename
                self.get_logger().info(f"Recording saved as '{h5_filename}' in folder '{task_folder}'")
                
                # Convert to HDF5 and delete the bag file afterward
                convert_to_h5(input_bag_path=str(task_folder_bag), output_h5_path=str(h5_filepath))
                self.get_logger().info(f"Recording converted to HDF5: {h5_filepath}")
                self.delete_recording(task_folder_bag)
            else:
                self.get_logger().info("Recording discarded.")
                self.delete_recording(task_folder_bag)

    def start_recording(self, task_folder_bag):
        if not self.topics_to_record:
            self.get_logger().error("No topics specified to record. Check the configuration file.")
            return

        # Set up rosbag2 writer
        storage_options = rosbag2_py.StorageOptions(uri=str(task_folder_bag), storage_id="sqlite3")
        converter_options = rosbag2_py.ConverterOptions(
            input_serialization_format="cdr", output_serialization_format="cdr"
        )

        self.writer = rosbag2_py.SequentialWriter()
        self.writer.open(storage_options, converter_options)

        # Add topics to be recorded
        self.subscribers = []
        for topic_name in self.topics_to_record:
            topic_type = topics_types.get(topic_name)
            if not topic_type:
                self.get_logger().error(f"Topic type for {topic_name} is not recognized.")
                continue
            
            # Create topic metadata for rosbag
            self.writer.create_topic(rosbag2_py.TopicMetadata(
                name=topic_name,
                type=topic_type.__name__,
                serialization_format="cdr"
            ))

            # Subscribe and add callback to write messages
            self.subscribers.append(
                self.create_subscription(
                    topic_type,
                    topic_name,
                    lambda msg, topic_name=topic_name: self.writer.write(
                        topic_name, serialize_message(msg), self.get_clock().now().nanoseconds
                    ),
                    10
                )
            )

        self.get_logger().info(f"Recording started for task '{self.task_name}' with topics: {[t for t in self.topics_to_record]}")

    def stop_recording(self):
        if self.writer:
            self.writer = None
            for sub in self.subscribers:
                self.destroy_subscription(sub)
            self.get_logger().info("Stopped recording.")
        else:
            self.get_logger().warn("No active recording to stop.")

    def delete_recording(self, task_folder_bag):
        # Delete all files in the task folder after converting
        for file in task_folder_bag.iterdir():
            file.unlink()
            
        # delete the folder
        task_folder_bag.rmdir()
        self.get_logger().info(f"Recording deleted from folder: {task_folder_bag}")

def main(args=None):
    # Define the base path for recordings
    base_path = "recordings"  # Modify this path as needed

    # Load topics to record (for demonstration, using hardcoded list)
    topics_to_record = ['/oakd_front_view/color', "/oakd_side_view/color", "/franka/end_effector_pose", '/hand/policy_output', "/sensor/bmp1/pressure"]

    # Initialize ROS and create DemoLogger instance
    rclpy.init(args=args)
    demo_logger = DemoLogger(topics_to_record, base_path)
    
    import threading
    threading.Thread(target=rclpy.spin, args=(demo_logger,)).start()
    
    while rclpy.ok():
        demo_logger.run_logger()
    demo_logger.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
