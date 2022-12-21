import yaml

if __name__ == '__main__':
    with open("data.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    robot_name = config["robot"]["robot_name"]

    # Create  .urdf file
    urdf_file = open(robot_name + ".urdf", "w")

    # Write header information for the .urdf file
    urdf_file.write("<?xml version=\"1.0\"?>\n")
    urdf_file.write("<robot name=\"" + robot_name + "\">\n")

    joints = config["robot"]["joint_list"]

    for joint in joints:
        # Prompt user for joint name, type, and link names
        joint_name = joint["joint_name"]
        joint_type = joint["type"]
        link1 = joint["link1"]
        link2 = joint["link2"]
        origin = joint["origin"]
        origin_xyz = origin[:len(origin) // 2]
        origin_rpy = origin[len(origin) // 2:]

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
