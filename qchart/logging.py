import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_log_directory():
    log_directory = Path(config['logging']['directory'])
    log_directory.mkdir(parents=True, exist_ok=True)
    return log_directory

def create_logger(logger_name):
    filename = Path(get_log_directory(), f'{logger_name}.log')
    logger = logging.getLogger(logger_name)
    log_handler = RotatingFileHandler(filename, maxBytes=1048576, backupCount=5)
    log_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s: '
            '%(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )
    )
    log_level = logging.getLevelName(config['logging']['level'])
    logger.setLevel(log_level)
    logger.addHandler(log_handler)
    return logger
