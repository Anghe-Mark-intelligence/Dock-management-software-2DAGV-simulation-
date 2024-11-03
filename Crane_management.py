import tkinter as tk
from tkinter import messagebox
import sqlite3

# 创建数据库和表
def create_db():
    conn = sqlite3.connect('crane_workers.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS workers (
            crane_id INTEGER PRIMARY KEY,
            worker_name TEXT NOT NULL,
            working_hours INTEGER NOT NULL,
            unloading_ship TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 插入数据
def add_worker():
    crane_id = entry_crane_id.get()
    worker_name = entry_worker_name.get()
    working_hours = entry_working_hours.get()
    unloading_ship = entry_unloading_ship.get()

    conn = sqlite3.connect('crane_workers.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO workers VALUES (?, ?, ?, ?)', (crane_id, worker_name, working_hours, unloading_ship))
        conn.commit()
        messagebox.showinfo("成功", "工人信息已添加")
    except sqlite3.IntegrityError:
        messagebox.showerror("错误", "吊机编号必须唯一")
    conn.close()

# 删除数据
def delete_worker():
    crane_id = entry_crane_id.get()

    conn = sqlite3.connect('crane_workers.db')
    c = conn.cursor()
    c.execute('DELETE FROM workers WHERE crane_id = ?', (crane_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("成功", "工人信息已删除")

# 更新数据
def update_worker():
    crane_id = entry_crane_id.get()
    worker_name = entry_worker_name.get()
    working_hours = entry_working_hours.get()
    unloading_ship = entry_unloading_ship.get()

    conn = sqlite3.connect('crane_workers.db')
    c = conn.cursor()
    c.execute('''
        UPDATE workers
        SET worker_name = ?, working_hours = ?, unloading_ship = ?
        WHERE crane_id = ?
    ''', (worker_name, working_hours, unloading_ship, crane_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("成功", "工人信息已更新")

# 查询数据
def query_worker():
    crane_id = entry_crane_id.get()

    conn = sqlite3.connect('crane_workers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM workers WHERE crane_id = ?', (crane_id,))
    worker = c.fetchone()
    conn.close()

    if worker:
        show_query_result(worker)
    else:
        messagebox.showerror("错误", "未找到工人信息")

# 弹出窗口显示查询结果
def show_query_result(worker):
    query_window = tk.Toplevel(root)
    query_window.title("查询结果")

    tk.Label(query_window, text="吊机编号:").grid(row=0, column=0)
    tk.Label(query_window, text=worker[0]).grid(row=0, column=1)

    tk.Label(query_window, text="工人姓名:").grid(row=1, column=0)
    tk.Label(query_window, text=worker[1]).grid(row=1, column=1)

    tk.Label(query_window, text="工作时间:").grid(row=2, column=0)
    tk.Label(query_window, text=worker[2]).grid(row=2, column=1)

    tk.Label(query_window, text="装卸货轮:").grid(row=3, column=0)
    tk.Label(query_window, text=worker[3]).grid(row=3, column=1)

    tk.Button(query_window, text="关闭", command=query_window.destroy).grid(row=4, columnspan=2)

# 创建窗口
root = tk.Tk()
root.title("吊机工人管理系统")

# 输入框
tk.Label(root, text="吊机编号").grid(row=0, column=0)
entry_crane_id = tk.Entry(root)
entry_crane_id.grid(row=0, column=1)

tk.Label(root, text="工人姓名").grid(row=1, column=0)
entry_worker_name = tk.Entry(root)
entry_worker_name.grid(row=1, column=1)

tk.Label(root, text="工作时间").grid(row=2, column=0)
entry_working_hours = tk.Entry(root)
entry_working_hours.grid(row=2, column=1)

tk.Label(root, text="装卸货轮").grid(row=3, column=0)
entry_unloading_ship = tk.Entry(root)
entry_unloading_ship.grid(row=3, column=1)

# 按钮
tk.Button(root, text="添加", command=add_worker).grid(row=4, column=0)
tk.Button(root, text="删除", command=delete_worker).grid(row=4, column=1)
tk.Button(root, text="更新", command=update_worker).grid(row=4, column=2)
tk.Button(root, text="查询", command=query_worker).grid(row=4, column=3)

create_db()
root.mainloop()
