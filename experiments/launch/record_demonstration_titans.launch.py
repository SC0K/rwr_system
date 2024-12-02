from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

# select the cameras to be used

cameras = {"front_view": True, "side_view": True, "wrist_view": True}


def generate_launch_description():
    return LaunchDescription(
        [
            # CAMERA INGRESS NODE
            Node(
                package="ingress",
                executable="oakd_node.py",
                name="oakd_node",
                output="log",
                parameters=[
                    {"enable_front_camera": cameras["front_view"]},
                    {"enable_side_camera": cameras["side_view"]},
                    {"enable_wrist_camera": cameras["wrist_view"]},
                ],
            ),
            
            Node(
                package="ingress",
                executable="rokoko_node.py",
                name="rokoko_node",
                output="log",
                parameters=[
                    {"rokoko_tracker/ip": "0.0.0.0"},
                    {"rokoko_tracker/port": 14043}, # change this to 14044 if you say the port is already in use
                    {"rokoko_tracker/use_coil": True}
                ],
            ),

            # HAND CONTROLLER NODE
            Node(
                package="hand_control",
                executable="hand_controller_node.py",
                name="hand_control_node",
                output="screen"
            ),
            
            # RETARGET NODE
            Node(
                package="retargeter",
                executable="retargeter_node_titans.py",
                name="retargeter_node",
                output="screen",
                # COMMENT OR UNCOMMENT THE FOLLOWING LINES TO SWITCH BETWEEN MJCF AND URDF, JUST ONE OF THEM SHOULD BE ACTIVE TODO: Make this a parameter
                parameters=[
                    {
                        "retarget/mjcf_filepath": os.path.join(
                            get_package_share_directory("viz"),
                            "models",
                            "titans_hand",
                            "new_mujoco",
                            "hand_titans_new.xml"
                        ),
                        "retarget/hand_scheme": os.path.join(
                            get_package_share_directory("viz"),
                            "models",
                            "titans_hand",
                            "new_mujoco",
                            "scheme_titans.yaml",
                        ),
                        "retarget/mano_adjustments": os.path.join( # do we need this?
                            get_package_share_directory("experiments"),
                            "cfgs",
                            "retargeter_adjustment_titans.yaml"
                        ),
                        "retarget/retargeter_cfg": os.path.join( #do we need this? 
                            get_package_share_directory("experiments"),
                            "cfgs",
                            "retargeter_cfgs_titans.yaml"
                        ),
                    },
                    {"debug": True},
                ],
            ),
            
            # VISUALIZATION NODE
            Node(
                package="viz",
                executable="visualize_joints.py",
                name="visualize_joints",
                parameters=[
                    {
                        "scheme_path": os.path.join(
                            get_package_share_directory("viz"),
                            "models",
                            "titans_hand",
                            "new_mujoco",
                            "scheme_titans.yaml",
                        )
                    }
                ],
                output="screen",
            ),
        ]
    )
