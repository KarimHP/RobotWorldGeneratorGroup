import pybullet as p
from obstacles.urdf_object.static_object import StaticObject

class MovingObject(StaticObject):

    def __init__(self, urdf, position, rotation) -> None:
        super().__init__(urdf, position, rotation)

    def step(self):
        for idx, item in enumerate(self.position):
            self.position[idx] = item + .1
        
        p.resetBasePositionAndOrientation(self.id, self.position, self.rotation)