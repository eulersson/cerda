import logging
import os
import sys

import coloredlogs
import dropbox

logger = logging.getLogger('cerda')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = coloredlogs.ColoredFormatter(fmt='%(asctime)s %(levelname)s %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

from farm_watcher import FarmWatcher
from helpers import dropbox_setup, parse_args
from errors import CerdaError

def main():
    (user, password, source, target, email, count, client, every) = parse_args(sys.argv[1:])
    watcher = FarmWatcher(user, password, source, target, notify=(email, count), client=client)
    watcher.run(every)
