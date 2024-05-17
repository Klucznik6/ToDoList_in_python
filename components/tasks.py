import json


def clearing_row_value():
    data = {
        'row': 0
    }
    print("działam")
    with open("config.json", "w") as file:
        json.dump(data, file)


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
