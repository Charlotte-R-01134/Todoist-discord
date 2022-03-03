from pypresence import Presence
import time
from datetime import datetime
import todoist
import tkinter as tk
from tkinter import simpledialog

root= tk.Tk()
root.withdraw()

def get_today_tasks(api):
    count = 0
    try:
        for task in api.state['items']:
            if task['due'] is not None:
                if task['due']['date'] == datetime.now().strftime("%Y-%m-%d"):
                    count += 1
    except Exception:
        pass
    return count

def get_overdue_tasks(api):
    count = 0
    try:
        for task in api.state['items']:
            if task['due'] is not None:
                if task['due']['date'] < datetime.now().strftime("%Y-%m-%d"):
                    count += 1
    except Exception:
        pass
    return count

def get_completed_tasks(api):
    try:
        response = api.completed.get_stats()
        completed = response['days_items'][0]['total_completed']
    except Exception:
        pass
    return completed

client = simpledialog.askstring(title="Client ID", prompt="Enter your client ID:")
token = simpledialog.askstring(title="Token", prompt="Enter your token:")
while True:
    api = todoist.TodoistAPI(token)
    api.sync()
    client_id = client #Put your client ID here
    try:
        RPC = Presence(client_id) 
        RPC.connect()
        RPC.update(state=f"Completed tasks: {get_completed_tasks(api)}\n", details=f"Tasks todo: {get_today_tasks(api)+get_overdue_tasks(api)}", small_image="todoist", small_text = "todoist", start=time.time())  # Set the presence
        time.sleep(15)
    except:
        time.sleep(15)