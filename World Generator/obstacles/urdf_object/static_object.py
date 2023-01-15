import pybullet as p
from ..base_obstacle import BaseObstacle

class StaticObject(BaseObstacle):

    def __init__(self, urdf, position, rotation, scale=1) -> None:
        super().__init__()
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.id = p.loadURDF(urdf, position, rotation, useFixedBase=True, globalScaling=scale)

    def step(self):
        pass