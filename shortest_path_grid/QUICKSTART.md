# Quick Start Guide

## Installation & Setup

### Requirements

-   Python 3.7+
-   tkinter (comes with Python by default)
-   matplotlib (optional, for complexity graphs)

### Install matplotlib (optional)

```bash
pip install matplotlib
```

---

## Running the Project

### 1. Quick Demo (2-3 minutes)

See all algorithms in action with different scenarios:

```bash
python quick_demo.py
```

**Output**:

-   5 different test cases
-   Path visualization
-   Algorithm comparison
-   Time measurements

---

### 2. Interactive UI (Play with algorithms)

Real-time visualization and experimentation:

```bash
python demo_ui.py
```

**Controls**:

-   **Left Click on Grid**: Toggle walls (black)
-   **Right Click on Grid**: Set start point (green), then goal (red)
-   **Find Path Button**: Show shortest path (yellow)
-   **Algorithm Selection**: Choose BFS, Dijkstra, or A\*
-   **Load Example**: Pre-made maze for testing
-   **Compare Algorithms**: See performance on current grid

---

### 3. Unit Tests (Verify correctness)

Run all 24 tests to verify algorithms work correctly:

```bash
python test_pathfinding.py -v
```

**Tests Cover**:

-   Grid operations
-   Algorithm correctness
-   Edge cases (unreachable goals, walls, etc.)
-   Performance comparisons

**Expected**: All 24 tests pass ✓

---

### 4. Complexity Analysis (Generate graphs)

Empirical performance measurement with visualization:

```bash
python complexity_analysis.py
```

**Output**:

-   Performance table (grid size vs time)
-   Obstacle density impact
-   Node exploration efficiency
-   Graphs saved as `complexity_analysis.png`

---

## File Overview

| File                     | Purpose             | Key Classes                |
| ------------------------ | ------------------- | -------------------------- |
| `grid_graph.py`          | Grid representation | `GridGraph`                |
| `pathfinding.py`         | Algorithms          | `BFS`, `Dijkstra`, `AStar` |
| `test_pathfinding.py`    | Unit tests          | 6 test classes, 24 tests   |
| `demo_ui.py`             | Interactive UI      | `GridUI`                   |
| `quick_demo.py`          | Command-line demos  | 5 demo functions           |
| `complexity_analysis.py` | Performance testing | `ComplexityAnalyzer`       |
| `README.md`              | Full documentation  | Technical details          |
| `PRESENTATION_NOTES.md`  | Presentation slides | 20 slides worth of content |

---

## Understanding the Algorithms

### BFS (Breadth-First Search)

```
✓ Use: Unweighted grids
✓ Guarantee: Shortest path
✓ Speed: O(V + E)
✗ Complex: No
```

### Dijkstra's Algorithm

```
✓ Use: Weighted grids
✓ Guarantee: Shortest path (non-negative weights)
✓ Speed: O((V+E) log V)
? Complex: Yes, uses priority queue
```

### A\* Algorithm

```
✓ Use: Large grids, fast pathfinding
✓ Guarantee: Shortest path (with admissible heuristic)
✓ Speed: O((V+E) log V) typical, much faster than Dijkstra
✓ Complex: Most complex, but fastest in practice
```

---

## Example: Using the Code Directly

```python
from grid_graph import GridGraph
from pathfinding import BFS, Dijkstra, AStar

# Create a 10x10 grid
grid = GridGraph(10, 10)

# Add some walls
grid.set_cell(5, 5, -1)  # -1 = wall
grid.set_cell(5, 6, -1)
grid.set_cell(5, 7, -1)

# Find path using BFS
bfs = BFS(grid)
path = bfs.find_path((0, 0), (9, 9))

print(f"Path: {path}")
print(f"Length: {len(path)} cells")
print(f"Nodes explored: {bfs.explored_nodes}")
```

---

## Common Issues & Solutions

### Issue: `ModuleNotFoundError` for matplotlib

**Solution**: This is optional. Code works without it.

```bash
pip install matplotlib
```

### Issue: Tkinter not found (demo_ui.py)

**Solution**: Tkinter comes with Python. Reinstall Python or:

```bash
# Linux
sudo apt-get install python3-tk

# macOS
# Should be included with Python
```

### Issue: Path not found for valid grid

**Check**:

1. Start point is not a wall
2. Goal point is not isolated
3. There's actually a path between them
4. Try the "Load Example" feature first

---

## Performance Tips

### For Large Grids (> 50×50):

-   Use **A\*** for fastest results
-   Avoid Dijkstra if all cells have same cost (use BFS instead)
-   Keep obstacles to < 50% for reasonable performance

### For Real-time Applications:

-   Pre-compute frequently-used paths
-   Use A\* with Manhattan heuristic
-   Cache grid information

### For Accuracy:

-   Use **Dijkstra** for weighted grids where correctness is critical
-   A\* is equally correct but faster

---

## What to Show in Presentation

### 5-Minute Overview

1. **Problem**: Shortest path on grid (1 min)
2. **Algorithms**: BFS, Dijkstra, A\* (2 min)
3. **Demo**: Run quick_demo.py (1 min)
4. **Results**: Show performance comparison (1 min)

### 10-Minute Detailed Presentation

1. Problem statement and motivation (1 min)
2. Grid graph representation (1.5 min)
3. Algorithm explanations with pseudocode (3 min)
4. Interactive demo (2 min)
5. Test results and edge cases (1.5 min)
6. Performance analysis and conclusion (1 min)

### Interactive Demo (5-10 min)

1. Open demo_ui.py
2. Left-click to create maze
3. Right-click to set start/goal
4. Switch algorithms and show path changes
5. Compare performance with "Compare Algorithms" button
6. Show that A\* explores fewer nodes

---

## Test Examples

### Test 1: Simple Open Grid

```
Grid: 5x5, all empty
Start: (0,0), Goal: (4,4)
Expected: 9-cell path (diagonal movement would be 5)
All algorithms: Find optimal path
```

### Test 2: Maze Navigation

```
Grid: 8x8 with vertical walls and gap
Expected: Path navigates through gap
All algorithms: Find path, different node exploration counts
A*: Explores ~50% fewer nodes
```

### Test 3: Unreachable Goal

```
Grid: Goal surrounded by walls
Expected: All return None
Behavior: Explore all reachable cells then give up
```

---

## Complexity Summary

| Aspect           | BFS    | Dijkstra      | A\*           |
| ---------------- | ------ | ------------- | ------------- |
| Time             | O(V+E) | O((V+E)log V) | O((V+E)log V) |
| Space            | O(V)   | O(V)          | O(V)          |
| Nodes Explored   | All    | Many          | Few           |
| Weighted Support | No     | Yes           | Yes           |
| Optimality       | ✓      | ✓             | ✓             |

---

## Next Steps

1. **Run quick_demo.py** to see everything work
2. **Run test_pathfinding.py** to verify correctness
3. **Open demo_ui.py** to experiment interactively
4. **Review README.md** for technical details
5. **Check PRESENTATION_NOTES.md** for presentation content

---

## Project Highlights

✅ **Complete Implementation** - All algorithms from scratch  
✅ **Comprehensive Testing** - 24 unit tests covering edge cases  
✅ **Interactive UI** - Real-time visualization  
✅ **Performance Analysis** - Empirical complexity verification  
✅ **Well Documented** - README, presentation notes, code comments

---

## Questions?

Check README.md for detailed technical documentation or PRESENTATION_NOTES.md for presentation-focused content.
