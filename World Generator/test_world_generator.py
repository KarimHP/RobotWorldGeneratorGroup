from world_generator import WorldGenerator
import pybullet as p
import pybullet_data
import time
import os
import sys


def init_pyb():
    physicsClient = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    planeID = p.loadURDF("plane.urdf")
    p.setGravity(0,0,-9.81)
    p.setRealTimeSimulation(0)

def update(world_generator):
    for sensor in world_generator.sensors:
        sensor.update()
    p.stepSimulation()
    time.sleep(1./10.)

if __name__ == "__main__":
    os.chdir(sys.path[0])

    init_pyb()
    generator = WorldGenerator()

    while 1:
        update(generator)
        