import os
import logging

import dropbox

logger = logging.getLogger("watchfarm")

def dropbox_setup():
    logger.warn("Might not be fully functioning yet...")
    app_key = 'gpf11zjrtp5od4x'
    app_secret = 'cyk4k6zgmraajy7'

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    authorize_url = flow.start()

    logger.info("1. Go to: %s", authorize_url)
    logger.info("2. Click 'Allow' (you might have to log in first).")
    logger.info("3. Copy the authorization code.")

    code = raw_input("Enter the authorization code here: ").strip()

    access_token, user_id = flow.finish(code)

    client = dropbox.client.DropboxClient(access_token)
    print 'linked acocunt: ', client.account_info()

def get_abs_form_rel(rel_rem_dir, username):
    return os.path.join(
        '/',
        os.path.join(
            'home',
            username,
            *rel_rem_dir.split('/')
        )
    )