import win32gui
from datetime import datetime
from time import sleep

def get_app_name():
    app_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    app_name = app_name.split('-')

    # Striping spaces of the ends of the strings
    app_name = [name.strip() for name in app_name]

    web_browsers = ['Google Chrome', 'Mozilla Firefox']
    exceptions = []
    app = app_name[len(app_name) - 1]
    if app in exceptions:
        return ''
    if app in web_browsers and 'Google Search' in app_name:
        return 'Google Search'
    else:
       return app_name[0].strip()
# {date:{name:time}}

app_activity_list = {}
current_date_activity = {}
current_app_name = get_app_name()
start_time = datetime.now()


while True:
    current_date = datetime.now().date()
    active_app_name = get_app_name()
    current_date_activity = app_activity_list[current_date] if current_date in app_activity_list else {}

    if active_app_name != current_app_name and active_app_name != "":
        end_time = datetime.now()
        if current_app_name in current_date_activity:
            current_date_activity[current_app_name] = current_date_activity[current_app_name] + (end_time - start_time)
        else:
            current_date_activity[current_app_name] = end_time - start_time

        print(f"{current_app_name} : {str(current_date_activity[current_app_name])}")
        print("============================================================================================")
        current_app_name = active_app_name
        start_time = end_time

    app_activity_list[current_date] = current_date_activity
