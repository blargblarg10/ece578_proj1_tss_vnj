"""
logger_config.py

Description:
    The logger_config module sets up the logger for the simulation.
    
Responsibilities:
    - Sets up the logger.
    - Provides the logger instance to other modules.

Usage:
    - The logger instance is imported by other modules.
"""
import logging
import os

def setup_logger(debug=False, log_file='sim/output/simulation_log.txt'):
    log_level = logging.DEBUG if debug else logging.INFO

    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logging.basicConfig(filename=log_file, level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')
    logger = logging.getLogger()
    return logger

logger = setup_logger()
