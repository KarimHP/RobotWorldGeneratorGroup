import pybullet as p
import pybullet_data
import os
import glob
import sys
import yaml
import time
import math
from sensors.base import BaseSensor
from sensors.lidar import LidarSensor
from obstacles.base_obstacle import BaseObstacle
from obstacles.maze.maze_urdf import MazeUrdf
from obstacles.shelf.shelf_urdf import ShelfUrdf
from obstacles.urdf_object.static_object import StaticObject
from obstacles.urdf_object.moving_object import MovingObject
from obstacles.human.human_obstacle import HumanObstacle
from obstacles.human.human_obstacle_static import HumanObstacleStatic
from helpers.helpers import getPosition, getRotation, getScale, isMoving, getUrdfPath
from robot import Robot


class WorldGenerator:
    robot: Robot = None
    obstacles: list[BaseObstacle] = []
    sensors: list[BaseSensor] = []
    

    def load_config(self, config_path: str):
        with open(config_path, "r") as stream:
            self.config = yaml.safe_load(stream)["world"]


    def load_robot(self):
        robot = self.config["robot"]
        self.robot = Robot(getUrdfPath(robot["type"]), getPosition(robot), getRotation(robot))

    def load_obstacle(self, obstacle):
        obstacle_name = obstacle["type"]
        position = getPosition(obstacle)
        rotation = getRotation(obstacle)
        scale = getScale(obstacle)


        if obstacle_name == "human" and isMoving(obstacle):
            self.obstacles.append(HumanObstacle(position, rotation, scale, obstacle["params"]))
        elif obstacle_name == "human" and not isMoving(obstacle):
            self.obstacles.append(HumanObstacleStatic(position, rotation, scale))
        else:
            if obstacle_name == "maze":
                maze = MazeUrdf(obstacle["params"])
                urdf_name = maze.generate()
            elif obstacle_name == "shelf":
                shelf = ShelfUrdf(obstacle["params"])
                urdf_name = shelf.generate()
            else:
                urdf_name = getUrdfPath(obstacle_name)
                
            if not isMoving(obstacle):
                self.obstacles.append(StaticObject(urdf_name, position, rotation, scale))
            else:
                self.obstacles.append(MovingObject(urdf_name, position, rotation, scale, obstacle["params"]["move"]))

    def load_obstacles(self):
        obstacles = self.config["obstacles"]
        for obstacle in obstacles:
            self.load_obstacle(obstacle)

    def load_goals(self):
        goals = self.config["goals"]
        for goal in goals:
            if "indicator" in goal:
                StaticObject(getUrdfPath(goal["indicator"]), getPosition(goal), getRotation(goal), getScale(goal))


    def load_sensors(self):
        sensors = self.config["robot"]["sensors"]
        for sensor in sensors:
            params = sensor["params"]
            if sensor["type"] == "lidar":
                self.sensors.append(LidarSensor(self.robot.id, sensor["link"], getPosition(sensor), getRotation(sensor),
                                                params["ray_min"], params["ray_max"], params["ray_num_ver"],
                                                params["ray_num_hor"]))

    def __init__(self, config_path: str) -> None:
        self.load_config(config_path)
        self.load_robot()
        self.load_obstacles()
        self.load_sensors()
        self.load_goals()
