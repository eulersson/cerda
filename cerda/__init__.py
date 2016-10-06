import datetime
import logging
import os
import signal
import sys

import coloredlogs
import dropbox

from cerda.errors import CerdaError
from cerda.farm_watcher import FarmWatcher
from cerda.helpers import dropbox_setup, parse_args

def setup_logging():
    """Sets up a logger with two handlers. The santard output handler will print
    info logger messages to the terminal using colors. The file handler will
    print debug messages to a file under ~/.cerda/logs/

    Returns:
        logger (logging.Logger): Initialized with all the right handles.
    """
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
    logger.info(
        "I created a log file: %s under ~/.cerda/logs, If you got any problems speak to Ramon "
        "(blanquer.ramon@gmail.com) or send him that file." % log_filename
    )

    return logger


def signal_handler(signal, frame):
    logger.info("\nOh, you leaving? See you soon! :D")
    sys.exit(0)

try:  # so sphinx does not complain...
    logger = setup_logging()
except:
    pass

def main():    
    if '-h' in sys.argv or '--help' in sys.argv:
        # Just show the help.
        parse_args(sys.argv[1:])
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    (user, password, source, target, email, count, client, every) = parse_args(sys.argv[1:])

    make_integer_if_exists_else_none = lambda x: int(x) if x is not None else None

    every, count = map(make_integer_if_exists_else_none, [every, count])

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

    if email and count:
        notify = (email, count)
    else:
        notify = None

    watcher = FarmWatcher(user, password, source, target, notify=notify, client=client)
    watcher.run(every)
