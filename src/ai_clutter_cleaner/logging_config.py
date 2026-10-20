"""Logging configuration."""

import logging
import sys


def setup_logging(log_level: int = logging.INFO) -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
