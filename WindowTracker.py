# TODO: Add json parsing and storing.

# Imports
import win32gui
import time
import datetime

# Function to get the current window
def get_active_winodw():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

# Varibale intitializations
current_window = get_active_winodw()
activity_list = []

# Main Code
while True:

    exists = False
    activity = {}

    # Intializes list if it is empty or first time.
    if len(activity_list) == 0:
        activity = {'name': current_window, 'usage': 1}

    if current_window != get_active_winodw():
        # TODO: Add something to track time with.

        # This checks if the activity exists
        for activities in activity_list:
            if activities['name'] == current_window:
                    exists = True
        # Adds activities to the list
        if exists:
            for activities in activity_list:
                if activities['name'] == current_window:
                        activities['usage'] = activities['usage'] + 1
        else:
            activity = {'name': current_window, 'usage': 1}
            activity_list.append(activity)

        current_window = get_active_winodw()

    print(activity_list)
    time.sleep(2)
