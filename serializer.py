import json
from datetime import datetime
from pathlib import Path

# Constansts
FILE_NAME = 'data.json'
DATE_FORMAT = '%Y-%m-%d'

def save_to_file(data_to_save: dict):
    formatted_data = {}
    for date in data_to_save:
        activites = data_to_save[date]

        formatted_data[datetime.strftime(date, DATE_FORMAT)] = activites

    with open(FILE_NAME, 'w') as f:
        json.dump(formatted_data, f, indent=2)

def load_from_file():
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

# This function is for debugging puropses
def list_apps_on_file():
    with open(FILE_NAME) as f:
        data = json.load(f)

    for item in data:
        print(item)
        i = data[item]
        for a in i:
            print(f'\t{a} : {i[a]}')

