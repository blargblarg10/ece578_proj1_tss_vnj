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
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create file handler which logs even debug messages
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(log_level)

    # Create console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger(debug=True)
