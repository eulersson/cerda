import getpass
import logging
import os
import tempfile
import time

import paramiko 
import pysftp

logger = logging.getLogger(__name__)

from cerda.errors import CerdaError
from cerda.helpers import get_abs_form_rel, email_sender

class FarmWatcher:
    """Core class of the command line application. Handles or the file input
    output operations."""

    extensions = ['.png', '.exr', '.jpg', '.jpeg', '.txt']

    def __init__(
        self, 
        username, 
        password, 
        rel_src_dir, 
        rel_tar_dir, 
        host='tete', 
        notify=None, 
        client=None
    ):
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
            notify (tuple): tuple (str, int) containing the email address to
                send the email to and the number of frames that need to be
                picked up before sending it.
            client (obj): the Dropbox client instance 
                used to upload the files to the account. It has been initialized
                already. It is ready to go.
        """
        self.__host = host
        self.__username = username
        self.__password = password
        self.__client = client
        self.__current_count = 0
        self.__processed = []
        self.__notify = bool(notify)
        self.__temporary_folder = None
        self.__notify_enabled = False

        report = ("\n\nREPORT\n"
                 "------\n"
                 "- Username: %s\n"
                 "- Relative Source Directory: %s\n"
                 "- Relative Target Directory: %s\n"
                 "- Host: %s\n") % ( 
                        username,
                        rel_src_dir,
                        rel_tar_dir,
                        host
                    )

        if notify is not None:
            self.__notify_enabled = True
            if notify[0] is not None:
                report += "- Notification Email: %s\n" % notify[0]
            if notify[1] is not None:
                report += "- Notify after %d dropped frames\n" % notify[1]
        else:
            report += "- Email: NO"

        if client is not None:
            report += "- Dropbox Client: %s\n" % str(client)
        else:
            report += "- Dropbox: NO"

        report += "\n"

        logger.debug(report)
        if self.__notify:
            (self.__email_address, self.__send_mail_after_count) = notify
            

            logger.info(
                "I will send you an email to %s after %s frames have been collected",
                self.__email_address,
                self.__send_mail_after_count
            )

        self.__abs_src_dir, self.__abs_tar_dir = (get_abs_form_rel(x, self.__username) for x in [rel_src_dir, rel_tar_dir])

        logger.debug(
            "Absolute paths: %s | %s",
            self.__abs_src_dir,
            self.__abs_tar_dir
        )

        if self.__client:
            # create temp folder
            self.__temporary_folder = tempfile.mkdtemp()
            logger.debug("A temporary folder has been created: %s", self.__temporary_folder)


        if not self.__client:
            if not os.path.exists(self.__abs_tar_dir):
                logger.warning(
                    "Seems that %s does not exist on your local drive. "
                    "Creating it... ",
                    self.__abs_tar_dir
                )
                os.makedirs(self.__abs_tar_dir)
                logger.info("Folder structure created, you are welcome :)")

    def process_item(self, sftp, item):
        """Performs all the I/O and logic operations on the current item.

        Args:
            sftp (obj): sftp connection object.
            item (str): filename. The newly rendered file.
        """
        if item not in self.__processed and os.path.splitext(item)[1] in self.extensions:
            logger.info("New item dropped: %s", item)

            source_absolute_filepath = os.path.join(sftp.pwd, item)

            destination = self.__abs_tar_dir if self.__client is None else self.__temporary_folder

            target_absolute_filepath =  os.path.join(
                destination,
                item
            )

            logger.debug(
                "Source absolute filepath: %s", 
                source_absolute_filepath
            )
            logger.debug(
                "Target absolute filepath: %s", 
                target_absolute_filepath
            )

            logger.debug("Getting the file from server")

            sftp.get(item, target_absolute_filepath)

            logger.debug("Removing file from server")

            sftp.remove(source_absolute_filepath)

            if self.__client:
                logger.debug("Need to move file to dropbox")
                logger.debug("Opening file: %s", target_absolute_filepath)

                file_temporary_location = os.path.join(destination, item)

                f = open(file_temporary_location, 'rb')
                dbox_path = '/'.join(os.path.join(self.__abs_tar_dir, item).split('/')[3:])

                logger.info("Uploading %s to Dropbox...", dbox_path)

                self.__client.put_file(dbox_path, f)
                f.close()

                logger.info("%s has been copied to Dropbox under %s", source_absolute_filepath, dbox_path)

                os.remove(target_absolute_filepath)

                logger.debug("Removed local file %s", target_absolute_filepath)

            self.__processed.append(item)

            self.__current_count += 1

            logger.debug(
                "__current_count: %s", 
                self.__current_count
            )

            if self.__notify_enabled:
                logger.debug(
                    "__send_mail_after_count: %s", 
                    self.__send_mail_after_count
                )

            if self.__notify_enabled and self.__current_count >= self.__send_mail_after_count:
                logger.debug("Sending email.")
                email_sender(self.__email_address, self.__processed)

    def run(self, delay_seconds):
        """Runs the watcher in a demonized fashion. When there is a new file it
        triggers a file processor.
        
        Args:
            delay_seconds (int): after checking if there is new files it will
                sleep this amount of seconds before checking again.

        """
        logger.info(
            "I am watching for frames at this renderfarm path: %s",
            self.__abs_src_dir
        )
        try:
            with pysftp.Connection(
                self.__host,
                self.__username,
                password=self.__password
            ) as sftp:
                try:
                    sftp.chdir(self.__abs_src_dir)
                except IOError:
                    raise CerdaError(
                        "The remote location %s could not be found on "
                        "the renderfarm." % self.__abs_src_dir
                    )

                while True:
                    current_dir = sftp.pwd
                    listed_stuff = sftp.listdir()

                    for item in listed_stuff:
                        self.process_item(sftp, item)

                    time.sleep(delay_seconds)

            sftp.close()

        except paramiko.ssh_exception.AuthenticationException:
            raise CerdaError("Looks like you entered the wrong password for your %s account" % getpass.getuser())