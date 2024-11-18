from mjcf_urdf_simple_converter import convert

# or, if you are using it in your ROS package and would like for the mesh directories to be resolved correctly, set meshfile_prefix, for example:
convert("/home/sitong/RWR_ros2_ws/src/rwr_system/src/viz/models/titans_hand/hand_titans.xml", "model.urdf")