import argparse
import getpass
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
from helpers import dropbox_setup
from errors import CerdaError

p_des = "Process credentials and paths for farm watcher"
s_des = "Remote location path (relative to home) where the frames get generated."
t_des = "Destination location path where you would like the frames to get sent to."
d_des = "Will send the files to the root path of your dropbox account."
m_des = "Email address to send notification to after -c frames have been rendered."
c_des = "At this numer of frames, send an email to the address specified with -m flag."
e_des = "How often to check for frames dropped (in seconds)"

def parse_args(args):
    parser = argparse.ArgumentParser(description=p_des)
    parser.add_argument('-s', '--source', help=s_des, required=True)
    parser.add_argument('-t', '--target', help=t_des, required=True)
    parser.add_argument('-dbox', '--dropbox', help=d_des, action='store_true')
    parser.add_argument('-m', '--email', help=m_des)
    parser.add_argument('-c', '--count', help=c_des)
    parser.add_argument('-e', '--every', help=e_des, type=int, default=5)
    args = parser.parse_args(args)

    if args.email or args.count:
        if not (args.email and args.count):
            logger.error("-c (--count) and -m (--mail) both need to be passed, not just one.")
            raise CerdaError

        else:
            logger.debug("mail is: %s", args.email)
            logger.debug("count is: %s", args.count)

    # validation on args.source

    # validation on args.target

    # validation on args.email

    # validation on args.count

    # validation on every

    client = None
    if args.dropbox:
        client = dropbox_setup()

    user = getpass.getuser()
    password = getpass.getpass("Password for %s: " % user)

    return (user, password, args.source, args.target, args.email, int(args.count), client, args.every)

def main():
    (user, password, source, target, email, count, client, every) = parse_args(sys.argv[1:])
    watcher = FarmWatcher(user, password, source, target, notify=(email, count), client=client)
    watcher.run(every)
