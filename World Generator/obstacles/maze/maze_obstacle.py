import pybullet as p
import numpy as np
import random
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.generate.DungeonRooms import DungeonRooms
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

from obstacles.base_obstacle import BaseObstacle
from obstacles.maze.maze_urdf import MazeUrdf

class MazeObstacle(BaseObstacle):

    def __init__(self, position, rotation, params) -> None:
        self.position = position
        self.rotation = rotation
        self.params = params
        self.generate()


    def has_el_prev_row(self, grid, row_idx, cell_idx):
        return row_idx > 0 and grid[row_idx - 1][cell_idx] == 1

    def has_el_next_row(self, grid, row_idx, cell_idx):
        return row_idx < len(grid) - 1 and grid[row_idx + 1][cell_idx] == 1

    def has_el_prev_col(self, grid, row_idx, cell_idx):
        return cell_idx > 0 and grid[row_idx][cell_idx - 1] == 1

    def has_el_next_col(self, grid, row_idx, cell_idx):
        return cell_idx < len(grid[row_idx]) - 1 and grid[row_idx][cell_idx + 1]

    def generate(self):
        width = self.params["width"]
        height = self.params["height"]
        wall_width = self.params["wall_width"]
        wall_height = self.params["wall_height"]
        wall_thickness = self.params["wall_thickness"]
        difficulty = self.params["difficulty"]

        connector_strict = self.params["connector_strict"]
        connector_probability = self.params["connector_probability"]
        connector_height = self.params["connector_height"]

        xy_offset = (wall_thickness / 2)
        wall_size = wall_width + wall_thickness

        m = Maze()
        m.generator = DungeonRooms(width, height)
        m.solver = BacktrackingSolver()
        m.generate_monte_carlo(100, 10, difficulty)

        urdf = MazeUrdf(width * wall_width, height * wall_width, wall_height)
        for row_idx, row in enumerate(m.grid):
            for cell_idx, cell in enumerate(row):
                curr_x = xy_offset + cell_idx * wall_width
                curr_y = xy_offset + row_idx * wall_width
                if cell == 0:
                    # random connector obstacles
                    if random.random() < connector_probability:
                        has_prev_row = self.has_el_prev_row(m.grid, row_idx, cell_idx)
                        has_next_row = self.has_el_next_row(m.grid, row_idx, cell_idx)
                        has_prev_col = self.has_el_prev_col(m.grid, row_idx, cell_idx)
                        has_next_col = self.has_el_next_col(m.grid, row_idx, cell_idx)
                        if (has_prev_row and has_next_row) or (connector_strict == False and (has_prev_row or has_next_row)):
                            urdf.add_wall(wall_thickness, wall_width * 2, connector_height, curr_x, curr_y, connector_height / 2)
                        if (has_prev_col and has_next_col) or (connector_strict == False and (has_prev_col or has_next_col)):
                            urdf.add_wall(wall_width * 2, wall_thickness, connector_height, curr_x, curr_y, connector_height / 2)
                    continue

                if self.has_el_next_col(m.grid, row_idx, cell_idx):
                    urdf.add_wall(wall_size, wall_thickness, wall_height, curr_x + (wall_width / 2), curr_y, wall_height / 2)

                if self.has_el_next_row(m.grid, row_idx, cell_idx):
                    urdf.add_wall(wall_thickness, wall_size, wall_height, curr_x, curr_y + (wall_width / 2), wall_height / 2)


        file_name = "maze.urdf"

        f = open(file_name, "w")
        f.write(urdf.get_urdf())
        f.close()

        self.id = p.loadURDF(file_name, self.position, self.rotation, useFixedBase=True)

        max_x = xy_offset + width * wall_width
        max_y = xy_offset + height * wall_width
        for i in range(0, len(m.solutions[0]) - 1):
            from_y = ((m.solutions[0][i][0] - 1) / width) * max_x + wall_size
            from_x = ((m.solutions[0][i][1] - 1) / height) * max_y + wall_size
            to_y = ((m.solutions[0][i + 1][0] - 1) / width) * max_x + wall_size
            to_x = ((m.solutions[0][i + 1][1] - 1) / height) * max_y + wall_size
            
            p.addUserDebugLine([from_x, from_y, .1], [to_x, to_y, .1], [1, 1, 0], 3, 0, self.id, 0)

                    
        