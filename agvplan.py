import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import json

class GridSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("码头AGV2D仿真环境")
        self.grid_size = 100
        self.cell_size = 6  # 每个格子为6x6像素
        self.canvas = tk.Canvas(master, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size)
        self.canvas.pack()

        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.agv_start = None
        self.agv_end = None

        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack()

        self.add_buttons()
        self.draw_grid()

        self.selected_action = None  # 当前选择的操作

    def add_buttons(self):
        tk.Button(self.buttons_frame, text="添加仓库", command=self.set_action_to_warehouse).grid(row=0, column=0)
        tk.Button(self.buttons_frame, text="添加障碍物", command=self.set_action_to_obstacle).grid(row=0, column=1)
        tk.Button(self.buttons_frame, text="添加吊机", command=self.set_action_to_crane).grid(row=0, column=2)
        tk.Button(self.buttons_frame, text="添加AGV起始点", command=self.set_action_to_agv_start).grid(row=0, column=3)
        tk.Button(self.buttons_frame, text="添加AGV终止点", command=self.set_action_to_agv_end).grid(row=0, column=4)
        tk.Button(self.buttons_frame, text="保存方格图", command=self.save_grid).grid(row=0, column=5)
        tk.Button(self.buttons_frame, text="加载方格图", command=self.load_grid).grid(row=0, column=6)
        tk.Button(self.buttons_frame, text="路径规划", command=self.path_planning).grid(row=0, column=7)

    def draw_grid(self):
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = "white"
                if self.grid[i, j] == 1:
                    color = "blue"  # 仓库
                elif self.grid[i, j] == 2:
                    color = "red"   # 障碍物
                elif self.grid[i, j] == 3:
                    color = "purple"  # 吊机
                elif self.grid[i, j] == 4:
                    color = "lightblue"  # AGV起始点
                elif self.grid[i, j] == 5:
                    color = "green"  # AGV终止点
                elif self.grid[i, j] == 6:
                    color = "yellow"  # 路径
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                              (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                              fill=color, outline="gray")

    def set_action_to_warehouse(self):
        self.selected_action = 'warehouse'
        messagebox.showinfo("提示", "你可以添加仓库了。")

    def set_action_to_obstacle(self):
        self.selected_action = 'obstacle'
        messagebox.showinfo("提示", "你可以添加障碍物了。")

    def set_action_to_crane(self):
        self.selected_action = 'crane'
        messagebox.showinfo("提示", "你可以添加吊机了。")

    def set_action_to_agv_start(self):
        self.selected_action = 'agv_start'
        messagebox.showinfo("提示", "你可以添加AGV起始点了。")

    def set_action_to_agv_end(self):
        self.selected_action = 'agv_end'
        messagebox.showinfo("提示", "你可以添加AGV终止点了。")

    def canvas_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.add_element((y, x))

    def add_element(self, pos):
        y, x = pos
        if self.grid[y, x] != 0:  # 检查是否已经有元素
            messagebox.showerror("错误", "该格子已被占用！")
            return
        
        if self.selected_action == 'warehouse':
            self.grid[y, x] = 1
        elif self.selected_action == 'obstacle':
            self.grid[y, x] = 2
        elif self.selected_action == 'crane':
            self.grid[y, x] = 3
        elif self.selected_action == 'agv_start':
            if self.agv_start is not None:
                messagebox.showerror("错误", "只能有一个AGV起始点！")
                return
            self.grid[y, x] = 4
            self.agv_start = (y, x)
        elif self.selected_action == 'agv_end':
            if self.agv_end is not None:
                messagebox.showerror("错误", "只能有一个AGV终止点！")
                return
            self.grid[y, x] = 5
            self.agv_end = (y, x)

        self.draw_grid()

    def save_grid(self):
        grid_name = filedialog.asksaveasfilename(defaultextension=".json", 
                                                    filetypes=[("JSON Files", "*.json")])
        if not grid_name or not grid_name.split("/")[-1].split(".")[0].isalpha():
            messagebox.showerror("错误", "请使用英文名称保存方格图！")
            return
        with open(grid_name, 'w') as f:
            json.dump(self.grid.tolist(), f)

    def load_grid(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        with open(file_path, 'r') as f:
            self.grid = np.array(json.load(f))
        self.draw_grid()

    def path_planning(self):
        if self.agv_start is None or self.agv_end is None:
            messagebox.showerror("错误", "请确保AGV起始点和终止点已设置！")
            return
        path = self.a_star(self.agv_start, self.agv_end)
        if path is not None:
            for (y, x) in path:
                self.grid[y, x] = 6  # 黄色路径
            self.draw_grid()
        else:
            messagebox.showinfo("结果", "没有找到路径！")

    def a_star(self, start, goal):
        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = min(open_set, key=lambda o: f_score.get(o, float('inf')))
            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            for neighbor in self.get_neighbors(current):
                if self.grid[neighbor] in [2, 3]:  # 障碍物和吊机不可通行
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                    open_set.add(neighbor)

        return None  # 没有路径

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (node[0] + dy, node[1] + dx)
            if 0 <= neighbor[0] < self.grid_size and 0 <= neighbor[1] < self.grid_size:
                neighbors.append(neighbor)
        return neighbors

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

if __name__ == "__main__":
    root = tk.Tk()
    app = GridSystem(root)
    app.canvas.bind("<Button-1>", app.canvas_click)  # 绑定点击事件
    root.mainloop()
