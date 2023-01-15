from obstacles.base_obstacle import BaseObstacle
from .human.man.man import Man

DONE_THRESHOLD = 1


class HumanObstacleStatic(BaseObstacle):
    timestep = .01
    current_move_point = 0
    move_transforms = []

    def __init__(self, position, rotation, scale=1) -> None:
        super().__init__()
        self.human = Man(0, partitioned=False, scaling=scale, static=True)
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.human.resetGlobalTransformation(position)

    def step(self):
        pass
