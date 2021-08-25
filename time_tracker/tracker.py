from win32 import win32gui
from datetime import datetime
from time import sleep
from typing import Callable, Optional, List, Iterable, Mapping, Any
from threading import Thread


class AppTracker(Thread):
    current_app: Optional[str] = None

    listeners: List[Callable[[str, str], None]] = []

    def __init__(self) -> None:
        super().__init__(
            group=None,
            target=self.track_activity,
            name="Tracker",
            args=(),
            kwargs={},
            daemon=True,
        )

    def subscribe(self, func: Callable[[str, str], None]):
        self.listeners.append(func)

    def notify_listeners(self) -> None:
        if self.current_app is not None:
            for func in self.listeners:
                func(self.current_app, datetime.now().isoformat())

    def get_app_name(self) -> str:
        app_name: List[str] = win32gui.GetWindowText(
            win32gui.GetForegroundWindow()
        ).split("-")
        app_name = [name.strip() for name in app_name]
        web_browsers = ["Google Chrome", "Mozilla Firefox"]
        app = app_name[len(app_name) - 1]
        for browser in web_browsers:
            if browser.lower() == app.lower():
                site = self.get_name_from_browser(app_name)
                return site if site else browser
        return app_name[len(app_name) - 1]

    # Checks if the site is a social media site, returns none if not
    def get_name_from_browser(self, app_name: list) -> Optional[str]:
        social_media = ["Reddit", "Twitter", "Facebook", "Instagram"]
        for site in social_media:
            if site.lower() in [entry.lower() for entry in app_name]:
                return site
        return None

    def track_activity(self) -> None:
        while len(self.listeners) > 0:
            active_app = self.get_app_name()
            if active_app == self.current_app:
                continue
            else:
                self.current_app = active_app
                self.current_app_start_time = datetime.now().isoformat()
                self.notify_listeners()
            sleep(1)
