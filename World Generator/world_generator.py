import pybullet as p
import pybullet_data
import os
import glob
import sys
import yaml
import time
import math
from obstacles.maze.maze_obstacle import MazeObstacle
from sensors.base import BaseSensor
from sensors.lidar import LidarSensor
from obstacles.base import BaseObstacle
from obstacles.static_object import StaticObject
from obstacles.moving_object import MovingObject
from robot import Robot

URDF_PATH = "../urdfs/"

class WorldGenerator:
    robot: Robot = None
    obstacles: list[BaseObstacle] = []
    sensors: list[BaseSensor] = []

    def load_config(self):
        with open("../config.yaml", "r") as stream:
            self.config = yaml.safe_load(stream)["world"]

    def find_urdfs(self, search_name):
        return list(glob.iglob(os.path.join(URDF_PATH, f"**/{search_name}.urdf"), recursive=True))

    def getPosition(self, obj):
        xyz = obj["position"]
        return [xyz["x"], xyz["y"], xyz["z"]]

    def getRotation(self, obj):
        conversion_fac = math.pi / 180
        rpy = obj["rotation"]
        print([rpy["r"] * conversion_fac, rpy["p"] * conversion_fac, rpy["y"] * conversion_fac])
        return p.getQuaternionFromEuler([rpy["r"] * conversion_fac, rpy["p"] * conversion_fac, rpy["y"] * conversion_fac])

    def load_robot(self):
        robot = self.config["robot"]
        self.robot = Robot(self.find_urdfs(robot["type"])[0], self.getPosition(robot), self.getRotation(robot))

    def load_obstacles(self):
        obstacles = self.config["obstacles"]
        for obstacle in obstacles:
            if obstacle["type"] == "maze":
                params = obstacle["params"]
                maze = MazeObstacle(self.getPosition(obstacle), self.getRotation(obstacle), params)
                self.obstacles.append(maze)
            else:
                self.obstacles.append(StaticObject(f"{obstacle['type']}.urdf", self.getPosition(obstacle), self.getRotation(obstacle)))

    def load_sensors(self):
        sensors = self.config["robot"]["sensors"]
        for sensor in sensors:
            params = sensor["params"]
            if sensor["type"] == "lidar":
                self.sensors.append(LidarSensor(self.robot.id, sensor["link"], self.getPosition(sensor), self.getRotation(sensor), params["ray_min"], params["ray_max"], params["ray_num_ver"], params["ray_num_hor"]))



    def __init__(self) -> None:
        self.load_config()
        self.load_robot()
        self.load_obstacles()
        self.load_sensors()



