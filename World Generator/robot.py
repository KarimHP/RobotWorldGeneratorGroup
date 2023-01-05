import pybullet as p

class Robot:

    def __init__(self, urdf, position, rotation) -> None:
        self.id = p.loadURDF(urdf, position, rotation, useFixedBase=True)