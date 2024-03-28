import json, time
import tkinter as tk
from tkinter import messagebox, simpledialog

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def view_tasks(self):
        for task in self.tasks:
            status = 'Completed' if task.completed else 'Not Completed'
            print(f'Task: {task.title}, Status: {status}')

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def complete_task(self, title):
        for task in self.tasks:
            if task.title == title:
                task.completed = True
                self.save_tasks()
                break

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
                self.tasks = [Task(task['title'], task['description']) for task in tasks]
                for task, task_data in zip(self.tasks, tasks):
                    task.completed = task_data['completed']
        except FileNotFoundError:
            pass
class App:
    def __init__(self, todo_list):
        self.todo_list = todo_list
        self.root = tk.Tk()
        self.root.title("To-Do List")
        self.root.geometry("300x400")
        self.root.configure(bg='black')
        self.listbox = tk.Listbox(self.root, bg='black', fg='white')
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.update_listbox()

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task, bg='white')
        self.add_button.pack(padx=10, pady=5, fill=tk.X)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task, bg='white')
        self.delete_button.pack(padx=10, pady=5, fill=tk.X)

        self.complete_button = tk.Button(self.root, text="Complete Task", command=self.delete_task, bg='white')
        self.complete_button.pack(padx=10, pady=5, fill=tk.X)

        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings, bg='white')
        self.settings_button.pack(padx=10, pady=5, fill=tk.X)

        self.settings_frame = tk.Frame(self.root)
        self.theme_button = tk.Button(self.settings_frame, text="Toggle Dark/Light Mode", command=self.toggle_theme)
        self.theme_button.pack(padx=10, pady=10)
        self.save_button = tk.Button(self.settings_frame, text="Save Settings", command=self.save_settings)
        self.save_button.pack(padx=10, pady=10)

        self.load_settings()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.todo_list.tasks:
            status = 'Completed' if task.completed else 'Not Completed'
            self.listbox.insert(tk.END, f'Task: {task.title}, Status: {status}')

    def add_task(self):
        self.new_task_window = tk.Toplevel(self.root)
        self.new_task_window.title("Add task")

        tk.Label(self.new_task_window, text="Enter task title:").pack()
        self.title_entry = tk.Entry(self.new_task_window)
        self.title_entry.pack()

        tk.Label(self.new_task_window, text="Enter task description:").pack()
        self.description_entry = tk.Text(self.new_task_window, height=5)
        self.description_entry.pack()

        tk.Button(self.new_task_window, text="Submit", command=self.submit_task).pack()

    def submit_task(self):
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", tk.END).strip()
        if title and description:
            self.todo_list.add_task(title, description)
            self.update_listbox()
        self.new_task_window.destroy()


    def delete_task(self):
        if self.listbox.curselection():
            title = self.listbox.get(self.listbox.curselection())
            if title:
                self.todo_list.delete_task(title[6:title.find(',')])
                self.update_listbox()
        else:
            messagebox.showinfo("No selection", "Please select a task to delete.")

    def complete_task(self):
        if self.listbox.curselection():
            title = self.listbox.get(self.listbox.curselection())
            if title:
                self.todo_list.complete_task(title[6:title.find(',')])  # Extract task title
                self.update_listbox()
        else:
            messagebox.showinfo("No selection", "Please select a task to complete.")

    def view_task(self, event):
        if self.listbox.curselection():
            title = self.listbox.get(self.listbox.curselection())
            for task in self.todo_list.tasks:
                if title[6:title.find(',')] == task.title:
                    self.view_task_window = tk.Toplevel(self.root)
                    self.view_task_window.title("Task Details")

                    tk.Label(self.view_task_window, text=f"Title: {task.title}").pack()
                    tk.Label(self.view_task_window, text="Description:").pack()
                    tk.Label(self.view_task_window, text=task.description, justify=tk.LEFT).pack()

                    window_width = 300
                    window_height = 200

                    root_width = self.root.winfo_width()
                    root_height = self.root.winfo_height()
                    root_x = self.root.winfo_x()
                    root_y = self.root.winfo_y()

                    position_top = root_y + (root_height // 2) - (window_height // 2)
                    position_left = root_x + (root_width // 2) - (window_width // 2)

                    self.view_task_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')


    def toggle_theme(self):
        if self.root.cget('bg') == 'black':
            self.root.configure(bg='white')
            self.listbox.configure(bg='white', fg='black')
            self.add_button.configure(bg='white', fg='black')
            self.delete_button.configure(bg='white', fg='black')
            self.complete_button.configure(bg='white', fg='black')
            self.settings_button.configure(bg='white', fg='black')
        else:
            self.root.configure(bg='black')
            self.listbox.configure(bg='black', fg='white')
            self.add_button.configure(bg='black', fg='white')
            self.delete_button.configure(bg='black', fg='white')
            self.complete_button.configure(bg='black', fg='white')
            self.settings_button.configure(bg='black', fg='white')

    def open_settings(self):
        self.listbox.pack_forget()
        self.add_button.pack_forget()
        self.delete_button.pack_forget()
        self.complete_button.pack_forget()
        self.settings_button.pack_forget()

        if self.root.cget('bg') == 'black':
            self.settings_frame.configure(bg='black')
            self.theme_button.configure(bg='black', fg='white')
            self.save_button.configure(bg='black', fg='white')
        else:
            self.settings_frame.configure(bg='white')
            self.theme_button.configure(bg='white', fg='black')
            self.save_button.configure(bg='white', fg='black')

        self.settings_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def close_settings(self):
        self.settings_frame.pack_forget()
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.add_button.pack(padx=10, pady=5, fill=tk.X)
        self.delete_button.pack(padx=10, pady=5, fill=tk.X)
        self.complete_button.pack(padx=10, pady=5, fill=tk.X)
        self.settings_button.pack(padx=10, pady=5, fill=tk.X)

    def save_settings(self):
        with open('settings.json', 'w') as file:
            json.dump({'theme': 'dark' if self.root.cget('bg') == 'black' else 'light'}, file)
        self.close_settings()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as file:
                settings = json.load(file)
                if settings['theme'] == 'dark':
                    self.root.configure(bg='black')
                    self.listbox.configure(bg='black', fg='white')
                    self.add_button.configure(bg='black', fg='white')
                    self.delete_button.configure(bg='black', fg='white')
                    self.complete_button.configure(bg='black', fg='white')
                    self.settings_button.configure(bg='black', fg='white')
                else:
                    self.root.configure(bg='white')
                    self.listbox.configure(bg='white', fg='black')
                    self.add_button.configure(bg='white', fg='black')
                    self.delete_button.configure(bg='white', fg='black')
                    self.complete_button.configure(bg='white', fg='black')
                    self.settings_button.configure(bg='white', fg='black')
        except FileNotFoundError:
            pass

    def run(self):
        self.listbox.bind('<Double-Button-1>', self.view_task)
        self.root.mainloop()

def main():
    todo_list = ToDoList()
    app = App(todo_list)
    app.run()

if __name__ == "__main__":
    main()