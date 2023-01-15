class BaseObstacle:
    id: int
    position: list[float]
    rotation: list[float]
    scale: float = 1

    def __init__(self, position: list[float], rotation: list[float], scale: float) -> None:
        self.position = position
        self.rotation = rotation
        self.scale = scale

    def step(self):
        pass
