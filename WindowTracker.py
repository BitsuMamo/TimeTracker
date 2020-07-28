#TODO Add json parsing and logic
from win32gui import GetWindowText, GetForegroundWindow
import time
from datetime import datetime
class WindowTracker(object):
    def __init__(self, window, delayTime, browsers, unWanted, timeUsed):
        self.window = window
        self.delayTime = delayTime
        self.browsers = browsers
        self.unWanted = unWanted
        self.timeUsed = timeUsed

    def isBrowser(self):
        for browser in self.browsers:
            if self.window.endswith(browser):
                self.window = self.window.split('-')
                self.window = self.window[-2].strip()
    #TODO this shit ain't working
    def isWanted(self):
        for item in self.unWanted:
            if str(self.window).strip() != str(item).strip():
                self.timeUsed[self.window] = datetime.now().second

    def run(self):
        while True:
            self.window = GetWindowText(GetForegroundWindow())
            self.isBrowser()
            self.isWanted()
            print(self.timeUsed)
            time.sleep(self.delayTime)

unWanted = ['New Tab', 'Google Search', 'Task Manager', ' ', '']
browsers = ['Brave', 'Chrome', 'FireFox']
timeUsed = {}

w = WindowTracker(GetWindowText(GetForegroundWindow()), 2, browsers, unWanted, timeUsed)
w.run()
