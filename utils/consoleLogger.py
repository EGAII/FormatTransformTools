import logging


class ConsoleLogger:
    def __init__(self, name):
        self.logger = logging.getLogger('logger')
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)s] - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def getLogger(self):
        return self.logger
