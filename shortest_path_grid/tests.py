# Simple tests to check basics

import unittest
from main import GridGraph, BFS, Dijkstra, AStar


class PathTests(unittest.TestCase):
    def test_open_grid_bfs(self):
        grid = GridGraph(3, 3)
        start, goal = (0, 0), (2, 2)
        path = BFS(grid).find_path(start, goal)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], goal)
        self.assertEqual(len(path), 5)  # shortest in 3x3 without diagonals

    def test_wall_detour_bfs(self):
        grid = GridGraph(3, 3)
        grid.set_cell(1, 1, -1)  # block center
        path = BFS(grid).find_path((0, 0), (2, 2))
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 5)  # must detour but still 4 moves

    def test_unreachable(self):
        grid = GridGraph(3, 3)
        for c in range(3):
            grid.set_cell(1, c, -1)  # solid wall across middle row
        path = BFS(grid).find_path((0, 0), (2, 2))
        self.assertIsNone(path)

    def test_weighted_prefers_cheaper(self):
        grid = GridGraph(3, 2)  # 2 rows, 3 columns
        grid.set_cell(0, 1, 10)  # expensive cell
        start, goal = (0, 0), (0, 2)
        path = Dijkstra(grid).find_path(start, goal)
        self.assertEqual(path, [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)])

    def test_astar_finds_path(self):
        grid = GridGraph(5, 5)
        grid.set_cell(2, 2, -1)
        path = AStar(grid).find_path((0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))


if __name__ == '__main__':
    unittest.main()

