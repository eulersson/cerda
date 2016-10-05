import logging

logger = logging.getLogger('cerda')

class CerdaError(Exception):
    def __init__(self, message):
        super(CerdaError, self).__init__(message)
        logger.error(message)
        raise SystemExit