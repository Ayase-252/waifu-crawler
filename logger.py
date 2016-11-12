"""
Custom log configuration
"""

import logging

FORMAT = "[%(asctime)s][%(module)s][%(thread)d:%(threadName)s][%(levelname)s]:%(message)s"
logging.basicConfig(filename='run.log', filemode='w', level="DEBUG",format=FORMAT)

def getLogger(logger_path):
    return logging.getLogger(logger_path)
