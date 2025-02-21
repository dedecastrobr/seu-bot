import logging
from logging.handlers import RotatingFileHandler
import os
from utils import get_config

class Logger:

    def __init__(self, name):
        try:
            self.config = get_config()
            log_directory = self.config.get("logs_folder")
            os.makedirs(log_directory, exist_ok=True)

            self.logger = logging.getLogger(name)
            if not self.logger.handlers:
                self.logger.setLevel(self.config.get("log_level").upper())
                formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

                log_file_path = os.path.join(log_directory, f"{name}.log")
                file_handler = RotatingFileHandler(log_file_path, maxBytes=1000000)
                file_handler.setFormatter(formatter)

                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)

                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)
        except KeyError as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Error initializing logger: {e}") from e

    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)