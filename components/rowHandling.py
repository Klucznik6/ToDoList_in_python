import json


def update_row(current_widget_row):
    config_open = open("config.json", "r")
    data = json.load(config_open)
    current_widget_row = data["row"]
    print(current_widget_row)
    config_open.close()
    return current_widget_row


def update_row_count(row):
    data = {
        'row': row
    }
    with open("config.json", "w") as write_file:
        json.dump(data, write_file)
