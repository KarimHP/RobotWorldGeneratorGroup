import pybullet as p
import pybullet_data
import os
import glob
import sys
import yaml
import time
import math
from obstacles.maze_obstacle import MazeObstacle
from sensors.lidar import LidarSensor

class WorldGenerator:
    sensors = []
    urdf_path = "../urdfs/"

    def load_config(self):
        with open("../config.yaml", "r") as stream:
            self.config = yaml.safe_load(stream)["world"]

    def init_pyb(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.planeID = p.loadURDF("plane.urdf")
        p.setGravity(0,0,-9.81)
        p.setRealTimeSimulation(0)

    def find_urdfs(self, search_name):
        return list(glob.iglob(os.path.join(self.urdf_path, f"**/{search_name}.urdf"), recursive=True))

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
        robot_urdf = self.find_urdfs(robot["type"])[0]
        self.robot_id = p.loadURDF(robot_urdf, self.getPosition(robot), self.getRotation(robot), useFixedBase=True)

    def load_obstacles(self):
        obstacles = self.config["obstacles"]
        for obstacle in obstacles:
            if obstacle["type"] == "maze":
                params = obstacle["params"]
                maze = MazeObstacle()
                maze.generate(self.getPosition(obstacle), self.getRotation(obstacle), params)
            else:
                p.loadURDF(f"{obstacle['type']}.urdf", self.getPosition(obstacle), self.getRotation(obstacle))

    def load_sensors(self):
        sensors = self.config["robot"]["sensors"]
        for sensor in sensors:
            params = sensor["params"]
            if sensor["type"] == "lidar":
                self.sensors.append(LidarSensor(self.robot_id, sensor["link"], self.getPosition(sensor), self.getRotation(sensor), params["ray_min"], params["ray_max"], params["ray_num_ver"], params["ray_num_hor"]))


    def update(self):
        for sensor in self.sensors:
            sensor.update()
        p.stepSimulation()
        time.sleep(1./10.)


    def __init__(self) -> None:
        self.load_config()
        self.init_pyb()
        self.load_robot()
        self.load_obstacles()
        self.load_sensors()

if __name__ == "__main__":
    os.chdir(sys.path[0])
    generator = WorldGenerator()
    

    while 1:
        generator.update()
        

