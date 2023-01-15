import pybullet as p
import math


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


def isMoving(obj):
    return "moving" in obj


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
