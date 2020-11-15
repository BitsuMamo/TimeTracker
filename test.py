import win32gui
from datetime import datetime
from time import sleep

def get_app_name():
    app_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    app_name = app_name.split('-')

    # Striping spaces of the ends of the strings
    for index in range(len(app_name)):
        app_name[index] = app_name[index].strip()

    web_browsers = ['Google Chrome', 'Mozilla Firefox']
    exceptions = []
    if app_name[len(app_name) - 1] not in exceptions:
        if app_name[len(app_name) - 1] in web_browsers:
            if ' Google Search ' in app_name:
                app_name = 'Google Search'
            else:
                app_name = app_name[0].strip()
        else:
            app_name = app_name[0]
    else:
        app_name = ''

    return app_name

while True:
    print(get_app_name())
    sleep(3)
