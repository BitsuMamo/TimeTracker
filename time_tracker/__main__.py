from win32 import win32gui
from datetime import datetime
from time import sleep
from typing import Dict, List, Tuple

from . import serializer


def get_app_name() -> str:
    app_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    app_name = app_name.split("-")

    # Striping spaces of the ends of the strings
    app_name = [name.strip() for name in app_name]

    web_browsers = ["Google Chrome", "Mozilla Firefox"]
    exceptions = []
    app = app_name[len(app_name) - 1]

    if app in exceptions:
        return ""
    if app in web_browsers:
        return get_name_from_browser(app_name)

    return app_name[len(app_name) - 1]


# Filters name that come from browsers
def get_name_from_browser(app_name: list) -> str:
    exceptions = ["New Tab"]
    for exception in exceptions:
        if exception in app_name:
            return ""
    if "Google Search" in app_name:
        return "Google Search"
    if len(app_name) < 3:
        return app_name[0]

    return app_name[len(app_name) - 2]


def track_activity() -> None:
    # Helper function to save current tracked app into the list
    def log_activity() -> None:
        activity_dict.append((current_app, start_date, datetime.now()))

    current_app = get_app_name()
    start_date = datetime.now()
    activity_dict: List[Tuple[str, datetime, datetime]] = []
    try:
        while True:
            active_app = get_app_name()
            if current_app == "":
                current_app = active_app
                continue
            if current_app != active_app:
                log_activity()
                start_date = datetime.now()
                current_app = active_app
            # Log activity every second
            # sleep(1)
    except KeyboardInterrupt:
        log_activity()
        serializer.save_to_db(activity_dict)
        display_all_activity()
        serializer.close_db_connection()


def display_all_activity():
    for data in serializer.get_all_data():
        print(
            f"{data[0]}, started at: {data[1].isoformat()}, ended at: {data[2].isoformat()}"
        )


if __name__ == "__main__":
    track_activity()
