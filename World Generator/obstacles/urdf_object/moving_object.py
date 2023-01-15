import time

import pybullet as p
from obstacles.urdf_object.static_object import StaticObject


class MovingObject(StaticObject):

    def __init__(self, urdf, position, rotation, start_pos, end_pos, steps=100, scale=1) -> None:
        super().__init__(urdf, position, rotation, scale)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.steps = steps
        self.counter = 0

    def step(self):
        if self.counter < self.steps:
            d = self.counter / self.steps
            new_pos = [self.start_pos[0] + d * (self.end_pos[0] - self.start_pos[0]),
                       self.start_pos[1] + d * (self.end_pos[1] - self.start_pos[1]),
                       self.start_pos[2] + d * (self.end_pos[2] - self.start_pos[2])]
            p.resetBasePositionAndOrientation(self.id, new_pos, self.rotation)
            self.counter += 1

        if self.counter >= self.steps:
            self.counter = 0
            self.start_pos, self.end_pos = self.end_pos, self.start_pos
