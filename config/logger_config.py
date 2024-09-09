import logging
import os
from datetime import datetime


class TodayFileHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()
        self._today = None
        self._filename = None

    def emit(self, record):
        today = datetime.now().date()
        if today != self._today:
            self._today = today
            os.makedirs('logs', exist_ok=True)
            self._filename = f'logs/{today}.log'
            self.stream = open(self._filename, 'a')
        super().emit(record)


file_handler = TodayFileHandler()
file_handler.setFormatter(
    logging.Formatter('%(asctime)s %(levelname)s %(message)s')
)
logging.basicConfig(
    format='%(name)s %(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        file_handler
    ]
)

logger = logging.getLogger(__name__)


def new_logger(name: str):
    return logging.getLogger(name)
