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

    if not (args.source and args.destination):
        logger.error("The --source and --destination flags are needed. Check 'watchfarm --help'")
        return

    if args.dropbox:
        logger.info("You will need to log in into dropbox")
        dropbox_setup()

    abs_dest_path = os.path.expanduser(os.path.join('~', args.destination))
    if not os.path.exists(abs_dest_path) and not args.dropbox:
        logger.warning("Seems that %s does not exist on your local drive. Creating it... ", abs_dest_path)
        os.makedirs(abs_dest_path)
        logger.info("Folder structure created, you are welcome :)")

    password = getpass.getpass()
    watcher = FarmWatcher(getpass.getuser(), password, args.source, args.destination)
    watcher.run(2)
