import mujoco
from mujoco.viewer import launch
import numpy as np
import time
from threading import Thread

# Path to your model file
model_path = "../../viz/models/titans_hand/hand_titans.xml"

# Load the model and data
model = mujoco.MjModel.from_xml_path(model_path)
data = mujoco.MjData(model)

# Define the joint names
joint_names = [
    "revolute_base_hand",
    "revolute_thumb",
    "revolute_proximal_thumb",
    "revolute_medial_thumb",
    "revolute_distal_thumb",
    "revolute_joint_1",
    "revolute_proximal_1",
    "revolute_medial_1",
    "revolute_joint_2",
    "revolute_proximal_2",
    "revolute_medial_2",
    "revolute_joint_3",
    "revolute_proximal_3",
    "revolute_medial_3",
    "revolute_joint_4",
    "revolute_proximal_4",
    "revolute_medial_4"
]

# Get the joint IDs by name
joint_ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, name) for name in joint_names]

# Function to rotate the joints back and forth
def simulate(model, data, joint_ids, amplitude, frequency, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        # Calculate the desired joint positions using a sine wave
        elapsed_time = time.time() - start_time
        desired_positions = amplitude * np.sin(np.pi/2 * frequency * elapsed_time)
        
        # Set the joint positions
        for i, joint_id in enumerate(joint_ids):
            data.ctrl[i] = desired_positions
        
        # Step the simulation
        mujoco.mj_step(model, data)
        
        # Optional: Add a small sleep to control the update rate
        time.sleep(0.01)

# Launch the interactive viewer in a separate thread
viewer_thread = Thread(target=launch, args=(model, data))
viewer_thread.start()

# Rotate the joints back and forth for 10 seconds
simulate(model, data, joint_ids, amplitude=0.5, frequency=0.5, duration=10)

# Stop the viewer after the rotation
viewer_thread.join()