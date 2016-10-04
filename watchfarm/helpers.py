import os
import logging

import dropbox

logger = logging.getLogger("watchfarm")

def dropbox_setup():
    token_path = os.path.join(os.path.expanduser(os.path.sep.join(['~', '.watchfarm'])), 'dbox_token.txt')
    logger.debug("Token location: %s", token_path)

    APP_KEY = 'gpf11zjrtp5od4x'
    APP_SECRET = 'cyk4k6zgmraajy7'

    logger.debug("Does token file exist on disk?")

    if os.path.isfile(token_path):
        logger.debug("YES! Opening token file...")

        token_file = open(token_path)
        access_token = token_file.read()
        token_file.close()

    else:
        logger.debug("NO! Need to create one.")

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
    logger.info("Oh, hello %s", client.account_info()['display_name'])
    return client

def get_abs_form_rel(rel_dir, username):
    return os.path.join(
        '/',
        os.path.join(
            'home',
            username,
            *rel_dir.split('/')
        )
    )