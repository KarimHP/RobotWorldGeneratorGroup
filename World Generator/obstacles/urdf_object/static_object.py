import pybullet as p
from ..base_obstacle import BaseObstacle

class StaticObject(BaseObstacle):

    def __init__(self, urdf, position, rotation) -> None:
        super().__init__()
        self.position = position
        self.rotation = rotation
        self.id = p.loadURDF(urdf, position, rotation, useFixedBase=True)

    def step(self):
        pass