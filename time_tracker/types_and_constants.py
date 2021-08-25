from typing import Tuple
from datetime import datetime

# Constants

DB_PATH = "activity.db"
DATE_FORMAT = "%Y-%m-%d"
NO_APP = "No apps running"
BASE_COMMAND = "SELECT * FROM activities ORDER BY start_date_iso ASC"

# Types

Record = Tuple[str, datetime, datetime]
