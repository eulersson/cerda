import logging
import sys

logger = logging.getLogger('cerda')

class CerdaError(Exception):
    """Prints out an error to the logger and exits the application.
    """
    def __init__(self, message):
        super(CerdaError, self).__init__(message)
        logger.error(message)
        sys.exit(0)