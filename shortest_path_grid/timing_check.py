# Small timing check for BFS / Dijkstra / A*
# Run: python timing_check.py

import time
from main import GridGraph, BFS, Dijkstra, AStar


def build_grid(n):
    grid = GridGraph(n, n)
    for r in range(n):
        for c in range(n):
            if (r + c) % 7 == 0 and (r, c) not in [(0, 0), (n - 1, n - 1)]:
                grid.set_cell(r, c, -1)
    # carve a guaranteed corridor: top row + rightmost column are open
    for c in range(n):
        grid.set_cell(0, c, 0)
    for r in range(n):
        grid.set_cell(r, n - 1, 0)
    return grid


def time_algo(algo_cls, grid, start, goal):
    pf = algo_cls(grid)
    t0 = time.perf_counter()
    path = pf.find_path(start, goal)
    elapsed = (time.perf_counter() - t0) * 1000
    return {
        "path_len": len(path) if path else None,
        "explored": pf.explored_nodes,
        "ms": elapsed,
    }


def run_sizes():
    for n in [10, 20, 30]:
        grid = build_grid(n)
        start, goal = (0, 0), (n - 1, n - 1)
        results = {}
        for name, cls in [("BFS", BFS), ("Dijkstra", Dijkstra), ("A*", AStar)]:
            results[name] = time_algo(cls, grid, start, goal)

        print(f"\nGrid {n}x{n}")
        for name in ["BFS", "Dijkstra", "A*"]:
            data = results[name]
            print(
                f"{name:9}  path={data['path_len']}  explored={data['explored']}  time={data['ms']:.2f}ms"
            )


if __name__ == "__main__":
    run_sizes()

