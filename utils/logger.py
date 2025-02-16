import logging
from logging.handlers import RotatingFileHandler

class Logger:

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            file_handler = RotatingFileHandler(f"{name}.log", maxBytes=1000000)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)