import pytest
from cerda.helpers import parse_args


def test_empty():
    with pytest.raises(SystemExit):
        args = parse_args([])


def test_illegal_source():
    with pytest.raises(SystemExit):
        parse_args(['loc*al1/local11', 'remote1/remote11'])


def test_illegal_target():
    with pytest.raises(SystemExit):
        parse_args(['local1/local11', 'remote1/remot+e11'])


def test_illegal_source_target():
    with pytest.raises(SystemExit):
        parse_args(['loca*l1/local11', 'remote1/remot+e11'])


def test_source_starting_slash():
    with pytest.raises(SystemExit):
        parse_args(['/local1/local11', 'remote1/remote11'])


def test_source_and_target_starting_slash():
    with pytest.raises(SystemExit):
        parse_args(['/local1/local11', '/remote1/remote11'])


def test_source_ending_slash():
    with pytest.raises(SystemExit):
        parse_args(['local1/local11/', 'remote1/remote11'])


def test_source_and_target_ending_slash():
    with pytest.raises(SystemExit):
        parse_args(['local1/local11/', 'remote1/remote11/'])


def test_passing_extensions_with_dots():
    with pytest.raises(SystemExit):
        parse_args(['foo/bar', 'foo/bar', '-t', '.png,.jpeg'])

def test_passing_extensions_with_spaces():
    with pytest.raises(SystemExit):
        parse_args(['foo/bar', 'foo/bar', '-t', 'png jpeg'])