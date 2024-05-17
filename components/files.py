import json
import os


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