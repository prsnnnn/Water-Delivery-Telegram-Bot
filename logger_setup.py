import logging
from datetime import datetime, timezone

class MongoHandler(logging.Handler):
    def __init__(self, collection, level=logging.WARNING):
        super().__init__(level=level)
        self.collection = collection
    def emit(self, record):
        try:
            entry = {
                'timestamp': datetime.now(timezone.utc),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
            }
            if record.exc_info:
                entry['traceback'] = self.format(record)
            self.collection.insert_one(entry)
        except Exception:
            pass


class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[90m',
        'INFO': '\033[36m',
        'WARNING': '\033[33m',
        'ERROR': '\033[31m',
        'CRITICAL': '\033[41m',
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        message = super().format(record)
        return f'{color}{message}{self.RESET}'


def setup_logging(mongo_collection=None):
    logger = logging.getLogger('aquaway')
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(ColorFormatter('%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
                                        datefmt='%H:%M:%S'))
    logger.addHandler(console)
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('../bot.log', maxBytes=5_000_000, backupCount=3, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d | %(message)s'))
    logger.addHandler(file_handler)

    # Mongo — тільки WARNING і вище, щоб не засмічувати базу дебаг-шумом
    if mongo_collection is not None:
        mongo_handler = MongoHandler(mongo_collection, level=logging.WARNING)
        logger.addHandler(mongo_handler)

    return logger