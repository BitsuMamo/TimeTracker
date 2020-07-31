import win32gui
import time
import json
from datetime import datetime

activity_name = ''
active_window_name =''
activity_list = []
new_user = True
hour = datetime.now().hour * 3600
minitue = datetime.now().minute* 60
sec = datetime.now().second

start_time = hour + minitue + sec
def get_active_window():
    window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return window

current_window = get_active_window()

while True:
    exists = False
    active_window_name = get_active_window()
    for activity in activity_list:
        activity_name = activity['name']
        if active_window_name == activity_name:
            exists = True

    if active_window_name != current_window:
        hour = datetime.now().hour* 3600
        minute = datetime.now().minute* 60
        sec = datetime.now().second


        end_time = hour + minitue +sec
        usage = end_time - start_time

        if not exists:
            activity_list.append({'name' : current_window, 'usage' : usage})
        else:
            # some erros here and there with the data collection.
            # other than that can finally collect data
            for activity in activity_list:
                if activity['name'] == current_window:
                    activity['usage'] = activity['usage'] + usage

        current_window = active_window_name
        start_time = hour + minute + sec



    print(activity_list)
    time.sleep(1)

