# Shortest Path on a Grid

This is our algorithms course project. We built a program that finds the shortest path on a grid using BFS, Dijkstra, and A\*.

## What it does

You get a grid where you can:

-   Draw walls by clicking
-   Pick a start point and goal point
-   The program finds the shortest path and shows it

## How to run

Just run main.py:

```
python main.py
```

A window will open with a grid.

## How to use the GUI

-   Left click on any cell to make it a wall (black) or remove the wall
-   Right click to set the start point (green)
-   Right click again to set the goal (red)
-   The path will show up in yellow

Buttons on the right:

-   Find Path: runs the selected algorithm
-   Clear Path: removes the yellow path
-   Clear All: resets everything
-   Load Example: loads a sample maze
-   Compare All: runs all 3 algorithms and shows how many nodes each one explored

## The algorithms

We implemented 3 algorithms from scratch (no heapq or built-in dict/set):

1. BFS - for grids where all cells have same cost
2. Dijkstra - for grids where some cells cost more to cross
3. A\* - like Dijkstra but uses a hint (Manhattan distance) to find the goal faster

## Files

-   main.py - the main program with algorithms and GUI
-   tests.py - unit tests to check if algorithms work
-   timing_check.py - measures how fast each algorithm runs on different grid sizes

## Running tests

```
python tests.py
```

Should say "OK" if everything works.

## Running timing check

```
python timing_check.py
```

Shows how many nodes each algorithm explores on 10x10, 20x20, 30x30 grids.

## What we learned

-   BFS is simple and works great for unweighted grids
-   Dijkstra handles weighted cells but explores a lot of nodes
-   A\* is the smartest - it explores way fewer nodes because it "knows" which direction the goal is

## Edge cases we handle

-   Walls blocking the path (goes around them)
-   Goal completely blocked (shows "unreachable")
-   Different grid sizes work fine

## Console mode

If you dont want the GUI, you can run:

```
python main.py --console
```

This prints the path as coordinates in the terminal.

---

Made for Algorithms course project.
