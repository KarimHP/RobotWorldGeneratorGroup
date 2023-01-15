import time
from helpers.helpers import getPosition
import pybullet as p
from obstacles.urdf_object.static_object import StaticObject


class MovingObject(StaticObject):
    counter: int = 0
    current_idx: int = 0
    move_path: list

    def __init__(self, urdf, position, rotation, move_path, scale=1) -> None:
        super().__init__(urdf, position, rotation, scale)
        self.move_path = move_path
        self.counter = 0

    def get_last_el(self):
        if self.current_idx > 0:
            return self.move_path[self.current_idx - 1]
        else:
            return self.move_path[len(self.move_path) - 1]

    def step(self):
        current_el = self.move_path[self.current_idx]
        steps = current_el["steps"]
        if self.counter < steps:
            start_pos = getPosition(self.get_last_el())
            end_pos = getPosition(current_el)
            d = self.counter / steps
            new_pos = [start_pos[0] + d * (end_pos[0] - start_pos[0]),
                       start_pos[1] + d * (end_pos[1] - start_pos[1]),
                       start_pos[2] + d * (end_pos[2] - start_pos[2])]
            p.resetBasePositionAndOrientation(self.id, new_pos, self.rotation)
            self.counter += 1

        if self.counter >= steps:
            self.counter = 0
            self.current_idx = (self.current_idx + 1) % len(self.move_path)
