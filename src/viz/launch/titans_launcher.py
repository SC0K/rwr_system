import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Path to the URDF file
    urdf = os.path.join(
        get_package_share_directory('viz'),
        "models",
        "titans_hand",
        "model.urdf"
    )

    # Load the URDF content
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # Robot State Publisher Node
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]  # Correct way to pass URDF
        ),
        # RViz Node
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            # Optional: You can pre-load a specific RViz configuration file
            # arguments=['-d', '<path_to_rviz_config_file>']
        ),
    ])
