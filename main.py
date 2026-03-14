import logging

from logging import config
from src.common.config import LOGGING_CONFIG

config.dictConfig(LOGGING_CONFIG)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    ...
