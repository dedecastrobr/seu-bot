import logging
from logging.handlers import RotatingFileHandler
import os
from utils import config

class Logger:

    def __init__(self, name):
        
        log_directory = config.get("logs_folder")
        os.makedirs(log_directory, exist_ok=True)

        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            # Create the log file inside /logs
            log_file_path = os.path.join(log_directory, f"{name}.log")
            file_handler = RotatingFileHandler(log_file_path, maxBytes=1000000)
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