# Project Requirements

## Python Version

-   Python 3.7 or higher

## Core Dependencies (Built-in)

-   `collections.deque` - For BFS queue
-   `heapq` - For priority queue (Dijkstra, A\*)
-   `typing` - Type hints
-   `time` - Performance measurement
-   `tkinter` - GUI (usually comes with Python)

## Optional Dependencies

-   `matplotlib` - For complexity analysis graphs
    ```bash
    pip install matplotlib
    ```

## Installation

### Option 1: No external dependencies needed (core only)

Just Python 3.7+ is required. All algorithms work with built-in modules.

### Option 2: Full installation with visualization

```bash
pip install matplotlib
```

## Verification

Test that everything is installed correctly:

```bash
# Test Python version
python --version

# Test tkinter
python -c "import tkinter; print('tkinter OK')"

# Test matplotlib (optional)
python -c "import matplotlib; print('matplotlib OK')"

# Run quick demo to verify
python quick_demo.py
```

## Project Files

### Core Implementation (2 files)

-   `grid_graph.py` - Grid representation, no external dependencies
-   `pathfinding.py` - Algorithms, uses only standard library

### Testing & Demos (3 files)

-   `test_pathfinding.py` - Unit tests, standard library only
-   `quick_demo.py` - Command-line demos, standard library only
-   `demo_ui.py` - Interactive UI, requires tkinter

### Analysis & Documentation (3 files)

-   `complexity_analysis.py` - Performance analysis, requires matplotlib
-   `README.md` - Technical documentation
-   `PRESENTATION_NOTES.md` - Presentation content

## System Requirements

### Minimum

-   Python 3.7+
-   50 MB disk space
-   100 MB RAM

### Recommended

-   Python 3.9+
-   100 MB disk space
-   200 MB RAM
-   matplotlib for graphs

### Tested On

-   Windows 10/11
-   macOS 10.14+
-   Linux (Ubuntu 18.04+)

## Running Different Modules

### No Dependencies Required

```bash
# All of these work with standard Python only
python quick_demo.py
python test_pathfinding.py
python -c "from grid_graph import GridGraph; from pathfinding import BFS; print('OK')"
```

### Requires tkinter

```bash
python demo_ui.py  # Interactive UI
```

### Requires matplotlib

```bash
python complexity_analysis.py  # Performance graphs
```

## Troubleshooting

### Python not found

-   Install Python from python.org
-   Add Python to PATH

### tkinter not found

```bash
# Windows
# Reinstall Python, ensure "tcl/tk and IDLE" is selected

# macOS
# brew install python-tk

# Linux
# Ubuntu/Debian: sudo apt-get install python3-tk
# Fedora: sudo dnf install python3-tkinter
```

### matplotlib import error

```bash
pip install --upgrade matplotlib
```

### Permission denied on Linux/macOS

```bash
chmod +x *.py
python3 instead of python
```

## File Size & Performance

-   Code: ~2,160 lines of Python
-   Tests: ~450 lines (24 unit tests)
-   Complexity: O(V + E) to O((V+E) log V) depending on algorithm
-   Memory: O(V) for all algorithms
-   Grid size: Tested up to 100×100, limited by RAM

## Compatibility Notes

-   All code is Python 3.7+ compatible
-   No Python 2.x support
-   tkinter may have issues on some Linux distributions (install tk separately)
-   matplotlib version 3.0+ recommended for graphs
