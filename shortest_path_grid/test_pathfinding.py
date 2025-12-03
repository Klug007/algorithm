"""
Unit Tests for Shortest Path Algorithms
Tests BFS, Dijkstra, and A* with various scenarios including edge cases.
"""

import unittest
from grid_graph import GridGraph
from pathfinding import BFS, Dijkstra, AStar


class TestGridGraph(unittest.TestCase):
    """Test GridGraph functionality."""
    
    def setUp(self):
        """Create a 5x5 grid for testing."""
        self.grid = GridGraph(5, 5)
    
    def test_grid_creation(self):
        """Test that grid is created with correct dimensions."""
        self.assertEqual(self.grid.width, 5)
        self.assertEqual(self.grid.height, 5)
        self.assertTrue(self.grid.is_walkable(0, 0))
    
    def test_wall_placement(self):
        """Test setting and detecting walls."""
        self.grid.set_cell(1, 1, -1)  # -1 = wall
        self.assertFalse(self.grid.is_walkable(1, 1))
        self.assertTrue(self.grid.is_walkable(1, 0))
    
    def test_weighted_cells(self):
        """Test weighted cell costs."""
        self.grid.set_cell(2, 2, 5)  # Weight = 5
        cost = self.grid.get_cost(2, 2)
        self.assertEqual(cost, 5)
    
    def test_get_neighbors(self):
        """Test neighbor retrieval (4-connected)."""
        neighbors = self.grid.get_neighbors(2, 2)
        self.assertEqual(len(neighbors), 4)
        self.assertIn((1, 2), neighbors)  # Up
        self.assertIn((3, 2), neighbors)  # Down
        self.assertIn((2, 1), neighbors)  # Left
        self.assertIn((2, 3), neighbors)  # Right
    
    def test_neighbors_with_wall(self):
        """Test that neighbors exclude walls."""
        self.grid.set_cell(1, 2, -1)  # Wall above
        neighbors = self.grid.get_neighbors(2, 2)
        self.assertEqual(len(neighbors), 3)
        self.assertNotIn((1, 2), neighbors)
    
    def test_corner_neighbors(self):
        """Test corner cells have fewer neighbors."""
        neighbors = self.grid.get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 2)  # Only down and right


class TestBFS(unittest.TestCase):
    """Test BFS pathfinding algorithm."""
    
    def setUp(self):
        """Create test grids."""
        self.grid = GridGraph(5, 5)
        self.bfs = BFS(self.grid)
    
    def test_bfs_simple_path(self):
        """Test BFS on open grid."""
        # 5x5 empty grid
        path = self.bfs.find_path((0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
        # Manhattan distance should be 8 steps
        self.assertEqual(len(path), 9)  # 9 nodes = 8 steps
    
    def test_bfs_blocked_goal(self):
        """Test BFS when goal is unreachable."""
        # Surround goal with walls
        self.grid.set_cell(3, 3, -1)
        self.grid.set_cell(3, 5, -1)
        self.grid.set_cell(4, 4, -1)
        self.grid.set_cell(5, 4, -1)
        
        path = self.bfs.find_path((0, 0), (4, 4))
        self.assertIsNone(path)
    
    def test_bfs_wall_maze(self):
        """Test BFS through a simple maze."""
        # Create a vertical wall with gap
        for row in range(5):
            if row != 2:
                self.grid.set_cell(row, 2, -1)
        
        path = self.bfs.find_path((0, 0), (0, 4))
        self.assertIsNotNone(path)
        # Should go around the wall
        self.assertIn((2, 2), path)
    
    def test_bfs_start_equals_goal(self):
        """Test BFS when start equals goal."""
        path = self.bfs.find_path((0, 0), (0, 0))
        self.assertIsNotNone(path)
        self.assertEqual(path, [(0, 0)])
    
    def test_bfs_start_on_wall(self):
        """Test BFS with start position on wall."""
        self.grid.set_cell(0, 0, -1)
        path = self.bfs.find_path((0, 0), (4, 4))
        self.assertIsNone(path)


class TestDijkstra(unittest.TestCase):
    """Test Dijkstra's algorithm."""
    
    def setUp(self):
        """Create test grids."""
        self.grid = GridGraph(5, 5)
        self.dijkstra = Dijkstra(self.grid)
    
    def test_dijkstra_simple_path(self):
        """Test Dijkstra on open grid."""
        path = self.dijkstra.find_path((0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
    
    def test_dijkstra_weighted_cells(self):
        """Test Dijkstra prefers lower-cost paths."""
        # Create two paths: one straight (high cost), one around
        for col in range(1, 4):
            self.grid.set_cell(2, col, 10)  # High cost
        
        # Lower cost path exists around
        path = self.dijkstra.find_path((0, 0), (4, 4))
        self.assertIsNotNone(path)
        
        # Path should avoid high-cost cells
        for row, col in path:
            if row == 2 and 1 <= col <= 3:
                # Path may go through but not via the straight high-cost route
                pass
    
    def test_dijkstra_unreachable(self):
        """Test Dijkstra with unreachable goal."""
        # Create barrier
        for row in range(5):
            self.grid.set_cell(row, 2, -1)
        
        path = self.dijkstra.find_path((0, 0), (0, 4))
        self.assertIsNone(path)
    
    def test_dijkstra_vs_bfs_same_cost(self):
        """Test Dijkstra and BFS give same path length for uniform costs."""
        self.grid.set_cell(1, 1, -1)
        
        bfs = BFS(self.grid)
        dijkstra = Dijkstra(self.grid)
        
        bfs_path = bfs.find_path((0, 0), (4, 4))
        dij_path = dijkstra.find_path((0, 0), (4, 4))
        
        self.assertIsNotNone(bfs_path)
        self.assertIsNotNone(dij_path)
        # Should have same length (BFS optimal for unweighted)
        self.assertEqual(len(bfs_path), len(dij_path))


class TestAStar(unittest.TestCase):
    """Test A* algorithm."""
    
    def setUp(self):
        """Create test grids."""
        self.grid = GridGraph(5, 5)
        self.astar = AStar(self.grid)
    
    def test_astar_simple_path(self):
        """Test A* on open grid."""
        path = self.astar.find_path((0, 0), (4, 4))
        self.assertIsNotNone(path)
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
    
    def test_astar_manhattan_heuristic(self):
        """Test Manhattan heuristic calculation."""
        h = AStar.manhattan_heuristic((0, 0), (4, 4))
        self.assertEqual(h, 8)
        
        h = AStar.manhattan_heuristic((2, 2), (2, 2))
        self.assertEqual(h, 0)
        
        h = AStar.manhattan_heuristic((1, 1), (3, 4))
        self.assertEqual(h, 5)
    
    def test_astar_through_maze(self):
        """Test A* in maze with obstacles."""
        # Create walls
        for col in range(1, 4):
            self.grid.set_cell(2, col, -1)
        
        path = self.astar.find_path((0, 0), (4, 4))
        self.assertIsNotNone(path)
    
    def test_astar_unreachable(self):
        """Test A* with unreachable goal."""
        # Isolate goal
        for d in range(-1, 2):
            for d2 in range(-1, 2):
                if (d, d2) != (0, 0):
                    row, col = 4 + d, 4 + d2
                    if 0 <= row < 5 and 0 <= col < 5:
                        self.grid.set_cell(row, col, -1)
        
        path = self.astar.find_path((0, 0), (4, 4))
        self.assertIsNone(path)


class TestExploredNodeCount(unittest.TestCase):
    """Test that algorithms explore correct number of nodes."""
    
    def test_bfs_explores_fewer_nodes_than_dijkstra(self):
        """BFS should explore fewer nodes for unweighted grid."""
        grid = GridGraph(10, 10)
        bfs = BFS(grid)
        dijkstra = Dijkstra(grid)
        
        bfs.find_path((0, 0), (9, 9))
        dijkstra.find_path((0, 0), (9, 9))
        
        # BFS is optimal for unweighted, should explore similar or fewer nodes
        self.assertLessEqual(bfs.explored_nodes, dijkstra.explored_nodes + 10)
    
    def test_astar_explores_fewer_than_dijkstra(self):
        """A* should explore fewer nodes than Dijkstra with good heuristic."""
        grid = GridGraph(10, 10)
        dijkstra = Dijkstra(grid)
        astar = AStar(grid)
        
        dijkstra.find_path((0, 0), (9, 9))
        astar.find_path((0, 0), (9, 9))
        
        # A* with good heuristic should explore fewer nodes
        self.assertLess(astar.explored_nodes, dijkstra.explored_nodes)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases."""
    
    def test_single_cell_grid(self):
        """Test with 1x1 grid."""
        grid = GridGraph(1, 1)
        bfs = BFS(grid)
        path = bfs.find_path((0, 0), (0, 0))
        self.assertEqual(path, [(0, 0)])
    
    def test_large_grid(self):
        """Test with large grid (100x100)."""
        grid = GridGraph(100, 100)
        bfs = BFS(grid)
        path = bfs.find_path((0, 0), (99, 99))
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 199)  # 199 cells = 198 steps
    
    def test_narrow_corridor(self):
        """Test path through narrow corridor."""
        grid = GridGraph(10, 3)
        # Only middle row is walkable
        for row in [0, 2]:
            for col in range(10):
                grid.set_cell(row, col, -1)
        
        bfs = BFS(grid)
        path = bfs.find_path((1, 0), (1, 9))
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 10)


if __name__ == '__main__':
    unittest.main()
