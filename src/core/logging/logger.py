import logging


class CustomStreamHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()
        fmt = "%(levelname)s - %(asctime)s - %(module)s/%(filename)s - %(funcName)s - %(lineno)d: %(message)s"
        formatter = logging.Formatter(fmt)
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        print(msg)


available_loggers = [
    "izr-api",
    "alembic",
    "uvicorn",
    "gunicorn.error",
    "gunicorn.access",
]
for logger_name in available_loggers:
    logger = logging.getLogger(logger_name)
    logger.addHandler(CustomStreamHandler())
    logger.setLevel(logging.INFO)

logger = logging.getLogger("izr-api")
