import sys
if sys.prefix == '/home/sitong/Virtual_environments/RWR_ros_venv':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sitong/RWR_ros2_ws/src/rwr_system/install/pressure_sub'
