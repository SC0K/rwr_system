import rclpy
import rclpy.logging
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from dynamixel_client import *
from threading import RLock
import time

# Dynamixel Constants
DXL_IDS = [0, 1, 3, 11, 12]  # IDs of the 5 Dynamixel motors
BAUDRATE = 57600
DEVICENAME = "/dev/ttyUSB0"
CURRENT_LIMIT = 100  # Max current/torque limit for each motor

class DynamixelController(Node):
    def __init__(self):
        super().__init__('dynamixel_controller')

        self.motor_ids = DXL_IDS
        self.motor_lock = RLock()  # lock to read / write motor information

        # initialize and connect dynamixels
        self._dxc = DynamixelClient(self.motor_ids, DEVICENAME, BAUDRATE)
        self.connect_to_dynamixels()

        self.set_operating_mode(0)  # Set the operating mode to 0 (current control)

        # Subscribe to the pressure_data topic to control the motors
        self.create_subscription(Float32MultiArray, 'pressure_data', self.pressure_callback, 10)

    def terminate(self):
        '''
        disable torque and disconnect from dynamixels
        '''
        self.disable_torque()
        time.sleep(0.1)  # wait for disabling torque
        self.disconnect_from_dynamixels()

    def connect_to_dynamixels(self):
        with self.motor_lock:
            self._dxc.connect()
            
    def disconnect_from_dynamixels(self):
        with self.motor_lock:
            self._dxc.disconnect()

    def set_operating_mode(self, mode):
        """
        see dynamixel_client.py for the meaning of the mode
        """
        with self.motor_lock:
            self._dxc.set_operating_mode(self.motor_ids, mode)

    def enable_torque(self, motor_ids=None):
        if motor_ids is None:
            motor_ids = self.motor_ids
        with self.motor_lock:
            self._dxc.set_torque_enabled(motor_ids, True)

    def disable_torque(self, motor_ids=None):
        if motor_ids is None:
            motor_ids = self.motor_ids
        with self.motor_lock:
            self._dxc.set_torque_enabled(motor_ids, False)

    def pressure_callback(self, msg: Float32MultiArray):
        """
        Callback to process the incoming pressure data and control the motors.
        Each pressure value controls one motor.
        """
        if len(msg.data) != 5:
            self.get_logger().error("Pressure data array must have exactly 5 elements!")
            return
        
        max_pressure = 60000
        current_offset = 10.0  # Offset for the current calculation
        pressures = np.array(msg.data)
        pressures = np.clip(pressures, 0, max_pressure)  # Clip pressures to a maximum value
        
        currents = (CURRENT_LIMIT-current_offset)/max_pressure  * pressures # Or apply your scaling here

        currents = np.clip(currents + current_offset, current_offset, CURRENT_LIMIT)

        self.set_motor_current(self.motor_ids, currents)

    def set_motor_current(self, motor_ids, current):
        """
        Set the current for a specific motor.
        """

        with self.motor_lock:
            self._dxc.write_desired_current(motor_ids, current)


def main(args=None):
    rclpy.init(args=args)
    node = DynamixelController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up
        node.terminate()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
