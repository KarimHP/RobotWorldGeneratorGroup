# Import required modules
import sys

# some basic shapes
shapes = {
    "box": "<box size='1 1 1'/>",
    "sphere": "<sphere radius='0.5'/>",
    "cylinder": "<cylinder radius='0.5' length='1'/>"
}

# Define the colors Array and the Color_map which appends the correct rgba code to the given color
colors = []
color_map = {
    "red": "1 0 0 1",
    "green": "0 1 0 1",
    "blue": "0 0 1 1",
    "white": "1 1 1 1",
    "black": "0 0 0 1"
}

# standard origins
origins = "<origin rpy = '0 0 0' xyz = '0 0 0'/>"

# Prompt user for robot name
robot_name = input("Enter robot name: ")

# Create  .urdf file
urdf_file = open(robot_name + ".urdf", "w")

# Write header information for the .urdf file
urdf_file.write("<?xml version=\"1.0\"?>\n")
urdf_file.write("<robot name=\"" + robot_name + "\">\n")

# Add a color counter so that we later know which link is which color
colorcounter = 0

# Loop until user is finished adding links
while True:

    # Prompt user for link name and shape
    link_name = input("Enter link name: ")
    shape = input("Enter shape (box, sphere, cylinder): ")

    # Check if shape is valid
    if shape not in shapes:
        print("Invalid shape. Please try again.")
        continue

    # depending if its a box, a cylinder or a sphere enter size/radius,length/radius
    if shape == "box":
        size = input("Enter the size of the box (eg: 1 1 1): ")
        shapes[shape] = "<box size =\"" + size + "\"/>"
    elif shape == "sphere":
        radius = input("Enter the radius of the sphere (eg: 0.5): ")
        shapes[shape] = "<sphere radius =\"" + radius + "\"/>"
    elif shape == "cylinder":
        radius = input("Enter the radius of the cylinder: ")
        length = input("Enter the length of the cylinder: ")
        shapes[shape] = "<cylinder radius =" + "'" + radius + "' " + " length=" + "'" + length + "'" "/>"

    # Prompt user for link color
    color = input("Enter color (e.g 'red' or 'blue'): ")
    rgba = color_map.get(color)
    if rgba is None:
        print("Invalid color")
        continue

    # Add the rgba value to the colors array
    colors.append(rgba)
    

    # Prompt user for xyz and rpy
    xyz = input("Enter the xyz data (eg: 0 0 0.5): ")
    rpy = input("Enter the rpy data (eg: 0 0 0): ")
    origins = "<origin rpy =" + "'" + rpy + "' " + "xyz=" + "'" + xyz + "'" + "/>"

    # Add the material section to the .urdf file 
    urdf_file.write("<material name =" + "'" + color + "'" + ">\n")
    urdf_file.write("   <color rgba=" + "'" + colors[colorcounter] + "'" + "/>\n")
    urdf_file.write("</material>\n")

    # Add link to .urdf file
    urdf_file.write("\n")
    urdf_file.write("<link name=\"" + link_name + "\">\n")
    urdf_file.write("<visual>\n")
    urdf_file.write("<geometry>\n")
    urdf_file.write(shapes[shape] + "\n")
    urdf_file.write("</geometry>\n")
    urdf_file.write(origins + "\n")
    urdf_file.write("<material name =" + "'" + color + "'" + "/>")
    urdf_file.write("</visual>\n")
    urdf_file.write("</link>\n")
    urdf_file.write("\n")

    # Prompt user to add another link
    add_link = input("Add another link? (y/n) ")
    if add_link.lower() != "y":
        break
    else:
        colorcounter = colorcounter + 1
        

while True:
    # Check if user wants to add a joint between the links
    add_joint = input("Add a joint between the links? (y/n) ")
    if add_joint.lower() == "y":
        # Prompt user for joint name, type, and link names
        joint_name = input("Enter joint name: ")
        joint_type = input("Enter joint type (e.g. revolute): ")
        link1 = input("Enter first link name: ")
        link2 = input("Enter second link name: ")
        origin_xyz = "0 0 0"
        origin_rpy = "0 0 0"
        axis = "1 0 0"

        origin_xyz = input("Enter origin xyz (default: 0 0 0): ") or origin_xyz
        origin_rpy = input("Enter origin rpy (default: 0 0 0): ") or origin_rpy

        if joint_type == "revolute" or joint_type == "prismatic":
            axis = input("Enter rotation axis (default: 1 0 0): ") or axis
            limits = input("Enter limits (lower, upper, effort, velocity): ") or "0 0 1 1"
            limits_list = str.split(limits, " ")
            limit_lower = limits_list[0]
            limit_upper = limits_list[1]
            limit_effort = limits_list[2]
            limit_velocity = limits_list[3]
            joint_origin = f"<origin xyz=\"{origin_xyz}\" rpy=\"{origin_rpy}\"/>"
            joint_axis = f"<axis xyz=\"{axis}\"/>"
            joint_limit = f"<limit lower=\"{limit_lower}\" upper=\"{limit_upper}\" effort=\"{limit_effort}\" " \
                          f"velocity=\"{limit_velocity}\"/>"
            joint_options = f"{joint_origin}\n {joint_axis}\n {joint_limit}\n"
        elif joint_type == "continuous":
            axis = input("Enter rotation axis (default: 1 0 0): ") or axis
            joint_axis = f"<axis xyz=\"{axis}\"/>"
            joint_options = f"{joint_axis}\n"
        elif joint_type == "fixed":
            joint_options = f"<origin xyz=\"{origin_xyz}\" rpy=\"{origin_rpy}\"/>"
        elif joint_type == "floating":
            limits = input("Enter limits (lower, upper, effort, velocity): ") or "0 0 1 1"
            limits_list = str.split(limits, " ")
            limit_lower = limits_list[0]
            limit_upper = limits_list[1]
            limit_effort = limits_list[2]
            limit_velocity = limits_list[3]
            joint_origin = f"<origin xyz=\"{origin_xyz}\" rpy=\"{origin_rpy}\"/>"
            joint_limit = f"<limit lower=\"{limit_lower}\" upper=\"{limit_upper}\" effort=\"{limit_effort}\" " \
                          f"velocity=\"{limit_velocity}\"/>"
            joint_options = f"{joint_origin}\n {joint_limit}\n"
        elif joint_type == "planar":
            joint_origin = f"<origin xyz=\"{origin_xyz}\" rpy=\"{origin_rpy}\"/>"
            axis = input("Enter surface normal (default: 1 0 0): ") or axis
            joint_axis = f"<axis xyz=\"{axis}\"/>"
            joint_options = f"{joint_origin}\n {joint_axis}\n"

        else:
            continue

        # Add joint to .urdf file
        urdf_file.write("<joint name=\"" + joint_name + "\" type=\"" + joint_type + "\">\n")
        urdf_file.write("<parent link=\"" + link1 + "\"/>\n" + "<child link=\"" + link2 + "\"/>\n")
        urdf_file.write(joint_options)

        urdf_file.write("</joint>\n")
    else:
        break
# write the closing tag for the <robot>
urdf_file.write("</robot>\n")

# TODO: Add xml validator
