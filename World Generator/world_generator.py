import pybullet as p
import pybullet_data
import os
import glob
import sys
import yaml
from sensors.lidar import LidarSensor

class WorldGenerator:
    sensors = []
    urdf_path = "urdfs"

    def load_config(self):
        with open("../config.yaml", "r") as stream:
            self.config = yaml.safe_load(stream)["world"]

    def init_pyb(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.planeID = p.loadURDF("plane.urdf")
        p.setGravity(0,0,-9.81)
        p.setRealTimeSimulation(0)

    def find_urdfs(self, search_folder):
        return list(glob.iglob(os.path.join(self.urdf_path, search_folder, "**/*.urdf"), recursive=True))

    def getPosition(self, obj):
        xyz = obj["position"]
        return [xyz["x"], xyz["y"], xyz["z"]]

    def getRotation(self, obj):
        rpy = obj["rotation"]
        return p.getQuaternionFromEuler([rpy["r"], rpy["p"], rpy["y"]])

    def load_robot(self):
        robot = self.config["robot"]
        robot_urdf = self.find_urdfs(robot["type"])[0]
        self.robot_id = p.loadURDF(robot_urdf, self.getPosition(robot), self.getRotation(robot))

    def load_obstacles(self):
        obstacles = self.config["obstacles"]
        for obstacle in obstacles:
            p.loadURDF(f"{obstacle['type']}.urdf", self.getPosition(obstacle), self.getRotation(obstacle))

    def load_sensors(self):
        sensors = self.config["robot"]["sensors"]
        for sensor in sensors:
            if sensor["type"] == "lidar":
                self.sensors.append(LidarSensor(self.robot_id, sensor["link"], self.getPosition(sensor), self.getRotation(sensor)))


    def update(self):
        p.stepSimulation()
        print(p.getBodyInfo(self.robot_id))
        for sensor in self.sensors:
            sensor.update()
            sensor._set_lidar_cylinder(render=True, ray_num_hor=1, ray_num_ver=1)


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
        

