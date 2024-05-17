import os.path
import customtkinter
import re
import json
from timeConfig import now

task_widget_row = 0  # zmienna odpowiadająca za kolejność zadań


def if_files_exists():
    data = {
        'row': 0
    }
    data_to_saved = {
        'saved_tasks': []
    }
    try:
        if not os.path.exists("config.json"):
            f = open("config.json", "x")
            f.write(json.dumps(data))
            f.close()
    except:
        print("Config jest plikiem !")
    try:
        if not os.path.exists("saved.json"):
            f = open("saved.json", "x")
            f.write(json.dumps(data_to_saved))
            f.close()
    except:
        print("Saved jest plikiem !")


if_files_exists()


def save_task(task_row, content, date):
    try:
        with open("saved.json", 'r') as file:
            tasks_dict = json.load(file)
    except FileNotFoundError:
        tasks_dict = {"saved_tasks": []}

    task_to_save = {
        "row": task_row,
        "content": content,
        "date": date
    }
    tasks_dict["saved_tasks"].append(task_to_save)

    with open("saved.json", 'w') as file:
        json.dump(tasks_dict, file, indent=4)


def update_row(current_widget_row):
    config_open = open("config.json", "r")
    data = json.load(config_open)
    current_widget_row = data["row"]
    print(current_widget_row)
    config_open.close()
    return current_widget_row


task_widget_row = update_row(task_widget_row)


def clearing_row_value():
    data = {
        'row': 0
    }
    print("działam")
    with open("config.json", "w") as file:
        json.dump(data, file)


def delete_task(row):
    try:
        with open("saved.json", 'r') as file:
            tasks_dict = json.load(file)
    except FileNotFoundError:
        print("Plik saved.json nie istnieje.")
        return

    if "saved_tasks" not in tasks_dict:
        print("Brak listy zadań w pliku.")
        return

    tasks_to_keep = [task for task in tasks_dict["saved_tasks"] if task.get("row") != row]

    tasks_dict["saved_tasks"] = tasks_to_keep

    if not tasks_dict["saved_tasks"]:
        clearing_row_value()

    with open("saved.json", 'w') as file:
        json.dump(tasks_dict, file, indent=4)


class task_widget:

    def __init__(self, content, row, time):
        self.task_widget_label = customtkinter.CTkLabel(tasks_frame, width=390, height=100, bg_color="dodgerblue3",
                                                        text=content)
        self.delete_button = customtkinter.CTkButton(self.task_widget_label, width=40, height=40,
                                                     bg_color="dodgerblue3", fg_color="firebrick3", text="❌",
                                                     command=lambda: (
                                                         self.task_widget_label.destroy(), delete_task(row)))
        self.task_widget_label.grid(row=row, column=0, pady=20)
        self.delete_button.grid(row=0, column=1)
        print(time)
        print(row)


def restore_tasks():
    f = open("saved.json", "r")
    data = json.loads(f.read())
    for task in data["saved_tasks"]:
        task_widget(task['content'], task['row'], task['date'])
    f.close()


def update_row_count(row):
    data = {
        'row': row
    }
    with open("config.json", "w") as write_file:
        json.dump(data, write_file)


def button_submit_entry():
    entry_content = entry.get()
    entry_length = len(entry.get())
    pattern = re.compile(r'\s+')
    entry_content = re.sub(pattern, '', entry_content)

    if entry_content != "":
        global task_widget_row
        task_widget_row += 1
        task_widget(entry.get(), task_widget_row, now)
        update_row_count(task_widget_row)
        save_task(task_widget_row, entry.get(), now)
        entry.delete(0, entry_length)
    else:
        entry.delete(0, entry_length)
        pass


app = customtkinter.CTk()
app.geometry("700x400")

tasks_frame = customtkinter.CTkScrollableFrame(app, width=440, height=340, fg_color="grey14")
tasks_frame.pack(anchor="n", expand=True, pady=5)

submiting_frame = customtkinter.CTkFrame(app, width=500, height=200)
submiting_frame.pack(anchor="s", expand=True, pady=5)
submiting_frame.pack_propagate(0)

entry = customtkinter.CTkEntry(submiting_frame, placeholder_text="Co chcesz dziś zrobić ?", width=300, font=("", 17),
                               corner_radius=0)
entry_submit_button = customtkinter.CTkButton(submiting_frame, text="Zapisz", command=button_submit_entry,
                                              font=("", 17), corner_radius=0)

entry.grid(row=0, column=0)
entry_submit_button.grid(row=0, column=1)

restore_tasks()

app.mainloop()