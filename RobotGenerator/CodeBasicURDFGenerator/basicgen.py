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
    "red": "1 0 0",
    "green": "0 1 0",
    "blue": "0 0 1",
    "white": "1 1 1",
    "black": "0 0 0"
}

#standard origins
origins = "<origin rpy = '0 0 0' xyz = '0 0 0'/>"

# Prompt user for robot name
robot_name = input("Enter robot name: ")

# Create  .urdf file
urdf_file = open(robot_name + ".urdf", "w")

# Write header information for the .urdf file
urdf_file.write("<?xml version=\"1.0\"?>\n")
urdf_file.write("<robot name=\"" + robot_name + "\">\n")


 # Add a color counter so that we later know which link is which color
colorcounter = 0; 

# Loop until user is finished adding links
while True:

   

    # Prompt user for link name and shape
    link_name = input("Enter link name: ")
    shape = input("Enter shape (box, sphere, cylinder): ")

    # Check if shape is valid
    if shape not in shapes:
        print("Invalid shape. Please try again.")
        continue

    #depending if its a box, a cylinder or a sphere enter size/radius,length/radius
    if shape == "box":
        size = input("Enter the size of the box (eg: 1 1 1): ")
        shapes[shape] = "<box size =\"" + size + "\"/>"
    elif shape == "sphere":
        radius = input("Enter the radius of the sphere (eg: 0.5): ")
        shapes[shape] = "<sphere radius =\"" + radius + "\"/>"
    elif shape == "cylinder":
        radius = input("Enter the radius of the cylinder: ")
        length = input("Enter the length of the cylinder: ")
        shapes[shape] = "<cylinder radius =" + "'" + radius + "' "+" length=" + "'" + length + "'" "/>"


    # Prompt user for link color
    color = input("Enter color (e.g 'red' or 'blue'): ")
    rgba = color_map.get(color)
    if rgba is None:
        print("Invalid color")
        continue

    
    # Add the rgba value to the colors array
    colors.append(rgba)
    print (colors[colorcounter])

    # Prompt user for xyz and rpy
    xyz = input("Enter the xyz data (eg: 0 0 0.5): ")
    rpy = input("Enter the rpy data (eg: 0 0 0): ")
    origins = "<origin rpy =" + "'" + rpy + "' "+ "xyz=" + "'" + xyz + "'" + "/>"

    # Add the material section to the .urdf file 
    urdf_file.write("<material name =" + "'" + color +"'" + ">")
    urdf_file.write("   <color rgba=" + "'" + colors[colorcounter] + "'" + "/>")
    urdf_file.write("</material>")

    # Add link to .urdf file
    urdf_file.write("<link name=\"" + link_name + "\">\n")
    urdf_file.write("<visual>\n")
    urdf_file.write("<geometry>\n")
    urdf_file.write(shapes[shape] + "\n")
    urdf_file.write("</geometry>\n")
    urdf_file.write(origins + "\n")
    urdf_file.write("<material name =" + "'" + color + "'" + "/>")
    urdf_file.write("</visual>\n")
    urdf_file.write("</link>\n")

    # Prompt user to add another link
    add_link = input("Add another link? (y/n) ")
    if add_link.lower() != "y":
        break
    else: 
        colorcounter = colorcounter + 1 
        print(colorcounter)
        

# Check if user wants to add a joint between the links
add_joint = input("Add a joint between the links? (y/n) ")
if add_joint.lower() == "y":
    # Prompt user for joint name, type, and link names
    joint_name = input("Enter joint name: ")
    joint_type = input("Enter joint type (e.g. revolute): ")
    link1 = input("Enter first link name: ")
    link2 = input("Enter second link name: ")

    # Add joint to .urdf file
    urdf_file.write("<joint name=\"" + joint_name + "\" type=\"" + joint_type + "\">\n")
    #TODO: Add links to joint

#write the closing tag for the <robot>
urdf_file.write(" </robot>\n")


#TODO: Add xml validator