import argparse
import getpass
import logging
import os
import re
import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
            "You will have to give me permissions to upload stuff to your "
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


def email_sender(email_address, wd, processed_items, attach_previews=False):
    """Given an email and the list of rendered items it sends an email using
    Google's SMTP servers. The email will come from cerdancca@gmail.com.

    Args:
        email_address (str): address to send the email to.
        wd (str): working directory
        processed_items (list): list of rendered item file names.
        attach_previews (bool): if need to attach preview images

    """
    processed_items = map(lambda x: str(x), processed_items)

    logger.debug("Preparing email for %s", email_address)
    logger.debug("Processed items are %s", processed_items)

    # Email preparation
    fromaddr = "cerda.ncca@gmail.com"
    toaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "cerda: Report"

    body = "Renders are finished!\n%s" % processed_items

    msg.attach(MIMEText(body, 'plain'))

    if attach_previews:
        processed_items = map(lambda p: os.path.join(wd, os.path.splitext(p)[0]+'.preview.png'), processed_items)
        logger.info("Attaching these items: %s" % processed_items)

        logger.debug("PROCESSED ITEMS: %s" % processed_items)

        # Attachements
        for f in processed_items or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(f)
                )
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                msg.attach(part)

    # Sending email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "NCCA2016cerda")
    text = msg.as_string()

    try:
        logger.info("Sending an email to %s", toaddr)
        server.sendmail(fromaddr, toaddr, text)
    except:
        logger.error("Couldn't send an email. Check the logs under ~/.cerda/logs/")

    # Clean up the previews as they have been sent already
    if attach_previews:
        for preview in processed_items:
            os.remove(preview)

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
t_des = "Custom file extensions to mark for transfering. I.e. -t tiff,exr,obj"
epilog = ("Examples: \n\n"
          "My renderfarm is rendering out the frames at"
          "/home/i7243466/project1/render on the tete server. I want the frames "
          "to get transfered to my Dropbox account under /some/folder and when "
          "it has finished rendering, which means 20 frames get collected, send "
          "me an email notification:\n\n"
          "\t$ cerda project1/render some/folder --dropbox --email blanquer.ramon@gmail.com --count 20\n"
          "\nor\n"
          "\t$ cerda project1/render rendered/frames -dbox -e blanquer.ramon@gmail.com -c 20\n")


def is_render_finished(sftp, item):
    """Checks if the render has been finished by checking if there is
    a file with the same name with .mantra_checkpoint appended to it.

    Args:
        sftp (obj): sftp connection object.
        item (str): name of file

    Returns:
        bool: Whether render is completed or not
    """
    logger.info("Checking if render is finished for %s" % item)
    listed_files = sftp.listdir()

    if item + '.mantra_checkpoint' in listed_files:
        return False
    else:
        return True


def parse_args(args):
    """Parsing and validation of all the user supplied arguments.

    It will make sure that if user passes email or count passes both, as both
    are needed. Also will validate the time delay for checking for new frames as
    it cannot be negative, and same for the count value, it doesn't make sense
    values of 0 or lower.

    Args:
        args (list): list containing a representation of the command typed by
            the user.

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
    parser.add_argument('-t', '--customTypes', help=t_des)
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

    # Validation on source and target folders
    if args.source is None or args.target is None:
        raise CerdaError("Source and target folders must be specified.")

    # Both source and target mus be valid paths
    if not all(map(lambda path: validate_path(path), [args.source, args.target])):
        raise CerdaError(
            "Don't prepend slash (as it was absolute path) or append them. "
            "All the paths will be parsed and understood as relative to home: "
            "Example: hello/world --> /home/{user}/hello/world folder"
            "NOT: /hello/world, /hello/world/, hello/world/..."
        )

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

    # Validation on custom types
    custom_types = []
    if args.customTypes:
        if ' ' in args.customTypes:
            raise CerdaError(
                "Specify the types in a comma separated list of like extensions. "
                "Example: --customTypes png,jpeg,tiff"
            )
        custom_types = args.customTypes.split(',')
        if not all(map(lambda x: not x.startswith('.'), custom_types)):
            raise CerdaError(
                "Don't write dots when defining file extensions please.\n"
                "\tGOOD: --customTypes png,jpeg,tiff\n"
                "\tBAD: --customTypes .png,.jpeg,.tiff"
            )

        custom_types = map(lambda x: '.'+x, custom_types)

    # Dropbox handling
    client = None
    if args.dropbox:
        client = dropbox_setup()

    user = getpass.getuser()
    password = getpass.getpass("Password for %s: " % user)

    return user, password, args.source, args.target, args.email, args.count, client, args.every, custom_types


def validate_path(path):
    """Validates the input path for source or targets given a relative path string.

    Args:
        path (string): relative path

    Returns:
        bool: success.
    """
    if path.endswith('/') or path.startswith('/'):
        return False

    regex = re.compile(r'[A-Za-z-_0-9]+(?:/[A-Za-z-_0-9]+)*')
    result = regex.match(path)

    # If not matching the full string something is wrong
    if not result.regs[0][1] == len(path):
        return False

    return True
