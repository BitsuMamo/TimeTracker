#TODO Add json parsing and logic
import win32gui
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

    def isUnWanted(self):
        for item in self.unWanted:
            if self.window != item:
                self.timeUsed[self.window] = 2

    def run(self):
        while True:
            self.window = GetWindowText(GetForegroundWindow())
            self.isBrowser()
            self.isUnWanted()
            self.timeUsed[self.window] = datetime.now().second
            print(self.timeUsed)
            time.sleep(self.delayTime)

unWanted = ['New Tab', 'Google Search']
browsers = ['Brave', 'Chrome']
timeUsed = {}

w = WindowTracker(GetWindowText(GetForegroundWindow()), 2, browsers, unWanted, timeUsed)
w.run()
