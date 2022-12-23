import yaml

if __name__ == '__main__':
    with open("data.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

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

    # For Schleife für link_list
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
            radius = str(link["radius"])
            shapes[shape] = "<sphere radius =\"" + radius + "\"/>"
        elif shape == "cylinder":
            radius = str(link["radius"])
            length = str(link["length"])
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
        xyz = str(link["xyz"])
        rpy = str(link["rpy"])
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

    joints = config["robot"]["joint_list"]

    for joint in joints:
        # Prompt user for joint name, type, and link names
        joint_name = joint["joint_name"]
        joint_type = joint["type"]
        link1 = joint["link1"]
        link2 = joint["link2"]
        origins = str.split(joint["origin"], " ")
        origin_xyz = ' '.join(map(str, origins[:3]))
        origin_rpy = ' '.join(map(str, origins[3:]))

        if joint_type == "revolute" or joint_type == "prismatic":
            axis = joint["axis"]
            limits = joint["limits"]
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
            axis = joint["axis"]
            joint_axis = f"<axis xyz=\"{axis}\"/>"
            joint_options = f"{joint_axis}\n"

        elif joint_type == "fixed":
            joint_options = f"<origin xyz=\"{origin_xyz}\" rpy=\"{origin_rpy}\"/>"

        elif joint_type == "floating":
            limits = joint["limits"]
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
            axis = joint["axis"]
            joint_axis = f"<axis xyz=\"{axis}\"/>"
            joint_options = f"{joint_origin}\n {joint_axis}\n"

        else:
            continue

        # Add joint to .urdf file
        urdf_file.write("<joint name=\"" + joint_name + "\" type=\"" + joint_type + "\">\n")
        urdf_file.write("<parent link=\"" + link1 + "\"/>\n" + "<child link=\"" + link2 + "\"/>\n")
        urdf_file.write(joint_options)

        urdf_file.write("</joint>\n")

    urdf_file.write("</robot>\n")
