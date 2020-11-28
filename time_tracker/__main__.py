import win32gui

from datetime import datetime
from . import serializer

def get_app_name() -> str:
    app_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    app_name = app_name.split('-')

    # Striping spaces of the ends of the strings
    app_name = [name.strip() for name in app_name]

    web_browsers = ['Google Chrome', 'Mozilla Firefox']
    exceptions = []
    app = app_name[len(app_name) - 1]

    if app in exceptions:
        return ''
    if app in web_browsers:
        return get_name_from_browser(app_name)

    return app_name[len(app_name) -1]


# Filters name that come from browsers 
def get_name_from_browser(app_name: list) -> str:
    exceptions = ['New Tab']
    for exception in exceptions:
        if exception in app_name:
            return ''

    if 'Google Search' in app_name:
        return 'Google Search'

    if len(app_name) < 3:
        return app_name[0]

    return app_name[len(app_name) - 2]


def track_activity() -> None:
    app_activity_list = serializer.load_from_file()
    current_app_name = get_app_name()
    start_time = datetime.now()
    a = datetime.now()

    while True:
        current_date = datetime.now().date()
        current_date_activity = app_activity_list[current_date] if current_date in app_activity_list else {}

        active_app_name = get_app_name()

        if active_app_name != current_app_name and active_app_name != "":
            end_time = datetime.now()
            if current_app_name in current_date_activity:
                current_date_activity[current_app_name] = current_date_activity[current_app_name] + (end_time - start_time).total_seconds()
            else:
                current_date_activity[current_app_name] = (end_time - start_time).total_seconds()

            current_app_name = active_app_name
            start_time = end_time

        app_activity_list[current_date] = current_date_activity

        b = datetime.now()
        if((b-a).total_seconds() > 5):
            serializer.save_to_file(app_activity_list)
            a = b


if __name__ == "__main__":
    track_activity()

