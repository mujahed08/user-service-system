import logging
import logging.config
import yaml

"""
with open('USER_SERVICE_SYSTEM/log4py.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f.read())
    logging.config.dictConfig(CONFIG)
"""

def get_logger(logger_name):
    logger_instance = logging.getLogger(logger_name)
    return logger_instance
