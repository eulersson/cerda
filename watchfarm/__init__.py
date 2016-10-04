import argparse
import getpass
import logging
import os

import coloredlogs
import dropbox

logger = logging.getLogger('watchfarm')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = coloredlogs.ColoredFormatter(fmt='%(asctime)s %(levelname)s %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

from farm_watcher import FarmWatcher
from helpers import dropbox_setup

def main():
    parser = argparse.ArgumentParser(description="Process credentials and paths for farm watcher")
    parser.add_argument('-s', '--source', help="Remote location path (relative to home) where the frames get generated.")
    parser.add_argument('-d', '--destination', help="Destination location path where you would like the frames to get sent to.")
    parser.add_argument('-db', '--dropbox', help="Will send the files to the root path of your dropbox account.", action='store_true')
    args = parser.parse_args()

    client = None

    if not (args.source and args.destination):
        logger.error("The --source and --destination flags are needed. Check 'watchfarm --help'")
        return

    if args.dropbox:
        client = dropbox_setup()

    password = getpass.getpass()
    watcher = FarmWatcher(getpass.getuser(), password, args.source, args.destination, client=client)
    watcher.run(2)
