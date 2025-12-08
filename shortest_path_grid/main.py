# Shortest path on a grid (BFS, Dijkstra, A*)
# Draw walls, pick start/goal, see the path

import tkinter as tk
from tkinter import messagebox
import time


# Grid storage: 0 empty, -1 wall, >0 cost

class GridGraph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    def set_cell(self, row, col, value):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = value
    
    def get_cell(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None
    
    def is_walkable(self, row, col):
        cell = self.get_cell(row, col)
        return cell is not None and cell != -1
    
    def get_neighbors(self, row, col):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if self.is_walkable(new_row, new_col):
                neighbors.append((new_row, new_col))
        return neighbors
    
    def get_cost(self, row, col):
        cell = self.get_cell(row, col)
        if cell is None:
            return 0
        if cell == 0:
            return 1
        elif cell > 0:
            return cell
        return 0


# Base pathfinder helpers

class PathFinder:
    def __init__(self, grid_graph):
        self.grid = grid_graph
        self.width = grid_graph.width
        self.height = grid_graph.height
        self.size = self.width * self.height
        self.explored_nodes = 0

    def index(self, row, col):
        return row * self.width + col

    def pos(self, idx):
        return divmod(idx, self.width)

    def reconstruct_path(self, parent, start_idx, goal_idx):
        path = []
        current = goal_idx
        while current != -1:
            path.append(self.pos(current))
            if current == start_idx:
                break
            current = parent[current]
        if not path or current == -1:
            return None
        path.reverse()
        return path


class MinHeap:
    # small min-heap for (priority, item)
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def push(self, priority, item):
        self.data.append((priority, item))
        self._bubble_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            return None, None
        self._swap(0, len(self.data) - 1)
        priority, item = self.data.pop()
        if self.data:
            self._bubble_down(0)
        return priority, item

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _bubble_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.data[parent][0] <= self.data[idx][0]:
                break
            self._swap(parent, idx)
            idx = parent

    def _bubble_down(self, idx):
        n = len(self.data)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < n and self.data[left][0] < self.data[smallest][0]:
                smallest = left
            if right < n and self.data[right][0] < self.data[smallest][0]:
                smallest = right
            if smallest == idx:
                break
            self._swap(idx, smallest)
            idx = smallest


# BFS: unweighted shortest path

class BFS(PathFinder):
    def find_path(self, start, goal):
        if not self.grid.is_walkable(*start) or not self.grid.is_walkable(*goal):
            return None

        self.explored_nodes = 0
        visited = [False] * self.size
        parent = [-1] * self.size

        start_idx = self.index(*start)
        goal_idx = self.index(*goal)

        queue = [start_idx]
        visited[start_idx] = True
        head = 0

        while head < len(queue):
            current_idx = queue[head]
            head += 1
            self.explored_nodes += 1

            if current_idx == goal_idx:
                return self.reconstruct_path(parent, start_idx, goal_idx)

            row, col = self.pos(current_idx)
            for n_row, n_col in self.grid.get_neighbors(row, col):
                n_idx = self.index(n_row, n_col)
                if not visited[n_idx]:
                    visited[n_idx] = True
                    parent[n_idx] = current_idx
                    queue.append(n_idx)

        return None


# Dijkstra: handles weights

class Dijkstra(PathFinder):
    def find_path(self, start, goal):
        if not self.grid.is_walkable(*start) or not self.grid.is_walkable(*goal):
            return None

        self.explored_nodes = 0
        start_idx = self.index(*start)
        goal_idx = self.index(*goal)

        dist = [float('inf')] * self.size
        parent = [-1] * self.size
        visited = [False] * self.size

        dist[start_idx] = 0
        heap = MinHeap()
        heap.push(0, start_idx)

        while len(heap):
            current_dist, current_idx = heap.pop()
            if current_idx is None:
                break
            if visited[current_idx]:
                continue

            visited[current_idx] = True
            self.explored_nodes += 1

            if current_idx == goal_idx:
                return self.reconstruct_path(parent, start_idx, goal_idx)

            if current_dist > dist[current_idx]:
                continue

            row, col = self.pos(current_idx)
            for n_row, n_col in self.grid.get_neighbors(row, col):
                n_idx = self.index(n_row, n_col)
                if visited[n_idx]:
                    continue

                cost = self.grid.get_cost(n_row, n_col)
                new_dist = current_dist + cost

                if new_dist < dist[n_idx]:
                    dist[n_idx] = new_dist
                    parent[n_idx] = current_idx
                    heap.push(new_dist, n_idx)

        return None


# A*: uses manhattan hint to be faster

class AStar(PathFinder):
    def manhattan(self, pos, goal):
        # simple estimate: just add up horizontal + vertical distance
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
    
    def find_path(self, start, goal):
        if not self.grid.is_walkable(*start) or not self.grid.is_walkable(*goal):
            return None
        
        self.explored_nodes = 0
        start_idx = self.index(*start)
        goal_idx = self.index(*goal)

        g_scores = [float('inf')] * self.size  # actual cost from start
        parent = [-1] * self.size
        visited = [False] * self.size

        g_scores[start_idx] = 0

        heap = MinHeap()
        heap.push(self.manhattan(start, goal), start_idx)
        
        while len(heap):
            f_score, current_idx = heap.pop()
            if current_idx is None:
                break

            if visited[current_idx]:
                continue
            
            visited[current_idx] = True
            self.explored_nodes += 1
            
            if current_idx == goal_idx:
                return self.reconstruct_path(parent, start_idx, goal_idx)
            
            row, col = self.pos(current_idx)
            for n_row, n_col in self.grid.get_neighbors(row, col):
                n_idx = self.index(n_row, n_col)
                if visited[n_idx]:
                    continue

                cost = self.grid.get_cost(n_row, n_col)
                tentative_g = g_scores[current_idx] + cost
                
                if tentative_g < g_scores[n_idx]:
                    g_scores[n_idx] = tentative_g
                    parent[n_idx] = current_idx
                    f = tentative_g + self.manhattan((n_row, n_col), goal)
                    heap.push(f, n_idx)
        
        return None


# GUI: click to add walls, right click for start/goal

class GridUI:
    CELL_SIZE = 30
    
    COLORS = {
        'empty': 'white',
        'wall': 'black',
        'weighted': 'lightgray',
        'start': 'green',
        'goal': 'red',
        'path': 'yellow',
    }
    
    def __init__(self, width=15, height=15):
        self.grid = GridGraph(width, height)
        self.width = width
        self.height = height
        self.start = None
        self.goal = None
        self.current_path = None
        self.current_algorithm = 'BFS'
        
        self.root = tk.Tk()
        self.root.title("Shortest Path on Grid")
        
        canvas_width = width * self.CELL_SIZE
        canvas_height = height * self.CELL_SIZE
        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas.bind('<Button-1>', self.on_left_click)   # left click = walls
        self.canvas.bind('<Button-3>', self.on_right_click)  # right click = start/goal
        
        self.create_panel()
        self.draw_grid()
    
    def create_panel(self):
        panel = tk.Frame(self.root)
        panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH)
        
        tk.Label(panel, text="Controls", font=('Arial', 14, 'bold')).pack(pady=10)
        
        info = tk.Text(panel, height=6, width=28)
        info.pack(pady=10)
        info.insert(tk.END, "Left Click: Toggle wall\nRight Click: Set start/goal\n\nGreen = Start\nRed = Goal\nYellow = Path")
        info.config(state=tk.DISABLED)
        
        tk.Label(panel, text="Algorithm:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.algo_var = tk.StringVar(value='BFS')
        for algo in ['BFS', 'Dijkstra', 'A*']:
            tk.Radiobutton(panel, text=algo, variable=self.algo_var, value=algo,
                          command=lambda a=algo: self.set_algorithm(a)).pack(anchor=tk.W)
        
        tk.Button(panel, text="Find Path", command=self.find_path, bg='lightgreen').pack(pady=5)
        tk.Button(panel, text="Clear Path", command=self.clear_path, bg='lightyellow').pack(pady=5)
        tk.Button(panel, text="Clear All", command=self.clear_all, bg='lightcoral').pack(pady=5)
        tk.Button(panel, text="Load Example", command=self.load_example, bg='lightblue').pack(pady=5)
        tk.Button(panel, text="Compare All", command=self.compare_algorithms, bg='plum').pack(pady=5)
        
        self.info_label = tk.Label(panel, text="", justify=tk.LEFT, font=('Courier', 9))
        self.info_label.pack(pady=10)
        
        comp_frame = tk.LabelFrame(panel, text="Complexity")
        comp_frame.pack(pady=10, fill=tk.BOTH)
        comp_text = tk.Text(comp_frame, height=5, width=25)
        comp_text.pack(padx=5, pady=5)
        comp_text.insert(tk.END, "BFS: O(V+E)\nDijkstra: O((V+E)logV)\nA*: O((V+E)logV)")
        comp_text.config(state=tk.DISABLED)
    
    def set_algorithm(self, algo):
        self.current_algorithm = algo
        self.clear_path()
    
    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.height):
            for col in range(self.width):
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                if self.start and (row, col) == self.start:
                    color = self.COLORS['start']
                elif self.goal and (row, col) == self.goal:
                    color = self.COLORS['goal']
                elif self.current_path and (row, col) in self.current_path:
                    color = self.COLORS['path']
                elif self.grid.get_cell(row, col) == -1:
                    color = self.COLORS['wall']
                elif (self.grid.get_cell(row, col) or 0) > 0:
                    color = self.COLORS['weighted']
                else:
                    color = self.COLORS['empty']
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
    
    def on_left_click(self, event):
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if 0 <= row < self.height and 0 <= col < self.width:
            cell = self.grid.get_cell(row, col)
            self.grid.set_cell(row, col, 0 if cell == -1 else -1)
            self.clear_path()
            self.draw_grid()
    
    def on_right_click(self, event):
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
        if not self.start or not self.goal:
            messagebox.showwarning("Warning", "Set start and goal first")
            return
        
        if self.current_algorithm == 'BFS':
            pf = BFS(self.grid)
        elif self.current_algorithm == 'Dijkstra':
            pf = Dijkstra(self.grid)
        else:
            pf = AStar(self.grid)
        
        t0 = time.time()
        self.current_path = pf.find_path(self.start, self.goal)
        elapsed = (time.time() - t0) * 1000
        
        if self.current_path:
            info = f"Algorithm: {self.current_algorithm}\n"
            info += f"Path: {len(self.current_path)} cells\n"
            info += f"Explored: {pf.explored_nodes}\n"
            info += f"Time: {elapsed:.2f} ms"
        else:
            info = f"Algorithm: {self.current_algorithm}\n"
            info += "Goal unreachable!\n"
            info += f"Explored: {pf.explored_nodes}\n"
            info += f"Time: {elapsed:.2f} ms"
        
        self.info_label.config(text=info)
        self.draw_grid()
    
    def clear_path(self):
        self.current_path = None
        self.info_label.config(text="")
        self.draw_grid()
    
    def clear_all(self):
        self.grid = GridGraph(self.width, self.height)
        self.start = None
        self.goal = None
        self.current_path = None
        self.info_label.config(text="")
        self.draw_grid()
    
    def load_example(self):
        self.clear_all()
        
        for row in range(self.height):
            if row != self.height // 2:
                self.grid.set_cell(row, self.width // 3, -1)
                self.grid.set_cell(row, 2 * self.width // 3, -1)
        
        for col in range(self.width):
            if col != self.width // 2:
                self.grid.set_cell(self.height // 3, col, -1)
        
        self.start = (0, 0)
        self.goal = (self.height - 1, self.width - 1)
        self.draw_grid()
    
    def compare_algorithms(self):
        if not self.start or not self.goal:
            messagebox.showwarning("Warning", "Set start and goal first")
            return
        
        results = {}
        for name, cls in [('BFS', BFS), ('Dijkstra', Dijkstra), ('A*', AStar)]:
            pf = cls(self.grid)
            t0 = time.time()
            path = pf.find_path(self.start, self.goal)
            elapsed = (time.time() - t0) * 1000
            results[name] = {
                'path': len(path) if path else 'N/A',
                'explored': pf.explored_nodes,
                'time': elapsed
            }
        
        info = "Comparison:\n\n"
        for name, data in results.items():
            info += f"{name}:\n"
            info += f"  Path: {data['path']}\n"
            info += f"  Explored: {data['explored']}\n"
            info += f"  Time: {data['time']:.2f}ms\n\n"
        
        self.info_label.config(text=info)
    
    def run(self):
        self.root.mainloop()


# Console demo if you don't want the GUI

def console_demo():
    print("=" * 50)
    print("SHORTEST PATH ALGORITHMS DEMO")
    print("=" * 50)
    
    grid = GridGraph(8, 8)
    for row in range(8):
        if row != 3 and row != 4:
            grid.set_cell(row, 3, -1)
    
    start = (0, 0)
    goal = (0, 7)
    
    print("\nGrid (. = empty, # = wall):")
    for row in grid.grid:
        print(' '.join('#' if c == -1 else '.' for c in row))
    
    print(f"\nStart: {start}")
    print(f"Goal: {goal}")
    
    for name, cls in [('BFS', BFS), ('Dijkstra', Dijkstra), ('A*', AStar)]:
        pf = cls(grid)
        path = pf.find_path(start, goal)
        print(f"\n{name}:")
        if path:
            print(f"  Path: {path}")
            print(f"  Length: {len(path)}")
            print(f"  Explored: {pf.explored_nodes}")
        else:
            print("  No path found")


# Main entry: --console for text mode, else GUI

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        console_demo()
    else:
        app = GridUI(15, 15)
        app.run()

