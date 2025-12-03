"""
Empirical Complexity Analysis
Measures actual running time vs. input size to verify Big-O complexity.
"""

import time
from grid_graph import GridGraph
from pathfinding import BFS, Dijkstra, AStar
import matplotlib.pyplot as plt


class ComplexityAnalyzer:
    """Analyzes empirical complexity of pathfinding algorithms."""
    
    @staticmethod
    def time_algorithm(grid_size, algorithm_class, trials=3):
        """
        Time an algorithm on a grid of given size.
        
        Args:
            grid_size: Size of square grid (grid_size x grid_size)
            algorithm_class: BFS, Dijkstra, or AStar
            trials: Number of trials to average
        
        Returns:
            Average time in milliseconds
        """
        total_time = 0
        
        for _ in range(trials):
            grid = GridGraph(grid_size, grid_size)
            pathfinder = algorithm_class(grid)
            
            start = (0, 0)
            goal = (grid_size - 1, grid_size - 1)
            
            start_time = time.time()
            pathfinder.find_path(start, goal)
            elapsed = time.time() - start_time
            
            total_time += elapsed
        
        return (total_time / trials) * 1000  # Convert to ms
    
    @staticmethod
    def analyze_scalability():
        """Analyze how algorithms scale with grid size."""
        grid_sizes = [5, 10, 15, 20, 30, 40]
        
        bfs_times = []
        dijkstra_times = []
        astar_times = []
        
        print("Analyzing algorithm scalability...")
        print("Grid Size | BFS (ms) | Dijkstra (ms) | A* (ms)")
        print("-" * 50)
        
        for size in grid_sizes:
            bfs_time = ComplexityAnalyzer.time_algorithm(size, BFS)
            dijkstra_time = ComplexityAnalyzer.time_algorithm(size, Dijkstra)
            astar_time = ComplexityAnalyzer.time_algorithm(size, AStar)
            
            bfs_times.append(bfs_time)
            dijkstra_times.append(dijkstra_time)
            astar_times.append(astar_time)
            
            print(f"{size:9d} | {bfs_time:8.3f} | {dijkstra_time:13.3f} | {astar_time:8.3f}")
        
        return grid_sizes, bfs_times, dijkstra_times, astar_times
    
    @staticmethod
    def analyze_with_obstacles():
        """Analyze algorithms with varying obstacle density."""
        grid_size = 30
        obstacle_densities = [0, 10, 20, 30, 40]
        
        bfs_times = []
        dijkstra_times = []
        astar_times = []
        explored_counts = {'BFS': [], 'Dijkstra': [], 'A*': []}
        
        print("\nAnalyzing with obstacle density...")
        print("Density | BFS (ms) | Dijkstra (ms) | A* (ms) | Explored")
        print("-" * 60)
        
        for density in obstacle_densities:
            grid = GridGraph(grid_size, grid_size)
            
            # Add walls based on density
            obstacle_count = int((grid_size * grid_size * density) / 100)
            placed = 0
            for row in range(grid_size):
                for col in range(grid_size):
                    if placed < obstacle_count and (row, col) not in [(0, 0), (grid_size-1, grid_size-1)]:
                        if (row + col) % (100 // (density + 1)) == 0:
                            grid.set_cell(row, col, -1)
                            placed += 1
            
            start = (0, 0)
            goal = (grid_size - 1, grid_size - 1)
            
            # BFS
            bfs = BFS(grid)
            start_time = time.time()
            bfs.find_path(start, goal)
            bfs_time = (time.time() - start_time) * 1000
            bfs_times.append(bfs_time)
            explored_counts['BFS'].append(bfs.explored_nodes)
            
            # Dijkstra
            dijkstra = Dijkstra(grid)
            start_time = time.time()
            dijkstra.find_path(start, goal)
            dijkstra_time = (time.time() - start_time) * 1000
            dijkstra_times.append(dijkstra_time)
            explored_counts['Dijkstra'].append(dijkstra.explored_nodes)
            
            # A*
            astar = AStar(grid)
            start_time = time.time()
            astar.find_path(start, goal)
            astar_time = (time.time() - start_time) * 1000
            astar_times.append(astar_time)
            explored_counts['A*'].append(astar.explored_nodes)
            
            print(f"{density:7d} | {bfs_time:8.3f} | {dijkstra_time:13.3f} | {astar_time:8.3f} | "
                  f"BFS:{explored_counts['BFS'][-1]:4d} Dij:{explored_counts['Dijkstra'][-1]:4d} "
                  f"A*:{explored_counts['A*'][-1]:4d}")
        
        return obstacle_densities, bfs_times, dijkstra_times, astar_times, explored_counts


def plot_complexity_results():
    """Plot and save complexity analysis results."""
    analyzer = ComplexityAnalyzer()
    
    # Scalability analysis
    sizes, bfs_times, dijkstra_times, astar_times = analyzer.analyze_scalability()
    
    plt.figure(figsize=(12, 5))
    
    # Time complexity plot
    plt.subplot(1, 2, 1)
    plt.plot(sizes, bfs_times, 'o-', label='BFS', linewidth=2)
    plt.plot(sizes, dijkstra_times, 's-', label='Dijkstra', linewidth=2)
    plt.plot(sizes, astar_times, '^-', label='A*', linewidth=2)
    plt.xlabel('Grid Size (n x n)')
    plt.ylabel('Time (ms)')
    plt.title('Algorithm Scalability')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Nodes explored plot
    obstacles = [0, 10, 20, 30, 40]
    grid_size = 30
    explored_bfs = []
    explored_dijkstra = []
    explored_astar = []
    
    for density in obstacles:
        grid = GridGraph(grid_size, grid_size)
        obstacle_count = int((grid_size * grid_size * density) / 100)
        placed = 0
        for row in range(grid_size):
            for col in range(grid_size):
                if placed < obstacle_count and (row, col) not in [(0, 0), (grid_size-1, grid_size-1)]:
                    if (row + col) % (100 // (density + 1)) == 0:
                        grid.set_cell(row, col, -1)
                        placed += 1
        
        bfs = BFS(grid)
        bfs.find_path((0, 0), (grid_size - 1, grid_size - 1))
        explored_bfs.append(bfs.explored_nodes)
        
        dijkstra = Dijkstra(grid)
        dijkstra.find_path((0, 0), (grid_size - 1, grid_size - 1))
        explored_dijkstra.append(dijkstra.explored_nodes)
        
        astar = AStar(grid)
        astar.find_path((0, 0), (grid_size - 1, grid_size - 1))
        explored_astar.append(astar.explored_nodes)
    
    plt.subplot(1, 2, 2)
    plt.plot(obstacles, explored_bfs, 'o-', label='BFS', linewidth=2)
    plt.plot(obstacles, explored_dijkstra, 's-', label='Dijkstra', linewidth=2)
    plt.plot(obstacles, explored_astar, '^-', label='A*', linewidth=2)
    plt.xlabel('Obstacle Density (%)')
    plt.ylabel('Nodes Explored')
    plt.title('Nodes Explored vs. Obstacle Density (30x30 grid)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('complexity_analysis.png', dpi=100)
    print("\nPlot saved as 'complexity_analysis.png'")
    plt.show()


if __name__ == '__main__':
    print("=" * 60)
    print("EMPIRICAL COMPLEXITY ANALYSIS")
    print("=" * 60)
    
    plot_complexity_results()
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
