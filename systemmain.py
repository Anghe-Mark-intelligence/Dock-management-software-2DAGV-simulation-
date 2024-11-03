#conda hongweihuangsystem
#若电脑没安装conda环境，则务必按如下代码输入终端
#conda create --name mtsystem python=3.8
#conda activate mtsystem
#pip install Pillow
#pip install requests beautifulsoup4

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import webbrowser

# 管理员的用户名和密码
admin_username = "admin"
admin_password = "123456"

# 固定的新闻网址
fixed_links = [
    "https://www.sohu.com/a/792490237_120153860",
    "https://haokan.baidu.com/v?pd=wisenatural&vid=678335125171766981",
    "https://worktile.com/kb/p/3090271",
    "https://baijiahao.baidu.com/s?id=1800257022570291757&wfr=spider&for=pc",
    "https://www.fwsir.com/fanwen/html/fanwen_20240816162522_3951326.html",
    "https://haokan.baidu.com/v?pd=wisenatural&vid=4644179736154287725",
    "https://b2b.baidu.com/q/aland?q=1E1D7F6672660B22047E7575033C6A73010A711276137135797B01627116196E&id=qideb5cd6c5da9c02bf91946dd63643199f&answer=9166279784795030838&utype=2",
    "https://www.baidu.com/link?url=_8XuMK6lzzfdkaLvmMjgRtxoF_ALHDWxj3ofeiQCUGBM0SUu4Xgfvo1zsHrX6YwGunkXA07QaceEy29kplgTsTstiNAdaiglklry7FMB81WQex1NR0PUEbNBT7b3xMM3&wd=&eqid=ce01cbcd0004df540000000267263b91"
]

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == admin_username and password == admin_password:
        messagebox.showinfo("登录成功", "欢迎进入系统！")
        open_main_interface()
    else:
        messagebox.showerror("登录失败", "管理员或者密码错误，请重试。")

def open_main_interface():
    for widget in root.winfo_children():
        widget.destroy()

    label_title = tk.Label(root, text="码头货运管理系统", font=("Arial", 20))
    label_title.pack(pady=20)

    news_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
    news_frame.pack(pady=10, padx=10, fill=tk.X)

    label_news_title = tk.Label(news_frame, text="新闻状态栏（实时更新）:", font=("Arial", 12))
    label_news_title.pack(side=tk.LEFT)

    news_text = tk.Text(news_frame, height=10, width=80, wrap=tk.WORD, state=tk.DISABLED)
    news_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(news_frame, command=news_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    news_text.config(yscrollcommand=scrollbar.set)

    news_text.config(state=tk.NORMAL)
    for link in fixed_links:
        news_text.insert(tk.END, f"{link}\n", "link")
        news_text.tag_config("link", foreground="blue", underline=True)
        news_text.tag_bind("link", "<Button-1>", lambda e, url=link: open_link(url))
        news_text.tag_bind("link", "<Enter>", lambda e: news_text.config(cursor="hand2"))  # 更改鼠标光标为小手
        news_text.tag_bind("link", "<Leave>", lambda e: news_text.config(cursor=""))  # 还原鼠标光标
    news_text.config(state=tk.DISABLED)

    button_agv_management = tk.Button(root, text="AGV货运小车管理", command=lambda: subprocess.run(["python", r"C:\Users\Administrator\Desktop\hongweihuang_system\agvplan.py"]))
    button_agv_management.pack(pady=10)

    button_dock_management = tk.Button(root, text="码头装卸管理", command=lambda: subprocess.run(["python", r"C:\Users\Administrator\Desktop\hongweihuang_system\matouzhuangxie.py"]))
    button_dock_management.pack(pady=10)

    button_crane_management = tk.Button(root, text="吊机管理", command=lambda: subprocess.run(["python", r"C:\Users\Administrator\Desktop\hongweihuang_system\Crane_management.py"]))
    button_crane_management.pack(pady=10)

    button_goods_identification = tk.Button(root, text="货物煤炭识别", command=lambda: subprocess.run(["python", r"C:\Users\Administrator\Desktop\hongweihuang_system\Goods_identification.py"]))
    button_goods_identification.pack(pady=10)

    label_footer = tk.Label(root, text="made by hongweihuang_AI", font=("Arial", 10))
    label_footer.pack(side=tk.BOTTOM, pady=10)

def open_link(url):
    webbrowser.open(url)

def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

def forgot_password():
    def check_answer():
        answer = entry_answer.get()
        if answer == "互联网+":
            new_password = entry_new_password.get()
            global admin_password
            admin_password = new_password
            messagebox.showinfo("密码重置成功", "密码已成功重置。")
            reset_window.destroy()
        else:
            messagebox.showerror("错误", "回答错误，无法重置密码。")

    reset_window = tk.Toplevel(root)
    reset_window.title("找回密码")
    reset_window.geometry("400x200")

    label_question = tk.Label(reset_window, text="密保：黄宏伟大学第一次参加的学科竞赛是什么？")
    label_question.pack(pady=10)

    entry_answer = tk.Entry(reset_window)
    entry_answer.pack(pady=5)

    label_new_password = tk.Label(reset_window, text="请输入新密码:")
    label_new_password.pack(pady=5)

    entry_new_password = tk.Entry(reset_window, show="*")
    entry_new_password.pack(pady=5)

    button_submit = tk.Button(reset_window, text="提交", command=check_answer)
    button_submit.pack(pady=20)

root = tk.Tk()
root.title("码头货运管理系统")
root.geometry("1080x900")

bg_image_path = r"C:\Users\Administrator\Desktop\hongweihuang_system\matou2.png"
bg_image = Image.open(bg_image_path).convert("RGBA")
bg_image = bg_image.resize((1080, 900), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

label_bg = tk.Label(root, image=bg_photo)
label_bg.place(x=0, y=0, relwidth=1, relheight=1)

label_username = tk.Label(root, text="管理员用户名:", bg="white")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

label_password = tk.Label(root, text="管理员密码:", bg="white")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

button_login = tk.Button(root, text="登录", command=login)
button_login.pack(pady=20)

button_forgot_password = tk.Button(root, text="找回密码", command=forgot_password)
button_forgot_password.pack(pady=5)

label_footer = tk.Label(root, text="made by mark_AI", font=("Arial", 10), bg="white")
label_footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
