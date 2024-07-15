
#To-Do List application

import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

TASKS_FILE = Path("tasks.json")

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x450")
        self.root.configure(bg="#2E3440")  # Set background color

        self.tasks = self.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="To-Do List", bg="#2E3440", fg="#D8DEE9", font=("Helvetica", 20))
        self.title_label.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, bg="#3B4252", fg="#D8DEE9", selectbackground="#88C0D0", font=("Helvetica", 12))
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.add_frame = tk.Frame(self.root, bg="#2E3440")
        self.add_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.add_frame, bg="#4C566A", fg="#D8DEE9", font=("Helvetica 12 bold"), width=25)
        self.task_entry.grid(row=0, column=0, padx=5)

        self.add_button = tk.Button(self.add_frame, text="Add Task", command=self.add_task, bg="#5E81AC", fg="black", font=("Helvetica", 12))
        self.add_button.grid(row=0, column=1, padx=5)

        self.button_frame = tk.Frame(self.root, bg="#2E3440")
        self.button_frame.pack(pady=5)

        self.done_button = tk.Button(self.button_frame, text="Mark as Done", command=self.mark_done, bg="#5E81AC", fg="black", font=("Helvetica", 12))
        self.done_button.grid(row=0, column=0, padx=5)
        
        self.remove_button = tk.Button(self.button_frame, text="Remove Task", command=self.remove_task, bg="#BF616A", fg="black", font=("Helvetica", 12))
        self.remove_button.grid(row=0, column=1, padx=5)

        self.load_tasks_to_listbox()

    def load_tasks_to_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for index, task in enumerate(self.tasks, start=1):
            status = " (Done)" if task['is_done'] else ""
            self.task_listbox.insert(tk.END, f"Task{index}: {task['title']}{status}")

    def add_task(self):
        task_title = self.task_entry.get().strip()
        if task_title:
            new_task = {"title": task_title, "is_done": False}
            self.tasks.append(new_task)
            self.save_tasks()
            self.load_tasks_to_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task title.")

    def mark_done(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.tasks[index]['is_done'] = True
            self.save_tasks()
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")
    
    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.tasks.pop(index)
            self.save_tasks()
            self.load_tasks_to_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to remove.")

    def load_tasks(self):
        if TASKS_FILE.exists():
            with open(TASKS_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as file:
            json.dump(self.tasks, file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
