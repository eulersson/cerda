import argparse
import getpass
import logging
import os

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
from helpers import dropbox_setup

def main():
    p_des = "Process credentials and paths for farm watcher"
    s_des = "Remote location path (relative to home) where the frames get generated."
    t_des = "Destination location path where you would like the frames to get sent to."
    d_des = "Will send the files to the root path of your dropbox account."
    m_des = "Email address to send notification to after -c frames have been rendered."
    c_des = "At this numer of frames, send an email to the address specified with -m flag."
    e_des = "How often to check for frames dropped (in seconds)"

    parser = argparse.ArgumentParser(description=p_des)
    parser.add_argument('-s', '--source', help=s_des, required=True)
    parser.add_argument('-t', '--target', help=t_des, required=True)
    parser.add_argument('-dbox', '--dropbox', help=d_des, action='store_true')
    parser.add_argument('-m', '--mail', help=m_des)
    parser.add_argument('-c', '--count', help=c_des)
    parser.add_argument('-e', '--every', help=e_des, type=int, default=5)
    args = parser.parse_args()

    client = None
    if args.dropbox:
        client = dropbox_setup()

    if args.mail or args.count:
        if not (args.mail and args.count):
            logger.error("-c (--count) and -m (--mail) both need to be passed, not just one.")
            return
        else:
            logger.debug("mail is: %s", args.mail)
            logger.debug("count is: %s", args.count)

    machine_user = getpass.getuser()
    password = getpass.getpass("Password for %s: " % machine_user)

    watcher = FarmWatcher(
        machine_user,
        password,
        args.source,
        args.target,
        notify=(args.mail, int(args.count)),
        client=client
    )
    watcher.run(args.every)
