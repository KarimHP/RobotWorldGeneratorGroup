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
from obstacles.base_obstacle import BaseObstacle
from obstacles.urdf_object.static_object import StaticObject
from obstacles.urdf_object.moving_object import MovingObject
from obstacles.human.human_obstacle import HumanObstacle
from obstacles.human.human_obstacle_static import HumanObstacleStatic
from helpers.helpers import getPosition, getRotation, getScale, getMoving, isMoving, getMovingSteps
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

    def load_robot(self):
        robot = self.config["robot"]
        self.robot = Robot(self.find_urdfs(robot["type"])[0], getPosition(robot), getRotation(robot))

    def load_obstacles(self):
        obstacles = self.config["obstacles"]
        for obstacle in obstacles:
            obstacle_name = obstacle["type"]
            if obstacle_name == "maze":
                params = obstacle["params"]
                maze = MazeObstacle(getPosition(obstacle), getRotation(obstacle), params)
                self.obstacles.append(maze)
            elif obstacle_name == "human":
                self.obstacles.append(HumanObstacle(getPosition(obstacle), getRotation(obstacle), obstacle["params"],
                                                    scale=getScale(obstacle)))
            elif obstacle_name == "human_static":
                self.obstacles.append(
                    HumanObstacleStatic(getPosition(obstacle), getRotation(obstacle),
                                        scale=getScale(obstacle)))
            else:
                predefined_urdfs = self.find_urdfs(obstacle_name)
                if len(predefined_urdfs) > 0:
                    urdf_name = predefined_urdfs[0]
                else:
                    urdf_name = f"{obstacle_name}.urdf"
                if not isMoving(obstacle):
                    self.obstacles.append(
                        StaticObject(urdf_name, getPosition(obstacle), getRotation(obstacle), getScale(obstacle)))
                else:
                    self.obstacles.append(MovingObject(urdf_name, getPosition(obstacle), getRotation(obstacle),
                                                       *getMoving(obstacle), getMovingSteps(obstacle), getScale(obstacle)))

    def load_sensors(self):
        sensors = self.config["robot"]["sensors"]
        for sensor in sensors:
            params = sensor["params"]
            if sensor["type"] == "lidar":
                self.sensors.append(LidarSensor(self.robot.id, sensor["link"], getPosition(sensor), getRotation(sensor),
                                                params["ray_min"], params["ray_max"], params["ray_num_ver"],
                                                params["ray_num_hor"]))

    def __init__(self) -> None:
        self.load_config()
        self.load_robot()
        self.load_obstacles()
        self.load_sensors()
