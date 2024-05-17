import customtkinter
import re
from components.timeConfig import now
from components.files import *
from components.tasks import *
from components.rowHandling import *


class task_widget_class:

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
        task_widget_class(task['content'], task['row'], task['date'])
    f.close()


def button_submit_entry():
    entry_content = entry.get()
    entry_length = len(entry.get())
    pattern = re.compile(r'\s+')
    entry_content = re.sub(pattern, '', entry_content)

    if entry_content != "":
        global task_widget_row
        task_widget_row += 1
        task_widget_class(entry.get(), task_widget_row, now)
        update_row_count(task_widget_row)
        save_task(task_widget_row, entry.get(), now)
        entry.delete(0, entry_length)
    else:
        entry.delete(0, entry_length)
        pass


if __name__ == "__main__":
    task_widget_row = 0  # zmienna odpowiadająca za kolejność zadań

    if_files_exists()

    task_widget_row = update_row(task_widget_row)

    app = customtkinter.CTk()
    app.geometry("700x400")

    tasks_frame = customtkinter.CTkScrollableFrame(app, width=440, height=340, fg_color="grey14")
    tasks_frame.pack(anchor="n", expand=True, pady=5)

    submiting_frame = customtkinter.CTkFrame(app, width=500, height=200)
    submiting_frame.pack(anchor="s", expand=True, pady=5)
    submiting_frame.pack_propagate(0)

    entry = customtkinter.CTkEntry(submiting_frame, placeholder_text="Co chcesz dziś zrobić ?", width=300,
                                   font=("", 17),
                                   corner_radius=0)
    entry_submit_button = customtkinter.CTkButton(submiting_frame, text="Zapisz", command=button_submit_entry,
                                                  font=("", 17), corner_radius=0)

    entry.grid(row=0, column=0)
    entry_submit_button.grid(row=0, column=1)

    restore_tasks()

    app.mainloop()
