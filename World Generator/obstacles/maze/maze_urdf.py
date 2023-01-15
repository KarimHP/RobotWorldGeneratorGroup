import pybullet as p
import numpy as np
import random
import os
from helpers.helpers import URDF_PATH
from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.generate.DungeonRooms import DungeonRooms
from mazelib.solve.BacktrackingSolver import BacktrackingSolver

from obstacles.base_obstacle import BaseObstacle
from helpers.urdf_wall_generator import UrdfWallGenerator

class MazeUrdf(BaseObstacle):

    def __init__(self, params) -> None:
        self.params = params


    def has_el_prev_row(self, grid, row_idx, cell_idx):
        return row_idx > 0 and grid[row_idx - 1][cell_idx] == 1

    def has_el_next_row(self, grid, row_idx, cell_idx):
        return row_idx < len(grid) - 1 and grid[row_idx + 1][cell_idx] == 1

    def has_el_prev_col(self, grid, row_idx, cell_idx):
        return cell_idx > 0 and grid[row_idx][cell_idx - 1] == 1

    def has_el_next_col(self, grid, row_idx, cell_idx):
        return cell_idx < len(grid[row_idx]) - 1 and grid[row_idx][cell_idx + 1]

    def generate(self):
        cols = self.params["cols"]
        rows = self.params["rows"]
        element_size = self.params["element_size"]
        element_depth = self.params["element_depth"]
        wall_thickness = self.params["wall_thickness"]
        difficulty = self.params["difficulty"]

        connector_strict = self.params["connector_strict"]
        connector_probability = self.params["connector_probability"]
        connector_height = self.params["connector_height"]

        xy_offset = (wall_thickness / 2)
        wall_size = element_size + wall_thickness

        m = Maze()
        m.generator = DungeonRooms(cols, rows)
        m.solver = BacktrackingSolver()
        m.generate_monte_carlo(100, 10, difficulty)

        urdf = UrdfWallGenerator()
        for row_idx, row in enumerate(m.grid):
            for cell_idx, cell in enumerate(row):
                curr_x = xy_offset + cell_idx * element_size
                curr_y = xy_offset + row_idx * element_size
                if cell == 0:
                    # random connector obstacles
                    if random.random() < connector_probability:
                        has_prev_row = self.has_el_prev_row(m.grid, row_idx, cell_idx)
                        has_next_row = self.has_el_next_row(m.grid, row_idx, cell_idx)
                        has_prev_col = self.has_el_prev_col(m.grid, row_idx, cell_idx)
                        has_next_col = self.has_el_next_col(m.grid, row_idx, cell_idx)
                        if (has_prev_row and has_next_row) or (connector_strict == False and (has_prev_row or has_next_row)):
                            urdf.add_wall(wall_thickness, element_size * 2, connector_height, curr_x, curr_y, connector_height / 2)
                        if (has_prev_col and has_next_col) or (connector_strict == False and (has_prev_col or has_next_col)):
                            urdf.add_wall(element_size * 2, wall_thickness, connector_height, curr_x, curr_y, connector_height / 2)
                    continue

                if self.has_el_next_col(m.grid, row_idx, cell_idx):
                    urdf.add_wall(wall_size, wall_thickness, element_depth, curr_x + (element_size / 2), curr_y, element_depth / 2)

                if self.has_el_next_row(m.grid, row_idx, cell_idx):
                    urdf.add_wall(wall_thickness, wall_size, element_depth, curr_x, curr_y + (element_size / 2), element_depth / 2)


        file_name = os.path.join(URDF_PATH, "generated", "maze.urdf")

        f = open(file_name, "w")
        f.write(urdf.get_urdf())
        f.close()

        return file_name
        #self.id = p.loadURDF(file_name, self.position, self.rotation, useFixedBase=True, globalScaling=self.scale)

        # Funktioniert nicht mehr ohne weiteres aber eig egal
        # max_x = xy_offset + cols * element_size
        # max_y = xy_offset + rows * element_size
        # for i in range(0, len(m.solutions[0]) - 1):
        #     from_y = ((m.solutions[0][i][0] - 1) / cols) * max_x + wall_size
        #     from_x = ((m.solutions[0][i][1] - 1) / rows) * max_y + wall_size
        #     to_y = ((m.solutions[0][i + 1][0] - 1) / cols) * max_x + wall_size
        #     to_x = ((m.solutions[0][i + 1][1] - 1) / rows) * max_y + wall_size
            
        #     p.addUserDebugLine([from_x, from_y, .1], [to_x, to_y, .1], [1, 1, 0], 3, 0, self.id, 0)

                    
        