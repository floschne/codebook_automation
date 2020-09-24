import logging.config

import os

logging.config.fileConfig(os.path.join(os.getcwd(), 'logger', 'logging.conf'))

# create logger
api_logger = logging.getLogger('Codebook_Automation_API')
backend_logger = logging.getLogger('Codebook_Automation_Backend')
