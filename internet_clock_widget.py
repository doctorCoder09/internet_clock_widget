import tkinter as tk
from tkinter import colorchooser, Menu
import requests
import datetime
import time
import json
import os

CONFIG_FILE = "clock_config.json"
SYNC_INTERVAL = 20 * 60   # 20 phút

# ===== CONFIG =====
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "color": "#00ff00",
        "x": 200,
        "y": 50
    }

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

config = load_config()

# ===== TIME SYNC =====
base_time = None
base_timestamp = None

def sync_time():
    global base_time, base_timestamp
    try:
        r = requests.get(
            "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Ho_Chi_Minh",
            timeout=3
        )
        d = r.json()
        base_time = datetime.datetime(
            d["year"], d["month"], d["day"],
            d["hour"], d["minute"], d["seconds"]
        )
        base_timestamp = time.time()
    except:
        if base_time is None:
            base_time = datetime.datetime.now()
            base_timestamp = time.time()

def get_display_time():
    delta = time.time() - base_timestamp
    return (base_time + datetime.timedelta(seconds=delta)).strftime("%H:%M:%S")

def update_clock():
    time_label.config(text=get_display_time())
    root.after(1000, update_clock)

def schedule_sync():
    sync_time()
    root.after(SYNC_INTERVAL * 1000, schedule_sync)

# ===== UI ACTIONS =====
def choose_color():
    color = colorchooser.askcolor()[1]
    if color:
        config["color"] = color
        time_label.config(fg=color)
        save_config()

def start_move(e):
    root.x = e.x
    root.y = e.y

def do_move(e):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

def end_move(e):
    config["x"] = root.winfo_x()
    config["y"] = root.winfo_y()
    save_config()

def show_menu(e):
    menu.tk_popup(e.x_root, e.y_root)

def exit_app():
    config["x"] = root.winfo_x()
    config["y"] = root.winfo_y()
    save_config()
    root.destroy()

# ===== UI =====
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.92)
root.configure(bg="#1e1e1e")

root.geometry(f"220x60+{config['x']}+{config['y']}")

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(fill="both", expand=True)

edit = tk.Label(
    frame, text="✏", fg="#ffaa00", bg="#1e1e1e",
    font=("Segoe UI", 13), cursor="hand2"
)
edit.pack(side="left", padx=6)
edit.bind("<Button-1>", lambda e: choose_color())

time_label = tk.Label(
    frame,
    text="--:--:--",
    fg=config["color"],
    bg="#1e1e1e",
    font=("Segoe UI", 32, "bold")
)
time_label.pack(side="left")

close = tk.Label(
    frame, text="✖", fg="#ff5555", bg="#1e1e1e",
    font=("Segoe UI", 13), cursor="hand2"
)
close.pack(side="right", padx=6)
close.bind("<Button-1>", lambda e: exit_app())

# ===== MENU =====
menu = Menu(root, tearoff=0)
menu.add_command(label="🎨 Đổi màu", command=choose_color)
menu.add_separator()
menu.add_command(label="❌ Thoát", command=exit_app)

frame.bind("<Button-3>", show_menu)
time_label.bind("<Button-3>", show_menu)

frame.bind("<Button-1>", start_move)
frame.bind("<B1-Motion>", do_move)
frame.bind("<ButtonRelease-1>", end_move)

# ===== START =====
sync_time()
schedule_sync()
update_clock()

root.mainloop()
