#TODO: Add json parsing and logic
#TODO: Add a filter to eliminate unessecary windows eg: New Tab, TaskManager...
#TODO: Add filter to check if same app with different windows
# dataHolder just temp till I know Json
from FilterList import FilterList as Fl
from win32gui import GetWindowText, GetForegroundWindow
import time
from datetime import datetime

class WindowTracker(object):

    def __init__(self, browserList, dataHolder, delayTime):
        self.browserList = browserList
        self.dataHolder = dataHolder
        self.delayTime = delayTime

    def checkIfBrowser(self, window):
        for browser in self.browserList:
            if window.endswith(browser):
                window = window.split('-')
                return window[-2]
        return window
    def run(self):
        while True:
            activeWindow = GetWindowText(GetForegroundWindow())
            activeWindow = self.checkIfBrowser(activeWindow)
            self.dataHolder[activeWindow] = datetime.now().second
            print(self.dataHolder)
            time.sleep(self.delayTime)


dataHolder = {}
w = WindowTracker(Fl.browsers, dataHolder, 1)
w.run()
