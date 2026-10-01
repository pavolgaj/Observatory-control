#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import os
import time

CONFIG_FILE = "config.json"

def load_config():
    """Load button config from JSON file."""
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror("Error", f"Config file '{CONFIG_FILE}' not found!")
        return {"groups": []}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def run_command(command):
    """Run a shell command when a button is pressed."""
    try:
        subprocess.Popen(command, shell=True)
        print(f'Running command: {command}')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run command:\n{e}")


def on_button_click(button_info):
    """Handle button click with optional confirmation."""
    command = button_info.get("command", "")
    confirm_text = button_info.get("confirm")

    if confirm_text:
        answer = messagebox.askyesno("SAFETY WARNING", confirm_text, icon='warning')
        if not answer:
            return  # user cancelled

    run_command(command)
    
    time.sleep(2)
    
    messagebox.showinfo("Info", 'Action "'+button_info.get("name","")+'" was executed!')

def create_group(frame, group):
    """Create a labeled frame for each group of buttons."""
    group_frame = ttk.LabelFrame(frame, text=group.get("name", ""), padding=(10, 5))
    group_frame.pack(fill="x", padx=10, pady=10)
    
    ssh=group.get("ssh", False)
    if ssh:
        ip=group.get("ip", "")
        user=group.get("user", "")
        if len(ip)*len(user)==0: ssh=False

    for btn in group.get("buttons", []):
        name = btn.get("name", "Button")
        command = btn.get("command", "")
        if not command: continue  #empty command
        
        if ssh:
            #run remotely
            btn["command"]=f'ssh {user}@{ip} '+command.replace('&&','\\&\\&')             

        ttk.Button(
            group_frame, text=name, width=40,
            command=lambda b=btn: on_button_click(b)
        ).pack(pady=4)
        

def create_gui():
    """Build the full Tkinter window with groups and buttons."""
    config = load_config()
    root = tk.Tk()
    root.title(config['title'])
    root.geometry(config['size'])

    # Title
    ttk.Label(root, text=config['title'], font=("Arial", 16, "bold")).pack(pady=10)

    # Groups
    for group in config.get("groups", []):
        create_group(root, group)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
