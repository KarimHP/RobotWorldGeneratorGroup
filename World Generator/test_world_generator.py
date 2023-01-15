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
    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)


def step(world_generator: WorldGenerator):
    for sensor in world_generator.sensors:
        sensor.step()

    for obstacle in world_generator.obstacles:
        obstacle.step()

    p.stepSimulation()
    time.sleep(1. / 100.)


if __name__ == "__main__":
    os.chdir(sys.path[0])

    init_pyb()
    generator = WorldGenerator()
    robot = generator.robot

    while 1:
        step(generator)
