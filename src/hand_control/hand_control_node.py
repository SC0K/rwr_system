#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import numpy as np
from std_msgs.msg import Float32MultiArray
import os
from gripper_controller import GripperController


class HandControllerNode(Node):
    def __init__(self, debug=True):
        super().__init__("hand_controller_node")

        # start tracker
        self.declare_parameter("hand_controller/port", "/dev/ttyUSB0")
        self.declare_parameter("hand_controller/baudrate", 3000000)

        port = self.get_parameter("hand_controller/port").value
        baudrate = self.get_parameter("hand_controller/baudrate").value

        print(f"Initializing GripperController with port: {port}, baudrate: {baudrate}")
        try:
            self._hc = GripperController(port=port)
            self._hc.init_joints(calibrate=False)
            print("GripperController initialized successfully")
        except Exception as e:
            print(f"Failed to initialize GripperController: {e}")
            self.get_logger().error(f"Failed to initialize GripperController: {e}")
            rclpy.shutdown()
            return

        self.joint_angle_sub = self.create_subscription(
            Float32MultiArray, "/hand/policy_output", self.joint_angle_cb, 10
        )
        print("Subscription created for /hand/policy_output")

    def joint_angle_cb(self, msg):
        try:
            assert len(msg.data) == 17, "Expected 17 joint angles, got {}".format(
                len(msg.data)
            )
            print("Received joint angles")
            joint_angles = np.array(msg.data)
            joint_angles_deg = joint_angles * 180 / np.pi
            self._hc.write_desired_joint_angles(joint_angles_deg)
            print("Joint angles written to GripperController")
        except Exception as e:
            print(f"Failed to process joint angles: {e}")
            self.get_logger().error(f"Failed to process joint angles: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = HandControllerNode()

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()