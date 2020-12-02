import logging
import json
import sys

with open("config.json", 'r') as file:
    config = json.load(file)

logger = logging
logger.basicConfig(stream=sys.stdout, format=config['LOG_FORMAT'], level=logging.INFO, datefmt="%H:%M:%S")
