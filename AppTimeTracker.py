import win32gui
from datetime import datetime
from time import sleep

def get_app_name():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

def correct_app_name(app_name):

    return None

# {date:{name:time}}

app_activity_list = {}
current_date_activity = {}
current_app_name = get_app_name()
start_time = datetime.now()

while True:
    date_exists = False
    app_name_exists = False
    current_date = datetime.now().date()
    active_app_name = get_app_name()
    end_time = None

    if current_date in app_activity_list:
        date_exists = True

    if date_exists:
        current_date_activity = app_activity_list[current_date]

    if not date_exists:
        current_date_activity = {}

    if active_app_name != current_app_name and active_app_name != "":
        end_time = datetime.now()

        if current_app_name in current_date_activity:
            app_name_exists = True

        if app_name_exists:
            current_date_activity[current_app_name] = current_date_activity[current_app_name] + (end_time - start_time)
        else:
            current_date_activity[current_app_name] = end_time - start_time

        print(current_app_name + ": " + str(current_date_activity[current_app_name]))
        print("============================================================================================")
        current_app_name = active_app_name
        start_time = end_time


    app_activity_list[current_date] = current_date_activity


    # sleep(5)


