import argparse
import getpass
import logging
import os
import re
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import dropbox

from cerda.errors import CerdaError

logger = logging.getLogger(__name__)

def dropbox_setup():
    """Sets up a Dropbox client object that will be used to put the files on
    the Dropbox account.

    The first time it is run it will ask the user to allow this app through the
    browser. The user will paste the authorization code and a token will get
    generated. I am storing it under ~/.cerda/dbox_token.txt. This does not
    contain any username or passwords, so the user is safe.

    Returns:
        obj: Initialized Dropbox client object

    """
    token_path = os.path.join(
        os.path.expanduser(
            os.path.sep.join(['~', '.cerda'])
        ),
        'dbox_token.txt'
    )

    logger.debug("Token location: %s", token_path)

    APP_KEY = 'g00qsmj1c10wc7o'
    APP_SECRET = 'szjgn373r8xbnxb'

    logger.debug("Does token file exist on disk?")

    if os.path.isfile(token_path):
        logger.debug("YES! Opening token file...")

        token_file = open(token_path)
        access_token = token_file.read()
        token_file.close()

    else:
        logger.info(
            "You will have to give me permissions to upload stuff to your"
            "Dropbox account. Don't worry it's just a one time thing."
        )

        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        authorize_url = flow.start()

        logger.info("1. Go to: %s", authorize_url)
        logger.info("2. Click 'Allow' (you might have to log in first).")
        logger.info("3. Copy the authorization code.")

        code = raw_input("Enter the authorization code here: ").strip()

        access_token, user_id = flow.finish(code)

        logger.debug("Access token is... %s", access_token)

        logger.debug("Writing access token's key and secret to file...")

        token_folder = os.path.dirname(token_path)

        if not os.path.exists(token_folder):
            os.makedirs(token_folder)        

        token_file = open(token_path, 'w')
        token_file.write(access_token)
        token_file.close()

    client = dropbox.client.DropboxClient(access_token)

    try:
        logger.info(
            "Yay! %s, I just hooked to your Dropbox account!",
            client.account_info()['display_name']
        )

    except dropbox.rest.ErrorResponse:
        os.remove(token_path)
        CerdaError("Something went wrong. I deleted the token. Try again.")

    return client

def email_sender(email_address, processed_items):
    """Given an email and the list of rendered items it sends an email using
    Google's SMTP servers. The email will come from cerdancca@gmail.com.

    Args:
        email_address (str): address to send the email to.
        processed_items (list): list of rendered item names.

    """
    processed_items = map(lambda x: str(x), processed_items)

    logger.debug("Preparing email for %s", email_address)
    logger.debug("Processed items are %s", processed_items)
    
    fromaddr = "cerda.ncca@gmail.com"
    toaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "cerda: Report"

    body = "Renders are finished!\n%s" % processed_items

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "NCCA2016cerda")
    text = msg.as_string()

    try:
        logger.info("Sending an email to %s", toaddr)
        server.sendmail(fromaddr, toaddr, text)
    except:
        logger.error("Couldn't send an email. Check the logs under ~/.cerda/logs/")
    server.quit()

def get_abs_form_rel(rel_dir, username):
    """Given a relative folder it expands the current user home folder thus
    constructing an absolute path.

    Args:
        rel_dir (str): relative path.
        username (str): self explanatory.

    Returns:
        str: Absolute path.

    """
    return os.path.join(
        '/',
        os.path.join(
            'home',
            username,
            *rel_dir.split('/')
        )
    )

# Descriptions for the parser
p_des = "An NCCA render farm collector."
s_des = "Remote location path (relative to home) where the frames get generated."
t_des = "Destination location path where you would like the frames to get sent to."
d_des = "Will send the files to the root path of your dropbox account."
m_des = "Email address to send notification to after -c frames have been rendered."
c_des = "At this numer of frames, send an email to the address specified with -m flag."
e_des = "How often to check for frames dropped (in seconds)"
epilog = ("Examples: \n\n"
          "My renderfarm is rendering out the frames at"
          "/home/i7243466/project1/render on the tete server. I want the frames "
          "to get transfered to my Dropbox account under /some/folder and when "
          "it has finished rendering, which means 20 frames get collected, send "
          "me an email notification:\n\n"
          "\t$ cerda project1/render some/folder --dropbox --email blanquer.ramon@gmail.com --count 20\n"
          "\nor\n"
          "\t$ cerda project1/render rendered/frames -dbox -e blanquer.ramon@gmail.com -c 20\n")

def parse_args(args):
    """Parsing and validation of all the user supplied arguments.

    It will make sure that if user passes email or count passes both, as both
    are needed. Also will validate the time delay for checking for new frames as
    it cannot be negative, and same for the count value, it doesn't make sense
    values of 0 or lower.

    Args:
        args (list): list containing a representation of the command typed by
            the user. Something like ['-s', 'source/path', '-t', 'target/path',
            '-dbox']

    Returns:
        tuple: a tuple with the parsed username (string), password (string),
        relative source and target paths (string), email, count (int),
        client (dropbox.client.DropboxClient), every (int).

    """

    parser = argparse.ArgumentParser(description=p_des, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source', help=s_des)
    parser.add_argument('target', help=t_des)
    parser.add_argument('-dbox', '--dropbox', help=d_des, action='store_true')
    parser.add_argument('-e', '--email', help=m_des)
    parser.add_argument('-c', '--count', help=c_des, type=int)
    parser.add_argument('-r', '--every', help=e_des, type=int, default=5)
    args = parser.parse_args(args)

    # Validate email and frame count at which to send email
    if args.email or args.count:
        if not (args.email and args.count is not None):
            logger.error("-c (--count) and -e (--mail) both need to be passed, not just one.")
            raise CerdaError("Exiting. Just try again passing both flags. OINK!")

        else:
            logger.debug("Email passed in is: %s", args.email)
            logger.debug("Frame count for sending email is: %s", args.count)
            EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
            if not EMAIL_REGEX.match(args.email):
                raise CerdaError("You entered an invalid email. Typo maybe?")

    # Validation on -s / --source to be implemented

    # validation on -t / --target to be implemented

    # Validation on -e / --every
    if args.every < 1:
        raise CerdaError(
            "No 0 or negative numbers, I know you want the renders ASAP, "
            "just chill out mate."
        )

    # Validation on -c / --count
    if args.count is not None and args.count < 1:
        raise CerdaError(
            "You want to be sent an email after %s frames have been rendered?"
            "That does not make any sense..." % args.count
        )

    # Dropbox handling
    client = None
    if args.dropbox:
        client = dropbox_setup()

    user = getpass.getuser()
    password = getpass.getpass("Password for %s: " % user)

    return (user, password, args.source, args.target, args.email, args.count, client, args.every)