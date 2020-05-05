import logging.config

import os

logging.config.fileConfig(os.path.join(os.getcwd(), 'api', 'logger', 'logging.conf'))

# create logger
logger = logging.getLogger('Document_Analysis_API')
