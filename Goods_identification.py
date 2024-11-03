#pip install opencv-python
import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk

class CoalDetector:
    def __init__(self, master):
        self.master = master
        master.title("煤炭识别系统")
        master.geometry("600x600")  # 设置窗口大小
        master.configure(bg='white')  # 设置背景颜色为白色

        # 加载背景图像并设置透明度
        self.bg_image = Image.open(r"C:\Users\Administrator\Desktop\hongweihuang_system\meitan.png").convert("RGBA")
        self.bg_image = self.bg_image.resize((600, 600), Image.LANCZOS)  # 使用 LANCZOS 代替 ANTIALIAS
        self.bg_image.putalpha(153)  # 60% 不透明度（255是完全不透明）

        self.original_image = None
        self.processed_image = None
        self.image_label = None  # 用于显示图像

        self.show_background()  # 显示背景图像

        self.label = Label(master, text="请加载图像", bg='white')
        self.label.pack(pady=20)

        self.load_button = Button(master, text="加载图像", command=self.load_image, bg='blue', fg='white', width=15)
        self.load_button.pack(pady=10)

        self.detect_button = Button(master, text="识别煤炭", command=self.detect_coal, bg='green', fg='white', width=15)
        self.detect_button.pack(pady=10)

    def show_background(self):
        bg_tk = ImageTk.PhotoImage(self.bg_image)
        bg_label = Label(self.master, image=bg_tk)
        bg_label.image = bg_tk  # Keep a reference
        bg_label.place(x=0, y=0)  # 使背景覆盖整个窗口

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.show_image(self.original_image, "原图像")

    def detect_coal(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

            # 查找轮廓
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            coal_found = False

            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # 可调节的面积阈值
                    cv2.drawContours(self.original_image, [contour], -1, (0, 255, 0), 2)
                    coal_found = True

            if coal_found:
                self.processed_image = self.original_image
                self.show_image(self.processed_image, "识别结果：有煤炭")
            else:
                self.label.config(text="没有煤炭")
                self.show_image(self.original_image, "识别结果：没有煤炭")

    def show_image(self, img, title):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        # 清除旧图像
        if self.image_label is not None:
            self.image_label.destroy()

        self.image_label = Label(self.master, image=img_tk, bg='white')
        self.image_label.image = img_tk  # Keep a reference
        self.image_label.pack(pady=10)
        self.master.title(title)

if __name__ == "__main__":
    root = Tk()
    coal_detector = CoalDetector(root)
    root.mainloop()
