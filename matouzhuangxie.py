import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# 生成模拟数据
def generate_data(num_samples=100):
    loading_times = np.random.uniform(1, 10, num_samples)  # 装卸时间，1到10小时之间
    efficiencies = 2 * loading_times + np.random.normal(0, 1, num_samples)  # 装卸效率，线性关系加上一些噪声
    return loading_times, efficiencies

# 生成100个样本的模拟数据
X, y = generate_data(100)

# 创建线性回归模型并训练
model = LinearRegression()
model.fit(X.reshape(-1, 1), y)

# 计算模型评估指标
predictions = model.predict(X.reshape(-1, 1))
r2 = r2_score(y, predictions)
mse = mean_squared_error(y, predictions)
coefficients = model.coef_[0]
intercept = model.intercept_

# 创建图形用户界面
def predict_efficiency():
    try:
        time = float(entry_time.get())
        efficiency = model.predict(np.array([[time]]))[0]
        messagebox.showinfo("预测结果", f"预计装卸效率: {efficiency:.2f} 货物件数")
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的数字")

app = tk.Tk()
app.title("码头装卸效率模拟器")
app.geometry("800x700")  # 设置窗口大小

# 加载背景图像并设置透明度
background_image_path = 'C:\\Users\\Administrator\\Desktop\\hongweihuang_system\\matou1.png'
background_image = Image.open(background_image_path).convert("RGBA")

# 设置60%透明度
alpha = int(255 * 0.6)  # 60% opacity
alpha_channel = Image.new("L", background_image.size, alpha)
background_image.putalpha(alpha_channel)

bg_label = tk.Label(app, image=ImageTk.PhotoImage(background_image))
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# 输入装卸时间
label_time = tk.Label(app, text="输入装卸时间（小时）：", bg='white')
label_time.pack(pady=10)

entry_time = tk.Entry(app)
entry_time.pack(pady=10)

# 预测按钮
predict_button = tk.Button(app, text="预测装卸效率", command=predict_efficiency)
predict_button.pack(pady=20)

# 创建左侧数据表
left_frame = tk.Frame(app)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

label_data = tk.Label(left_frame, text="模拟数据", font=("Arial", 14))
label_data.pack()

tree_data = ttk.Treeview(left_frame, columns=("装卸时间", "装卸效率"), show='headings')
tree_data.heading("装卸时间", text="装卸时间")
tree_data.heading("装卸效率", text="装卸效率")
tree_data.pack()

for time, efficiency in zip(X, y):
    tree_data.insert("", tk.END, values=(time, efficiency))

# 创建右侧模型评估表
right_frame = tk.Frame(app)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)

label_metrics = tk.Label(right_frame, text="模型评估指标", font=("Arial", 14))
label_metrics.pack()

tree_metrics = ttk.Treeview(right_frame, columns=("参数", "值"), show='headings')
tree_metrics.heading("参数", text="参数")
tree_metrics.heading("值", text="值")
tree_metrics.pack()

metrics = [
    ("R² Score", r2),
    ("均方误差 (MSE)", mse),
    ("回归系数", coefficients),
    ("截距", intercept)
]

for metric, value in metrics:
    tree_metrics.insert("", tk.END, values=(metric, f"{value:.4f}"))

# 运行应用程序
app.mainloop()
