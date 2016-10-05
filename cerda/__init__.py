import logging
import os
import sys
import signal

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

def signal_handler(signal, frame):
    logger.info("\nOh, you leaving? See you soon! :D")
    sys.exit(0)

def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        # Just show the help.
        parse_args(sys.argv[1:])
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print "\033[38;5;213m                                     `--:::--.                  `os/        \033[0m"
    print "\033[38;5;213m                                     yo+//+++osso+/:/+++++++/:.`y/:ss       \033[0m"
    print "\033[38;5;213m                                     d:-::::/+ossys+:--------/oyss/:y+      \033[0m"
    print "\033[38;5;213m                           .:+ossssssN::::::/syo/::------.......-/ss/d-     \033[0m"
    print "\033[38;5;213m                       `/syso/:-----:d::::/sy+:::----------.......-:ods     \033[0m"
    print "\033[38;5;213m                    `/yyo/:---------:h+::oh+::::------/:--------..--+oh.    \033[0m"
    print "\033[38;5;213m                  `ohs/::--.......--:so:sy/::::------+NN+----------:MN/y-   \033[0m"
    print "\033[38;5;213m         .--`   `+ho/::--..........-:+yoh/:::::------sMMy-----------mN::d`  \033[0m"
    print "\033[38;5;213m      `.yy//oo..hy/::--............-::hd/:::::-------/mm+----:++ooo+oo:-o+  \033[0m"
    print "\033[38;5;213m     +ssNss  .ymo::---.............:::hs::::::---------:--:oss+/:::::/+o+y  \033[0m"
    print "\033[38;5;213m    -o -dss   ds:::--.............-:::m/::::::-----------oyo//----.....-/y/ \033[0m"
    print "\033[38;5;213m    `-  `.   /d:::--..............-:::m:::::::---------:yy/+/---:/:--..-::d`\033[0m"
    print "\033[38;5;213m             yo:::--.............-::::m/:::::---------:od::o---+ddd/--:hdsy.\033[0m"
    print "\033[38;5;213m             d/:::-...........----::::ho::::::-------::ys::+---smdm+--/mmsd`\033[0m"
    print "\033[38;5;213m             d+:::-........--------:::+d/:::::--------:oh::o---:+so----+oy+ \033[0m"
    print "\033[38;5;213m             do:::---.-------------::::oh/:::::--------:yy++/---------:oy:  \033[0m"
    print "\033[38;5;213m             yy::-------------------::::oho:::::---------/syys+///+oyyo:`   \033[0m"
    print "\033[38;5;213m             /d::---------------------:::/syo/:::-----------:///+oydo`      \033[0m"
    print "\033[38;5;213m             .N::-----------------------:::/ohyo+/:---------::+oso:`        \033[0m"
    print "\033[38;5;213m              m+:--------:----------+:-------sddsssssssssssso+/-            \033[0m"
    print "\033[38;5;213m              sy:-------:s//:::----:y:-------dss:::::::+o`                  \033[0m"
    print "\033[38;5;213m              .m+:------hoshhyysssyyh:-------moy:::----y/   !\________      \033[0m"
    print "\033[38;5;213m               oNy+::--ss  :s//+++d-m:------:h:h::----:d`  / OINK!    \     \033[0m"
    print "\033[38;5;213m                yNmmdhdd`   dmdhhd- m/------y/`Nys+++od:  /     OINK!  |    \033[0m"
    print "\033[38;5;213m                `ymmmmd`    .mdmm:  sy/:::/oh  yNmmNmm/   | I'm Cerda  |    \033[0m"
    print "\033[38;5;213m                  -`os`      -`.`   `mmmmmmm.  .mm+hh-     \_____:D _ /     \033[0m"
    print "\033[38;5;213m                                     -mmmhd:                                \033[0m"
    print "\033[38;5;213m                                      `/:                                   \033[0m"

    logger.info("Hey I am Cerda, your render farm frame-transfering assistant!")
    logger.info("From the options you passed I guess you want to do the following:")
    logger.info(
        "I created a log file: %s, If you got any problems speak to Ramon "
        "(blanquer.ramon@gmail.com) or send him that file." % log_filename
    )
    (user, password, source, target, email, count, client, every) = parse_args(sys.argv[1:])
    logger.info("I will parse your command. Let me recap what you want to do:")
    msg =  "\n\n- Watch for frames that drop in /home/%s/%s under the renderfarm location\n" % (user, source)

    if client is not None:
        msg += "- Upload the rendered frames to %s on your dropbox home\n" % target
    else:
        msg += "- Transfer the frames to /home/%s/%s under your local account\n" % (user, target)

    if email is not None:
        msg += "- To send an email to %s after %d frames have been dropped\n" % (email, count)

    if every is not None:
        msg += "- To check for new rendered frames every %d seconds\n" % (every)

    logger.info(msg)

    answer = raw_input("Did I get it right? (y/n) ")

    if answer in ['yes', 'y', 'Y', 'Yes', 'YES']:
        logger.info("GREAT! I will proceed")
    else:
        logger.error("Shit I'm sorry. I'll get you out of here. Bye.")
        sys.exit(0)

    watcher = FarmWatcher(user, password, source, target, notify=(email, count), client=client)
    watcher.run(every)
