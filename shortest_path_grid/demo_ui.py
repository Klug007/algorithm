"""
Demo Application: Interactive Grid Pathfinding with Tkinter UI
Allows clicking to set start/goal, visualizes paths, and compares algorithms.
"""

import tkinter as tk
from tkinter import messagebox
from grid_graph import GridGraph
from pathfinding import BFS, Dijkstra, AStar
import time


class GridUI:
    """Interactive grid UI for pathfinding visualization."""
    
    CELL_SIZE = 30
    COLORS = {
        'empty': 'white',
        'wall': 'black',
        'weighted': 'lightgray',
        'start': 'green',
        'goal': 'red',
        'path': 'yellow',
        'explored': 'lightblue'
    }
    
    def __init__(self, width=15, height=15):
        """Initialize UI."""
        self.grid = GridGraph(width, height)
        self.width = width
        self.height = height
        self.start = None
        self.goal = None
        self.current_path = None
        self.current_algorithm = 'BFS'
        
        # Create window
        self.root = tk.Tk()
        self.root.title("Shortest Path on Grid - BFS/Dijkstra/A*")
        
        # Create canvas
        canvas_width = width * self.CELL_SIZE
        canvas_height = height * self.CELL_SIZE
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_width,
            height=canvas_height,
            bg='white'
        )
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        self.canvas.bind('<Button-3>', self.on_canvas_right_click)
        
        # Create control panel
        self.create_control_panel()
        
        # Draw grid
        self.draw_grid()
    
    def create_control_panel(self):
        """Create control panel with buttons and info."""
        panel = tk.Frame(self.root)
        panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(panel, text="Path Finder Control", font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Instructions
        instructions = tk.Text(panel, height=8, width=30, wrap=tk.WORD)
        instructions.pack(pady=10)
        instructions.insert(tk.END, 
            "Left Click: Toggle walls\n"
            "Right Click: Set start (first), goal (second)\n"
            "\n"
            "Green = Start\n"
            "Red = Goal\n"
            "Yellow = Path\n"
            "Black = Wall"
        )
        instructions.config(state=tk.DISABLED)
        
        # Algorithm selection
        tk.Label(panel, text="Algorithm:", font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        
        algo_frame = tk.Frame(panel)
        algo_frame.pack(pady=5)
        
        for algo in ['BFS', 'Dijkstra', 'A*']:
            tk.Radiobutton(
                algo_frame,
                text=algo,
                variable=tk.StringVar(value='BFS'),
                value=algo,
                command=lambda a=algo: self.set_algorithm(a)
            ).pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(panel)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Find Path", command=self.find_path, bg='lightgreen').pack(pady=5)
        tk.Button(button_frame, text="Clear Path", command=self.clear_path, bg='lightyellow').pack(pady=5)
        tk.Button(button_frame, text="Clear All", command=self.clear_all, bg='lightcoral').pack(pady=5)
        tk.Button(button_frame, text="Load Example", command=self.load_example, bg='lightblue').pack(pady=5)
        tk.Button(button_frame, text="Compare Algorithms", command=self.compare_algorithms, bg='plum').pack(pady=5)
        
        # Info display
        self.info_label = tk.Label(panel, text="", justify=tk.LEFT, font=('Courier', 9))
        self.info_label.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Complexity info
        complexity_frame = tk.LabelFrame(panel, text="Algorithm Complexity", font=('Arial', 9, 'bold'))
        complexity_frame.pack(pady=10, fill=tk.BOTH)
        
        complexity_text = tk.Text(complexity_frame, height=6, width=28, wrap=tk.WORD)
        complexity_text.pack(padx=5, pady=5)
        complexity_text.insert(tk.END,
            "BFS:\nTime: O(V+E)\nSpace: O(V)\n\n"
            "Dijkstra:\nTime: O((V+E)log V)\nSpace: O(V)\n\n"
            "A*:\nTime: O((V+E)log V)\nSpace: O(V)"
        )
        complexity_text.config(state=tk.DISABLED)
    
    def set_algorithm(self, algo):
        """Set current algorithm."""
        self.current_algorithm = algo
        self.clear_path()
    
    def draw_grid(self):
        """Draw the grid and all elements."""
        self.canvas.delete("all")
        
        # Draw cells
        for row in range(self.height):
            for col in range(self.width):
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                # Determine color
                if self.start and (row, col) == self.start:
                    color = self.COLORS['start']
                elif self.goal and (row, col) == self.goal:
                    color = self.COLORS['goal']
                elif self.current_path and (row, col) in self.current_path:
                    color = self.COLORS['path']
                elif self.grid.get_cell(row, col) == -1:
                    color = self.COLORS['wall']
                elif self.grid.get_cell(row, col) > 0:
                    color = self.COLORS['weighted']
                else:
                    color = self.COLORS['empty']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
    
    def on_canvas_click(self, event):
        """Handle left click - toggle walls."""
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if 0 <= row < self.height and 0 <= col < self.width:
            cell = self.grid.get_cell(row, col)
            if cell == -1:
                self.grid.set_cell(row, col, 0)
            else:
                self.grid.set_cell(row, col, -1)
            self.clear_path()
            self.draw_grid()
    
    def on_canvas_right_click(self, event):
        """Handle right click - set start/goal."""
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if 0 <= row < self.height and 0 <= col < self.width:
            if not self.start:
                self.start = (row, col)
            elif not self.goal:
                self.goal = (row, col)
                self.find_path()
            else:
                self.start = (row, col)
                self.goal = None
            self.draw_grid()
    
    def find_path(self):
        """Find and display path."""
        if not self.start or not self.goal:
            messagebox.showwarning("Info", "Set both start and goal")
            return
        
        # Select algorithm
        if self.current_algorithm == 'BFS':
            pathfinder = BFS(self.grid)
        elif self.current_algorithm == 'Dijkstra':
            pathfinder = Dijkstra(self.grid)
        else:  # A*
            pathfinder = AStar(self.grid)
        
        # Find path
        start_time = time.time()
        self.current_path = pathfinder.find_path(self.start, self.goal)
        elapsed = time.time() - start_time
        
        # Update info
        if self.current_path:
            info = f"Algorithm: {self.current_algorithm}\n"
            info += f"Path length: {len(self.current_path)} cells\n"
            info += f"Distance: {len(self.current_path) - 1} steps\n"
            info += f"Nodes explored: {pathfinder.explored_nodes}\n"
            info += f"Time: {elapsed*1000:.2f} ms"
        else:
            info = f"Algorithm: {self.current_algorithm}\n"
            info += "Goal unreachable!\n"
            info += f"Nodes explored: {pathfinder.explored_nodes}\n"
            info += f"Time: {elapsed*1000:.2f} ms"
        
        self.info_label.config(text=info)
        self.draw_grid()
    
    def clear_path(self):
        """Clear current path."""
        self.current_path = None
        self.info_label.config(text="")
        self.draw_grid()
    
    def clear_all(self):
        """Clear everything."""
        self.grid = GridGraph(self.width, self.height)
        self.start = None
        self.goal = None
        self.current_path = None
        self.info_label.config(text="")
        self.draw_grid()
    
    def load_example(self):
        """Load an example maze."""
        self.clear_all()
        
        # Create a maze with walls
        # Vertical walls
        for row in range(self.height):
            if row != self.height // 2:
                self.grid.set_cell(row, self.width // 3, -1)
                self.grid.set_cell(row, 2 * self.width // 3, -1)
        
        # Horizontal walls
        for col in range(self.width):
            if col != self.width // 2:
                self.grid.set_cell(self.height // 3, col, -1)
        
        # Set start and goal
        self.start = (0, 0)
        self.goal = (self.height - 1, self.width - 1)
        
        self.draw_grid()
    
    def compare_algorithms(self):
        """Compare all three algorithms."""
        if not self.start or not self.goal:
            messagebox.showwarning("Info", "Set both start and goal")
            return
        
        results = {}
        
        for algo_name in ['BFS', 'Dijkstra', 'A*']:
            if algo_name == 'BFS':
                pathfinder = BFS(self.grid)
            elif algo_name == 'Dijkstra':
                pathfinder = Dijkstra(self.grid)
            else:
                pathfinder = AStar(self.grid)
            
            start_time = time.time()
            path = pathfinder.find_path(self.start, self.goal)
            elapsed = time.time() - start_time
            
            results[algo_name] = {
                'path_length': len(path) if path else 'N/A',
                'nodes_explored': pathfinder.explored_nodes,
                'time': elapsed * 1000
            }
        
        # Display results
        info = "Algorithm Comparison:\n\n"
        for algo, data in results.items():
            info += f"{algo}:\n"
            info += f"  Path: {data['path_length']}\n"
            info += f"  Explored: {data['nodes_explored']}\n"
            info += f"  Time: {data['time']:.2f}ms\n\n"
        
        self.info_label.config(text=info)
    
    def run(self):
        """Run the UI."""
        self.root.mainloop()


if __name__ == '__main__':
    app = GridUI(width=15, height=15)
    app.run()
