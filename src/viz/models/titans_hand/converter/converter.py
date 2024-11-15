from mjcf_urdf_simple_converter import convert

# or, if you are using it in your ROS package and would like for the mesh directories to be resolved correctly, set meshfile_prefix, for example:
convert("/home/matteo/rwr_system/RWR-TactileTitans/MuJoCo/XMLfiles/simulation.xml", "model.urdf", asset_file_prefix="package://your_package_name/model/")