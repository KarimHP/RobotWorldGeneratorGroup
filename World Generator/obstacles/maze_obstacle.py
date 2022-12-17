import pybullet as p
import numpy as np
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.generate.DungeonRooms import DungeonRooms

class MazeObstacle:

    def __init__(self) -> None:
        pass

    def _create_visual_box(self, halfExtents):
        visual_id = p.createVisualShape(shapeType=p.GEOM_BOX, halfExtents=halfExtents, rgbaColor=[0.5,0.5,0.5,1])
        return visual_id
    def _create_collision_box(self, halfExtents):
        collision_id = p.createCollisionShape(shapeType=p.GEOM_BOX, halfExtents=halfExtents)
        return collision_id

    def generate(self, position, rotation, width, height, unit_size=.5, wall_height=1, wall_width=.25):
        start_x = position[0]
        start_y = position[1]
        start_z = position[2]

        m = Maze()
        m.generator = DungeonRooms(width, height)
        m.generate()

        for row_idx, row in enumerate(m.grid):
            for cell_idx, cell in enumerate(row):
                if cell == 0:
                    continue
                if cell_idx < len(row) - 1 and row[cell_idx + 1] == 1:
                    p.createMultiBody(
                            baseMass=0,
                            baseVisualShapeIndex=self._create_visual_box([unit_size,
                                                                        wall_width,
                                                                        wall_height]),
                            baseCollisionShapeIndex=self._create_collision_box([unit_size,
                                                                        wall_width,
                                                                        wall_height]),
                            basePosition=[start_x + cell_idx * unit_size * 2 + unit_size, start_y + row_idx * unit_size * 2, start_z + wall_height],
                            baseOrientation=rotation
                        )    
                if row_idx < len(m.grid) - 1 and m.grid[row_idx + 1][cell_idx] == 1:
                    p.createMultiBody(
                            baseMass=0,
                            baseVisualShapeIndex=self._create_visual_box([wall_width,
                                                                        unit_size,
                                                                        wall_height]),
                            baseCollisionShapeIndex=self._create_collision_box([wall_width,
                                                                        unit_size,
                                                                        wall_height]),
                            basePosition=[start_x + cell_idx * unit_size * 2, start_y + row_idx * unit_size * 2 + unit_size, start_z + wall_height],
                            baseOrientation=rotation
                        )     
                    
        