import pytest 

from cerda.errors import CerdaError

from cerda.helpers import parse_args

def test_empty():
    with pytest.raises(SystemExit):
        args = parse_args([])
