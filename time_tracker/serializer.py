import json
from datetime import datetime
from pathlib import Path
from typing import Dict

# Constansts
FILE_NAME = 'data.json'
DATE_FORMAT = '%Y-%m-%d'

def save_to_file(data_to_save: dict)->None:
    previous_data = load_from_file()
    formatted_data = {}
    for date in data_to_save:
        if date not in previous_data:
            activites = data_to_save[date]
            formatted_data[datetime.strftime(date, DATE_FORMAT)] = activites
        else:
            activites = data_to_save[date]
            previous_activites = previous_data[date]

            for activity in activites:
                if activity in previous_activites:
                    activites[activity] = activites[activity] + previous_activites[activity]

            formatted_data[datetime.strftime(date, DATE_FORMAT)] = activites

    with open(FILE_NAME, 'w') as f:
        json.dump(formatted_data, f, indent=2)

def load_from_file()->Dict:
    file = Path(FILE_NAME)
    formatted_data = {}
    if file.is_file():
        with open(FILE_NAME) as f:
            data_to_load = json.load(f)
        for date in data_to_load:
            activites = data_to_load[date]
            formatted_data[datetime.strptime(date, DATE_FORMAT).date()] = activites
    else:
        print('File doesn\'t exist.')
    return formatted_data

def list_apps_on_file()->None:
    with open(FILE_NAME) as f:
        data = json.load(f)
    for item in data:
        print(item)
        i = data[item]
        for a in i:
            print(f'\t{a} : {i[a]}')

