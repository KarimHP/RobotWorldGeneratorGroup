import pybullet as p
import math

def getPosition(obj):
        xyz = obj["position"]
        return [xyz["x"], xyz["y"], xyz["z"]]

def getRotation(obj):
    conversion_fac = math.pi / 180
    rpy = obj["rotation"]
    return p.getQuaternionFromEuler([rpy["r"] * conversion_fac, rpy["p"] * conversion_fac, rpy["y"] * conversion_fac])