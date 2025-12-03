"""
Shortest Path Algorithms: BFS, Dijkstra, and A*
Implements pathfinding algorithms on a grid graph.
"""

from typing import List, Tuple, Optional, Dict
from collections import deque
import heapq
import math


class PathFinder:
    """Base class for pathfinding algorithms."""
    
    def __init__(self, grid_graph):
        """
        Initialize pathfinder.
        
        Args:
            grid_graph: GridGraph instance
        """
        self.grid = grid_graph
        self.explored_nodes = 0
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """Find path from start to goal. Must be implemented by subclass."""
        raise NotImplementedError
    
    def reconstruct_path(self, came_from: Dict, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct path from came_from dictionary.
        
        Time Complexity: O(path_length)
        """
        path = []
        current = goal
        
        while current in came_from:
            path.append(current)
            current = came_from[current]
        
        path.append(start)
        path.reverse()
        return path


class BFS(PathFinder):
    """
    Breadth-First Search for unweighted grids.
    
    Time Complexity: O(V + E) where V = cells, E = edges
    Space Complexity: O(V)
    """
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find shortest path using BFS.
        
        Args:
            start: (row, col) starting position
            goal: (row, col) goal position
        
        Returns:
            List of coordinates from start to goal, or None if unreachable
        """
        if not self.grid.is_walkable(*start) or not self.grid.is_walkable(*goal):
            return None
        
        self.explored_nodes = 0
        queue = deque([start])
        visited = {start}
        came_from = {}
        
        while queue:
            current = queue.popleft()
            self.explored_nodes += 1
            
            if current == goal:
                return self.reconstruct_path(came_from, start, goal)
            
            for neighbor in self.grid.get_neighbors(*current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        return None  # Goal unreachable


class Dijkstra(PathFinder):
    """
    Dijkstra's Algorithm for weighted grids.
    
    Time Complexity: O((V + E) log V) where V = cells, E = edges
    Space Complexity: O(V)
    """
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find shortest path using Dijkstra's algorithm.
        
        Args:
            start: (row, col) starting position
            goal: (row, col) goal position
        
        Returns:
            List of coordinates from start to goal, or None if unreachable
        """
        if not self.grid.is_walkable(*start) or not self.grid.is_walkable(*goal):
            return None
        
        self.explored_nodes = 0
        distances = {}
        came_from = {}
        visited = set()
        
        # Initialize distances
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                distances[(row, col)] = float('inf')
        distances[start] = 0
        
        # Min heap: (distance, node)
        heap = [(0, start)]
        
        while heap:
            current_dist, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            self.explored_nodes += 1
            
            if current == goal:
                return self.reconstruct_path(came_from, start, goal)
            
            if current_dist > distances[current]:
                continue
            
            for neighbor in self.grid.get_neighbors(*current):
                if neighbor not in visited:
                    cost = self.grid.get_cost(*neighbor)
                    new_dist = current_dist + cost
                    
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        came_from[neighbor] = current
                        heapq.heappush(heap, (new_dist, neighbor))
        
        return None  # Goal unreachable


class AStar(PathFinder):
    """
    A* Algorithm with Manhattan heuristic for weighted grids.
    
    Time Complexity: O((V + E) log V) where V = cells, E = edges
    Space Complexity: O(V)
    """
    
    @staticmethod
    def manhattan_heuristic(pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
        """
        Manhattan distance heuristic.
        
        Time Complexity: O(1)
        """
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find shortest path using A* algorithm.
        
        Args:
            start: (row, col) starting position
            goal: (row, col) goal position
        
        Returns:
            List of coordinates from start to goal, or None if unreachable
        """
        if not self.grid.is_walkable(*start) or not self.grid.is_walkable(*goal):
            return None
        
        self.explored_nodes = 0
        g_scores = {}
        came_from = {}
        visited = set()
        
        # Initialize g_scores
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                g_scores[(row, col)] = float('inf')
        g_scores[start] = 0
        
        # Min heap: (f_score, node) where f_score = g + h
        h_start = self.manhattan_heuristic(start, goal)
        heap = [(h_start, start)]
        
        while heap:
            f_score, current = heapq.heappop(heap)
            
            if current in visited:
                continue
            
            visited.add(current)
            self.explored_nodes += 1
            
            if current == goal:
                return self.reconstruct_path(came_from, start, goal)
            
            for neighbor in self.grid.get_neighbors(*current):
                if neighbor not in visited:
                    cost = self.grid.get_cost(*neighbor)
                    tentative_g = g_scores[current] + cost
                    
                    if tentative_g < g_scores[neighbor]:
                        g_scores[neighbor] = tentative_g
                        came_from[neighbor] = current
                        
                        h = self.manhattan_heuristic(neighbor, goal)
                        f = tentative_g + h
                        heapq.heappush(heap, (f, neighbor))
        
        return None  # Goal unreachable
