import logging
import sys

from connect4cube.connect4.connect4 import Connect4Demo, Connect4Human
from connect4cube.rainbow.rainbow import Rainbow

LOG = logging.getLogger(__name__)
LOG.debug("sys.path=" + ":".join(sys.path))

if __name__ == "__main__":
    apps = [Rainbow(), Connect4Demo(), Connect4Human()]
    while True:
        for app in apps:
            app.run()
