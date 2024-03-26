# logging_config.py

import logging
import os

'''
    Handles the creation of multiples log files depending on the name of the api

'''

def configure_api_logging(api_name: str, append_logs:bool = False):

    log_dir = os.getenv('LOGS_DIR', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f'{api_name}.log')
    
    api_logger = logging.getLogger(api_name)
    api_logger.setLevel(logging.ERROR)
    api_logger.propagate = False
    
    if append_logs:
        file_mode = 'a'
    else:  
        file_mode = 'w'

    handler = logging.FileHandler(log_file, mode=file_mode)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    api_logger.addHandler(handler)
    
    return api_logger