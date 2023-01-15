import pybullet as p
from ..base_obstacle import BaseObstacle

class StaticObject(BaseObstacle):

    def __init__(self, urdf, position, rotation, scale=1) -> None:
        super().__init__(position, rotation, scale)
        self.urdf = urdf
        self.load_urdf()
        
    def load_urdf(self):
        self.id = p.loadURDF(self.urdf, self.position, self.rotation, useFixedBase=True, globalScaling=self.scale)

    def step(self):
        pass