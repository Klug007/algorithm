# Small tests for our path code

import unittest
from main import GridGraph, BFS, Dijkstra, AStar


def print_grid_simple(grid):
    for row in grid.grid:
        line = " ".join("#" if c == -1 else "." if c == 0 else str(c) for c in row)
        print(line)


class PathTests(unittest.TestCase):
    # test 1: 3x3 grid, no walls
    # S . .
    # . . .
    # . . G
    def test_1_open_grid_bfs(self):
        grid = GridGraph(3, 3)
        start, goal = (0, 0), (2, 2)
        print("\nTest 1 - BFS on open 3x3 grid")
        print("Grid:")
        print_grid_simple(grid)
        path = BFS(grid).find_path(start, goal)
        print("Found path:", path)
        # should find a path from S to G
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        self.assertEqual(len(path), 5)  # shortest in 3x3 without diagonals

    # test 2: 3x3 grid, center is a wall
    # S . .
    # . # .
    # . . G
    def test_2_wall_detour_bfs(self):
        grid = GridGraph(3, 3)
        grid.set_cell(1, 1, -1)
        print("\nTest 2 - BFS with wall in the middle")
        print("Grid (# is wall):")
        print_grid_simple(grid)
        path = BFS(grid).find_path((0, 0), (2, 2))
        print("Found path:", path)
        # must go around the wall
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 5)

    # test 3: 3x3 grid, middle row is all walls
    # S . .
    # # # #
    # . . G
    def test_3_unreachable(self):
        grid = GridGraph(3, 3)
        for c in range(3):
            grid.set_cell(1, c, -1)
        print("\nTest 3 - unreachable goal (full wall row)")
        print("Grid:")
        print_grid_simple(grid)
        path = BFS(grid).find_path((0, 0), (2, 2))
        print("Found path:", path)
        # here goal cannot be reached at all
        self.assertIsNone(path)

    # test 4: 2 rows, 3 columns (3x2)
    # (0,0) [10] (0,2)
    # (1,0) (1,1) (1,2)
    # middle top cell is very expensive (10), Dijkstra should avoid it
    def test_4_weighted_prefers_cheaper(self):
        grid = GridGraph(3, 2)
        grid.set_cell(0, 1, 10)
        start, goal = (0, 0), (0, 2)
        print("\nTest 4 - Dijkstra on weighted grid (3x2)")
        print("Grid (. = cost 1, numbers = cost, # = wall):")
        print_grid_simple(grid)
        path = Dijkstra(grid).find_path(start, goal)
        print("Found path:", path)
        # path should go down, then right, then up
        self.assertEqual(path, [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)])

    # test 5: 5x5 grid with one wall in the middle
    # A* should still find some path from corner to corner
    def test_5_astar_finds_path(self):
        grid = GridGraph(5, 5)
        grid.set_cell(2, 2, -1)
        print("\nTest 5 - A* on 5x5 grid with a wall")
        print("Grid:")
        print_grid_simple(grid)
        path = AStar(grid).find_path((0, 0), (4, 4))
        print("Found path:", path)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))


if __name__ == '__main__':
    unittest.main()
