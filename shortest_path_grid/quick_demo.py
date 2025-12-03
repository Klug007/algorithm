"""
Quick Demo Script - Run to verify everything works
Shows all three algorithms in action with example cases
"""

from grid_graph import GridGraph
from pathfinding import BFS, Dijkstra, AStar
import time


def demo_1_simple_path():
    """Demo 1: Simple path on open grid."""
    print("\n" + "="*60)
    print("DEMO 1: Simple Path on Open Grid (5x5)")
    print("="*60)
    
    grid = GridGraph(5, 5)
    start = (0, 0)
    goal = (4, 4)
    
    print(f"\nGrid (. = empty, # = wall):")
    print(grid)
    print(f"\nStart: {start} (green)")
    print(f"Goal: {goal} (red)")
    
    for algo_name, algo_class in [('BFS', BFS), ('Dijkstra', Dijkstra), ('A*', AStar)]:
        pathfinder = algo_class(grid)
        start_time = time.time()
        path = pathfinder.find_path(start, goal)
        elapsed = (time.time() - start_time) * 1000
        
        print(f"\n{algo_name}:")
        print(f"  Path length: {len(path)} cells")
        print(f"  Path: {path}")
        print(f"  Nodes explored: {pathfinder.explored_nodes}")
        print(f"  Time: {elapsed:.3f} ms")


def demo_2_maze_with_walls():
    """Demo 2: Maze navigation with walls."""
    print("\n" + "="*60)
    print("DEMO 2: Maze with Walls (8x8)")
    print("="*60)
    
    grid = GridGraph(8, 8)
    
    # Create vertical wall with gap
    for row in range(8):
        if row != 3 and row != 4:
            grid.set_cell(row, 3, -1)
            grid.set_cell(row, 5, -1)
    
    start = (0, 0)
    goal = (0, 7)
    
    print(f"\nMaze (. = empty, # = wall):")
    print(grid)
    
    for algo_name, algo_class in [('BFS', BFS), ('Dijkstra', Dijkstra), ('A*', AStar)]:
        pathfinder = algo_class(grid)
        path = pathfinder.find_path(start, goal)
        
        print(f"\n{algo_name}:")
        if path:
            print(f"  Path found! Length: {len(path)} cells")
            print(f"  Nodes explored: {pathfinder.explored_nodes}")
            
            # Visualize path
            grid_copy = GridGraph(8, 8)
            for row in range(8):
                if row != 3 and row != 4:
                    grid_copy.set_cell(row, 3, -1)
                    grid_copy.set_cell(row, 5, -1)
            for r, c in path:
                if (r, c) != start and (r, c) != goal:
                    grid_copy.set_cell(r, c, 2)  # Mark path
            print("\nPath visualization (path marked with numbers):")
            print(grid_copy)
        else:
            print(f"  Path not found!")
            print(f"  Nodes explored: {pathfinder.explored_nodes}")


def demo_3_weighted_grid():
    """Demo 3: Weighted grid - Dijkstra finds lowest cost path."""
    print("\n" + "="*60)
    print("DEMO 3: Weighted Grid (Dijkstra vs BFS)")
    print("="*60)
    
    grid = GridGraph(5, 3)
    
    # Create high-cost zone in middle
    for col in range(1, 4):
        grid.set_cell(1, col, 5)  # Cost = 5 per cell
    
    start = (0, 0)
    goal = (2, 4)
    
    print(f"\nGrid (. = cost 1, numbers = cost value):")
    print(grid)
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    
    # BFS (unweighted - goes straight through)
    bfs = BFS(grid)
    bfs_path = bfs.find_path(start, goal)
    print(f"\nBFS (unweighted):")
    print(f"  Path: {bfs_path}")
    print(f"  Length: {len(bfs_path)} cells")
    
    # Dijkstra (weighted - avoids high cost)
    dijkstra = Dijkstra(grid)
    dij_path = dijkstra.find_path(start, goal)
    print(f"\nDijkstra (weighted):")
    print(f"  Path: {dij_path}")
    print(f"  Length: {len(dij_path)} cells")


def demo_4_algorithm_comparison():
    """Demo 4: Compare algorithm efficiency."""
    print("\n" + "="*60)
    print("DEMO 4: Algorithm Comparison (20x20 grid with obstacles)")
    print("="*60)
    
    grid = GridGraph(20, 20)
    
    # Add some random walls
    for row in range(20):
        for col in range(20):
            if (row + col) % 7 == 0 and (row, col) not in [(0, 0), (19, 19)]:
                grid.set_cell(row, col, -1)
    
    start = (0, 0)
    goal = (19, 19)
    
    results = {}
    
    for algo_name, algo_class in [('BFS', BFS), ('Dijkstra', Dijkstra), ('A*', AStar)]:
        pathfinder = algo_class(grid)
        start_time = time.time()
        path = pathfinder.find_path(start, goal)
        elapsed = (time.time() - start_time) * 1000
        
        results[algo_name] = {
            'path_length': len(path) if path else None,
            'nodes_explored': pathfinder.explored_nodes,
            'time': elapsed
        }
    
    print(f"\nComparison (20x20 grid with obstacles):")
    print(f"{'Algorithm':<12} {'Path Length':<15} {'Nodes Explored':<20} {'Time (ms)':<12}")
    print("-" * 59)
    
    for algo_name in ['BFS', 'Dijkstra', 'A*']:
        data = results[algo_name]
        path_len = data['path_length'] if data['path_length'] else 'N/A'
        print(f"{algo_name:<12} {str(path_len):<15} {data['nodes_explored']:<20} {data['time']:<12.3f}")
    
    # Show efficiency gain
    dijkstra_explored = results['Dijkstra']['nodes_explored']
    astar_explored = results['A*']['nodes_explored']
    if dijkstra_explored > 0:
        reduction = ((dijkstra_explored - astar_explored) / dijkstra_explored) * 100
        print(f"\nA* explores {reduction:.1f}% fewer nodes than Dijkstra!")


def demo_5_unreachable_goal():
    """Demo 5: Unreachable goal (isolated by walls)."""
    print("\n" + "="*60)
    print("DEMO 5: Unreachable Goal (Isolated by Walls)")
    print("="*60)
    
    grid = GridGraph(7, 7)
    
    # Isolate center with walls
    for r in range(7):
        for c in range(7):
            if (r == 3 or r == 4) and (c == 3 or c == 4):
                continue
            if (r == 3 or r == 4) and c == 5:
                grid.set_cell(r, c, -1)
            if (r == 3 or r == 4) and c == 3:
                grid.set_cell(r, c, -1)
            if r == 5 and (c == 3 or c == 4):
                grid.set_cell(r, c, -1)
            if r == 2 and (c == 3 or c == 4):
                grid.set_cell(r, c, -1)
    
    start = (0, 0)
    goal = (3, 3)
    
    print(f"\nGrid with isolated goal:")
    print(grid)
    
    for algo_name, algo_class in [('BFS', BFS), ('Dijkstra', Dijkstra), ('A*', AStar)]:
        pathfinder = algo_class(grid)
        path = pathfinder.find_path(start, goal)
        
        print(f"\n{algo_name}:")
        if path:
            print(f"  Path found! Length: {len(path)}")
        else:
            print(f"  Goal is unreachable")
            print(f"  Nodes explored before giving up: {pathfinder.explored_nodes}")


def run_all_demos():
    """Run all demos."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " SHORTEST PATH ALGORITHMS - INTERACTIVE DEMO ".center(58) + "║")
    print("║" + " BFS | Dijkstra | A* ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    demo_1_simple_path()
    demo_2_maze_with_walls()
    demo_3_weighted_grid()
    demo_4_algorithm_comparison()
    demo_5_unreachable_goal()
    
    print("\n" + "="*60)
    print("ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run unit tests: python test_pathfinding.py")
    print("2. Run interactive UI: python demo_ui.py")
    print("3. Analyze complexity: python complexity_analysis.py")
    print("="*60 + "\n")


if __name__ == '__main__':
    run_all_demos()
