import logging
import os
import sys

import datetime

import coloredlogs
import dropbox

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Colored stream handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

stream_formatter = coloredlogs.ColoredFormatter(fmt='%(asctime)s %(levelname)s %(message)s')
ch.setFormatter(stream_formatter)

# File handler
log_filename = datetime.datetime.utcnow().strftime("cerda.%Y%m%d-%H%M%S.log")
logs_dir = os.path.expanduser(os.path.sep.join(['~', '.cerda', 'logs']))

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

fh = logging.FileHandler(os.path.join(logs_dir, log_filename))
fh.setLevel(logging.DEBUG)

file_formatter = logging.Formatter(fmt='[%(levelname)s]%(name)s: %(message)s')
fh.setFormatter(file_formatter)

# Add handlers
logger.addHandler(ch)
logger.addHandler(fh)

from farm_watcher import FarmWatcher
from helpers import dropbox_setup, parse_args
from errors import CerdaError

def main():
    logger.info("Hey I am Cerda, your render farm frame-transfering assistant!")
    (user, password, source, target, email, count, client, every) = parse_args(sys.argv[1:])
    watcher = FarmWatcher(user, password, source, target, notify=(email, count), client=client)
    watcher.run(every)
