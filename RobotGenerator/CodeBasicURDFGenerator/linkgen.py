# Import required modules
import sys
import yaml

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

# Open the config.yaml file
with open("RobotGenerator/CodeBasicURDFGenerator/data.yaml", "r") as stream:
    # Load the yaml file into a dictionary
    config = yaml.safe_load(stream)

robot_name = config["robot"]["robot_name"]

# Create  .urdf file
urdf_file = open(robot_name + ".urdf", "w")

# Write header information for the .urdf file
urdf_file.write("<?xml version=\"1.0\"?>\n")
urdf_file.write("<robot name=\"" + robot_name + "\">\n")

# Add a color counter so that we later know which link is which color
colorcounter = 0

# Get linklist from config
links = config["robot"]["link_list"]

#For Schleife für link_list
for link in links:
    link_name = link["link_name"]
    shape = link["link_shape"]

    # Check if shape is valid
    if shape not in shapes:
        print("Invalid shape. Please try again.")
        continue

    # depending if its a box, a cylinder or a sphere enter size/radius,length/radius
    if shape == "box":
        size = str(link["size"])
        shapes[shape] = "<box size =\"" + size + "\"/>"
    elif shape == "sphere":
        radius = link["radius"]
        shapes[shape] = "<sphere radius =\"" + radius + "\"/>"
    elif shape == "cylinder":
        radius = link["radius"]
        length = link["length"]
        shapes[shape] = "<cylinder radius =" + "'" + radius + "' " + " length=" + "'" + length + "'" "/>"

    # Prompt user for link color
    color = link["link_color"]
    rgba = color_map.get(color)
    if rgba is None:
        print("Invalid color")
        continue

    # Add the rgba value to the colors array
    colors.append(rgba)
    

    # Prompt user for xyz and rpy
    xyz = link["xyz"]
    rpy = link["rpy"]
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

  
    colorcounter = colorcounter + 1
        
