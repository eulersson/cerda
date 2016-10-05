import pytest 

from cerda.helpers import parse_args

def test_parser_empty():
    with pytest.raises(SystemExit):
        args = parse_args([])
