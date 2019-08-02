import logging
import sys

logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))


def main():
    print("now we're talking!")


if __name__ == "__main__":
    main()  # dear intellij: simply give me a quick play button here :)
