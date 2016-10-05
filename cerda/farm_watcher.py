import getpass
import logging
import os
import tempfile
import time

import paramiko 
from paramiko.ssh_exception import AuthenticationException

import pysftp

logger = logging.getLogger(__name__)

from helpers import get_abs_form_rel
from helpers import email_sender

from cerda.errors import CerdaError

class FarmWatcher:
    """Core class of the command line application. Handles or the file input
    output operations."""
    extensions = ['.png', '.exr', '.jpg', '.jpeg', '.txt']
    def __init__(self, username, password, rel_src_dir, rel_tar_dir, host='tete', notify=None, client=None):
        """Farm watcher constructor initializes a state parsed from arguments.

        Args:
            username (str): local machine username. The i number, i.e. i7243466
            password (str): password used to connect to the renderfarm server
            rel_src_dir (str): renderfarm directory where frames will be dropped.
                It needs to be relative to the home folder.
            rel_tar_dir (str): target directory where to place the rendered images.
                It needs to be relative to the home folder. If dropbox option is
                passed it will go to that folder from the dropbox root.
            host (str): host direction to connect to using sftp
            client (dropbox.client.DropboxClient): the Dropbox client instance 
                used to upload the files to the account. It has been initialized
                already. It is ready to go.
        """
        self.__host = host
        self.__username = username
        self.__password = password
        self.__client = client
        self.__processed = []
        self.__notify = bool(notify)
        self.__temporary_folder = None

        report = ("\n\nREPORT\n"
                 "------\n"
                 "- Username: %s\n"
                 "- Relative Source Directory: %s\n"
                 "- Relative Target Directory: %s\n"
                 "- Host: %s\n"
                 "- Notification Email: %s\n"
                 "- Notification Count: %d\n"
                 "- Dropbox Client: %s\n\n") % ( 
                        username,
                        rel_src_dir,
                        rel_tar_dir,
                        host,
                        notify[0],
                        notify[1],
                        str(client)
                    )
        logger.debug(report)
        if self.__notify:
            (self.__email_address, self.__send_mail_after_count) = notify
            self.__current_count = 0

        logger.info("I will send you an email to %s after %s frames have been collected", self.__email_address, self.__send_mail_after_count)

        self.__abs_src_dir, self.__abs_tar_dir = (get_abs_form_rel(x, self.__username) for x in [rel_src_dir, rel_tar_dir])

        logger.debug("Absolute paths: %s | %s", self.__abs_src_dir, self.__abs_tar_dir)

        if self.__client:
            # create temp folder
            self.__temporary_folder = tempfile.mkdtemp()
            logger.debug("A temporary folder has been created: %s", self.__temporary_folder)


        if not self.__client:
            if not os.path.exists(self.__abs_tar_dir):
                logger.warning("Seems that %s does not exist on your local drive. Creating it... ", self.__abs_tar_dir)
                os.makedirs(self.__abs_tar_dir)
                logger.info("Folder structure created, you are welcome :)")

        logger.info("Will be watching for frames at this renderfarm path: %s", self.__abs_src_dir)

    def run(self, delay_seconds):
        try:
            with pysftp.Connection(
                self.__host,
                self.__username,
                password=self.__password
            ) as sftp:
                sftp.chdir(self.__abs_src_dir)
                while True:
                    current_dir = sftp.pwd
                    listed_stuff = sftp.listdir()
                    for item in listed_stuff:
                        if item not in self.__processed and os.path.splitext(item)[1] in self.extensions:
                            logger.info("New item dropped: %s", item)

                            source_absolute_filepath = os.path.join(sftp.pwd, item)
                            target_absolute_filepath =  os.path.join(self.__abs_tar_dir if self.__client else self.__temporary_folder, item)

                            logger.debug("Source absolute filepath: %s", source_absolute_filepath)
                            logger.debug("Target absolute filepath: %s", target_absolute_filepath)

                            logger.debug("Getting the file from server")
                            sftp.get(item, target_absolute_filepath)
                            logger.debug("Removing file from server")
                            sftp.remove(source_absolute_filepath)

                            if self.__client:
                                logger.debug("Need to move file to dropbox")
                                logger.debug("Opening file: %s", target_absolute_filepath)
                                f = open(target_absolute_filepath, 'rb')
                                dbox_path = '/'.join(target_absolute_filepath.split('/')[3:])
                                logger.info("Uploading %s to Dropbox...", dbox_path)
                                self.__client.put_file(dbox_path, f)
                                f.close()
                                logger.info("%s has been copied to Dropbox under %s", source_absolute_filepath, dbox_path)
                                os.remove(target_absolute_filepath)
                                logger.debug("Removed local file %s", target_absolute_filepath)

                            self.__processed.append(item)

                            self.__current_count += 1

                            logger.debug("__send_mail_after_count: %s", self.__send_mail_after_count)
                            logger.debug("__current_count: %s", self.__current_count)

                            logger.debug("bool(current >= count) --> %s", str(bool(self.__current_count >= self.__send_mail_after_count)))

                            if self.__current_count >= self.__send_mail_after_count:
                                logger.debug("Sending email.")
                                email_sender(self.__email_address, self.__processed)

                    time.sleep(delay_seconds)

            sftp.close()

        except AuthenticationException:
            raise CerdaError("Looks like you entered the wrong password for your %s account" % getpass.getuser())