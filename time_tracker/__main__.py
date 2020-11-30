from win32 import win32gui
from datetime import datetime
from time import sleep
from typing import Optional, List, Tuple

from . import serializer


def get_app_name() -> str:
    app_name:List[str] = win32gui.GetWindowText(win32gui.GetForegroundWindow()).split("-")
    app_name = [name.strip() for name in app_name]
    web_browsers = ["Google Chrome", "Mozilla Firefox"]
    app = app_name[len(app_name) - 1]
    for browser in web_browsers:
        if browser.lower() == app.lower():
            site = get_name_from_browser(app_name)
            return site if site else browser
    return app_name[len(app_name) - 1]

# Checks if the site is a social media site, returns none if not
def get_name_from_browser(app_name: list) -> Optional[str]:
    social_media = ["Reddit", "Twitter", "Facebook", "Instagram"]
    for site in social_media:
        if site.lower() in [entry.lower() for entry in app_name]:
            return site
    return None


# TODO look into threads for main while loop
def track_activity() -> None:
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
                activity_dict.append((current_app, start_date, datetime.now()))
                start_date = datetime.now()
                current_app = active_app
            sleep(1)
    except KeyboardInterrupt:
        activity_dict.append((current_app, start_date, datetime.now()))
        serializer.save_to_db(activity_dict)
        display_all_activity()
        serializer.close_db_connection()

        # Temporary function. Should be removed
def display_all_activity():
    for data in serializer.get_all_data():
        print(
            f"{data[0]}, started at: {data[1].isoformat()}, ended at: {data[2].isoformat()}"
        )


if __name__ == "__main__":
    track_activity()
