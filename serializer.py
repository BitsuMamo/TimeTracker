import json
from datetime import datetime, timedelta
from pathlib import Path

FILE_NAME = 'data.json'
DATE_FORMAT = '%Y-%m-%d'

def save_to_file(data_to_save: dict):
    formatted_data = {}
    for date in data_to_save:
        activites = data_to_save[date]
        '''
        for activity in activites:
            delta_time = activites[activity]
            activites[activity] = delta_time.total_seconds()
        '''
        formatted_data[datetime.strftime(date, DATE_FORMAT)] = activites

    with open(FILE_NAME, 'w') as f:
        json.dump(formatted_data, f, indent=2)

def load_from_file():
    file = Path(FILE_NAME)
    formatted_data = {}

    if file.is_file():

        with open(FILE_NAME) as f:
            data = json.load(f)

        for date in data:
            activites = data[date]
            '''
            for activity in activites:
                activites[activity] = timedelta(seconds=activites[activity])
            '''
            formatted_data[datetime.strptime(date, DATE_FORMAT)] = activites
    else:
        print('File doesn\'t exist.')

    return formatted_data

def list_apps_on_file():
    with open(FILE_NAME) as f:
        data = json.load(f)

    for item in data:
        print(item)
        i = data[item]
        for a in i:
            print(f'\t{a} : {i[a]}')

