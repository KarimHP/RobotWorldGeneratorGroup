from world_generator import WorldGenerator
import pybullet as p
import pybullet_data
import time
import os
import sys
import argparse

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

    parser = argparse.ArgumentParser(description='World Generator run script for testing')

    parser.add_argument('config', type=str, nargs='?', default="config",
                    help='A required integer positional argument')

    args = parser.parse_args()

    init_pyb()
    generator = WorldGenerator(os.path.join("../configs", f"{args.config}.yaml"))
    robot = generator.robot

    while 1:
        step(generator)
