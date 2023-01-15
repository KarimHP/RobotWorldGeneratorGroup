class BaseObstacle:
    id: int
    position: list[float]
    rotation: list[float]
    scale: float = 1

    def step(self):
        pass
