import logging
import os

logger = logging.getLogger(__name__)


def main():
    logger.info("test1")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
