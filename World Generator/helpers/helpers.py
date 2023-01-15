import pybullet as p
import math
import glob
import os
import sys

URDF_PATH = "../urdfs/"

def getPosition(obj):
    xyz = obj["position"]
    return [xyz["x"], xyz["y"], xyz["z"]]


def getRotation(obj):
    conversion_fac = math.pi / 180
    rpy = obj["rotation"]
    return p.getQuaternionFromEuler([rpy["r"] * conversion_fac, rpy["p"] * conversion_fac, rpy["y"] * conversion_fac])


def getScale(obj):
    if "scale" in obj:
        scale = obj["scale"]
    else:
        scale = 1
    return scale

def findUrdfs(search_name):
    return list(glob.iglob(os.path.join(URDF_PATH, f"**/{search_name}.urdf"), recursive=True))

def getUrdfPath(name):
    predefined_urdfs = findUrdfs(name)

    if len(predefined_urdfs) > 0:
        urdf_name = predefined_urdfs[0]
    else:
        urdf_name = f"{name}.urdf"
    return urdf_name
    

def isMoving(obj):
    return "params" in obj and "move" in obj["params"]


def getMoving(obj):
    if "moving" in obj:
        start_pos = obj["start_pos"]
        end_pos = obj["end_pos"]
        return [start_pos["x"], start_pos["y"], start_pos["z"]], [end_pos["x"], end_pos["y"], end_pos["z"]]

def getMovingSteps(obj):
    if "steps" in obj:
        return obj["steps"]
    else:
        return 100
