"""
Grid Graph Module: Represents a grid as a graph structure.
Supports weighted and unweighted cells with walls/obstacles.
"""

from typing import List, Tuple, Set
from collections import deque


class GridGraph:
    """Represents a 2D grid as a graph with cells as nodes."""
    
    def __init__(self, width: int, height: int):
        """
        Initialize a grid graph.
        
        Args:
            width: Number of columns
            height: Number of rows
        """
        self.width = width
        self.height = height
        # Grid[row][col]: 0 = empty, -1 = wall, >0 = weight
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    def set_cell(self, row: int, col: int, value: int) -> None:
        """
        Set a cell value.
        
        Args:
            row: Row index
            col: Column index
            value: -1 for wall, 0 for empty, >0 for weighted cell
        """
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = value
    
    def get_cell(self, row: int, col: int) -> int:
        """Get cell value. Returns None if out of bounds."""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None
    
    def is_walkable(self, row: int, col: int) -> bool:
        """Check if a cell is walkable (not a wall)."""
        cell = self.get_cell(row, col)
        return cell is not None and cell != -1
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get 4-connected neighbors (up, down, left, right).
        
        Returns:
            List of (row, col) tuples for walkable neighbors
        """
        neighbors = []
        # Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_walkable(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def get_cost(self, row: int, col: int) -> int:
        """
        Get the cost/weight of moving to a cell.
        
        Returns:
            1 for empty cells, weight for weighted cells, 0 for walls
        """
        cell = self.get_cell(row, col)
        if cell == 0:
            return 1  # Default cost for empty cell
        elif cell > 0:
            return cell  # Use cell weight
        return 0  # Wall has 0 cost (not walkable)
    
    def __str__(self) -> str:
        """String representation of the grid."""
        result = []
        for row in self.grid:
            row_str = []
            for cell in row:
                if cell == -1:
                    row_str.append('#')
                elif cell == 0:
                    row_str.append('.')
                else:
                    row_str.append(str(min(cell, 9)))  # Cap at 9 for display
            result.append(' '.join(row_str))
        return '\n'.join(result)
