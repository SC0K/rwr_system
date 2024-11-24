import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import mujoco_py

class MujocoJointPublisher(Node):
    def __init__(self):
        super().__init__('mujoco_joint_publisher')
        self.publisher = self.create_publisher(JointState, 'joint_states', 17)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        # Initialize MuJoCo simulation
        self.model = mujoco_py.load_model_from_path('://package/viz/models/titans_hand/new_mujoco/hand_titans_new.xml')
        self.sim = mujoco_py.MjSim(self.model)

    def timer_callback(self):
        # Get the joint positions from the MuJoCo simulation
        joint_positions = self.sim.data.qpos.tolist()  # Joint positions (qpos)
        joint_velocities = self.sim.data.qvel.tolist()  # Joint velocities (qvel)
        
        # Create a JointState message to publish
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        #joint_state_msg.name = ["joint_1", "joint_2", "join_3" ]  # Replace with your joint names
        joint_state_msg.position = joint_positions
        joint_state_msg.velocity = joint_velocities

        # Publish the joint states
        self.publisher.publish(joint_state_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MujocoJointPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
