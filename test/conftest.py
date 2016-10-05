import sys
import os

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cerda.helpers import initialize_parser

@pytest.fixture
def parser():
    return initialize_parser()