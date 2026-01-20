import tkinter as tk
from tkinter import colorchooser, Menu
import requests
import datetime
import json
import os

CONFIG_FILE = "clock_config.json"

# ===== LOAD / SAVE CONFIG =====
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"color": "#00ff00", "size": 32}

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# ===== LẤY GIỜ INTERNET =====
def get_vn_time():
    try:
        r = requests.get(
            "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Ho_Chi_Minh",
            timeout=2
        )
        d = r.json()
        return f"{d['hour']:02d}:{d['minute']:02d}:{d['seconds']:02d}"
    except:
        return datetime.datetime.now().strftime("%H:%M:%S")

def update_time():
    time_label.config(text=get_vn_time())
    root.after(1000, update_time)

# ===== ĐỔI MÀU =====
def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        config["color"] = color
        time_label.config(fg=color)
        save_config()

# ===== DI CHUYỂN =====
def start_move(e):
    root.x = e.x
    root.y = e.y

def do_move(e):
    root.geometry(f"+{root.winfo_pointerx()-root.x}+{root.winfo_pointery()-root.y}")

# ===== RESIZE =====
def start_resize(e):
    root.rx = e.x
    root.ry = e.y
    root.rw = root.winfo_width()
    root.rh = root.winfo_height()

def do_resize(e):
    w = root.rw + (e.x - root.rx)
    h = root.rh + (e.y - root.ry)
    root.geometry(f"{max(w,120)}x{max(h,50)}")

# ===== MENU CHUỘT PHẢI =====
def show_menu(e):
    menu.tk_popup(e.x_root, e.y_root)

def reset_size():
    root.geometry("220x60")

# ===== UI =====
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.configure(bg="#1e1e1e")
root.attributes("-alpha", 0.92)

root.geometry("220x60")

canvas = tk.Canvas(root, bg="#1e1e1e", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# bo tròn
canvas.create_rectangle(
    0, 0, 300, 200,
    fill="#1e1e1e", outline=""
)

frame = tk.Frame(canvas, bg="#1e1e1e")
frame.place(relwidth=1, relheight=1)

# ===== ICON =====
edit = tk.Label(frame, text="✏", fg="#ffaa00", bg="#1e1e1e",
                font=("Segoe UI", 13), cursor="hand2")
edit.pack(side="left", padx=6)
edit.bind("<Button-1>", lambda e: choose_color())

time_label = tk.Label(
    frame,
    text="--:--:--",
    fg=config["color"],
    bg="#1e1e1e",
    font=("Segoe UI", config["size"], "bold")
)
time_label.pack(side="left")

close = tk.Label(frame, text="✖", fg="#ff5555", bg="#1e1e1e",
                 font=("Segoe UI", 13), cursor="hand2")
close.pack(side="right", padx=6)
close.bind("<Button-1>", lambda e: root.destroy())

# ===== GÓC RESIZE =====
resize = tk.Label(frame, text="◢", fg="#666", bg="#1e1e1e",
                  cursor="bottom_right_corner")
resize.place(relx=1.0, rely=1.0, anchor="se")
resize.bind("<Button-1>", start_resize)
resize.bind("<B1-Motion>", do_resize)

# ===== MENU =====
menu = Menu(root, tearoff=0)
menu.add_command(label="🎨 Đổi màu", command=choose_color)
menu.add_command(label="🔄 Reset kích thước", command=reset_size)
menu.add_separator()
menu.add_command(label="❌ Thoát", command=root.destroy)

frame.bind("<Button-3>", show_menu)
time_label.bind("<Button-3>", show_menu)

frame.bind("<Button-1>", start_move)
frame.bind("<B1-Motion>", do_move)

update_time()
root.mainloop()
