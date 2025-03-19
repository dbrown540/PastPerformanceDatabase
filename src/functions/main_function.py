"""
main_function.py
Main wrapper for the entire project.
"""

import logging
from src.utils.health_check import run_health_check
from src.utils.logging_helper import setup_logging, log_health_status
from src.config.constants import HTTP_STATUS_CODES

def main():
    """
    Main wrapper for the project
    """

    # * 1. Check health status

    setup_logging()
    logging.info("Starting Past Performance Health Check...")

    # Run pre-execution health check
    systems_healthy, health_status = run_health_check()
    
    log_health_status(systems_healthy, health_status)
