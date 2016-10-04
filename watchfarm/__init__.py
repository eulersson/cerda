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
    p_des = "Process credentials and paths for farm watcher"
    s_des = "Remote location path (relative to home) where the frames get generated."
    t_des = "Destination location path where you would like the frames to get sent to."
    d_des = "Will send the files to the root path of your dropbox account."
    e_des = "How often to check for frames dropped (in seconds)"

    parser = argparse.ArgumentParser(description=p_des)
    parser.add_argument('-s', '--source', help=s_des, required=True)
    parser.add_argument('-t', '--target', help=t_des, required=True)
    parser.add_argument('-db', '--dropbox', help=d_des, action='store_true')
    parser.add_argument('-e', '--every', help=s_des, type=int, default=5)
    args = parser.parse_args()

    if args.dropbox:
        client = dropbox_setup()

    password = getpass.getpass('Enter password:')
    watcher = FarmWatcher(getpass.getuser(), password, args.source, args.target, client=client)
    watcher.run(args.every)
