import pybullet as p
import pybullet_data

# Connect to the PyBullet simulator
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
# Set the gravity
p.setGravity(0, 0, -9.81)
planeID = p.loadURDF("plane.urdf")
# Load the URDF file
urdf_id = p.loadURDF("World Generator\\urdfs\\kuka_kr3_support\\urdf\\kr3r540.urdf", [0, 0, 0], [0, 0, 0, 1],
                     useFixedBase=True)

# Set the flag to stop the simulation
stop_simulation = False

# Get the number of joints in the robot
num_joints = p.getNumJoints(urdf_id)

# Create a list to store the joint angles
joint_angles = []

# Create a slider for each joint
for i in range(num_joints):
    # Get the joint information
    joint_info = p.getJointInfo(urdf_id, i)
    # Get the joint name and limits
    joint_name = joint_info[1].decode('utf-8')
    joint_min = joint_info[8]
    joint_max = joint_info[9]
    # Create a slider for the joint
    joint_angle = p.addUserDebugParameter(joint_name, joint_min, joint_max, 0)
    # Add the joint angle to the list
    joint_angles.append(joint_angle)

# Run the simulation
while not stop_simulation:
    # Step the simulation
    p.stepSimulation()
    # Get the current joint angles
    for i in range(num_joints):
        joint_angle = p.readUserDebugParameter(joint_angles[i])
        # Set the joint angle
        p.setJointMotorControl2(urdf_id, i, p.POSITION_CONTROL, joint_angle)


# Disconnect from the PyBullet simulator
p.disconnect()
