import win32gui
import win32con

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
    if app in web_browsers:
        return get_name_from_browser(app_name)
    else:
       return app_name[0].strip()

# {date:{name:time}}

# Gets a more accurate form of the tab name
def get_name_from_browser(app_name: list):
    exceptions = ['New Tab']
    for exception in exceptions:
        if exception in app_name:
            return ''

    if 'Google Search' in app_name:
        return 'Google Search'

    return app_name[len(app_name) - 2]


while True:
    print(get_app_name())
    sleep(3)
