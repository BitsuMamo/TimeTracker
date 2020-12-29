from datetime import datetime
from time_tracker.tracker import AppTracker
from time_tracker.types_and_constants import DATE_FORMAT, NO_APP, Record
from time_tracker.db import AppDB
from typing import Callable, List, Optional


class Activity:

    _db: Optional[AppDB] = None
    listeners: List[Callable] = []

    def __init__(self) -> None:
        self.current_app = NO_APP
        self.current_app_start_time = datetime.now().isoformat()
        self.tracker = AppTracker()
        self.tracker.subscribe(self.app_change)
        self.tracker.start()

    def notify_listeners(self) -> None:
        for func in self.listeners:
            func()

    def subscribe(self, func: Callable) -> None:
        self.listeners.append(func)

    def app_change(self, new_app: str, start_date: str) -> None:
        if self.current_app != NO_APP:
            self.db.save(
                tuple(
                    [
                        self.current_app,
                        datetime.fromisoformat(self.current_app_start_time),
                        datetime.fromisoformat(start_date),
                    ]
                )
            )
        self.current_app = new_app
        self.current_app_start_time = start_date
        self.notify_listeners()

    @property
    def db(self) -> AppDB:
        if not self._db:
            self._db = AppDB()
        return self._db

    def get_activity_by_date(
        self, earliest_cutoff: Optional[str] = None, latest_cutoff: Optional[str] = None
    ) -> List[Record]:
        return self.db.get_data_by_date(
            earliest_date=earliest_cutoff, latest_date=latest_cutoff
        )

    def get_activity_by_app_and_date(self, app: str) -> List[Record]:
        return self.db.get_data_by_app(app)

    def get_activity_by_app_and_date(
        self,
        app: str,
        earliest_date: Optional[str] = None,
        latest_date: Optional[str] = None,
    ):
        return self.db.get_data_by_app_and_date(
            app, earliest_date=earliest_date, latest_date=latest_date
        )

