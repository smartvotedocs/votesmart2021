import pytest

from parse import get_args


def test_default_arguments():
    args = get_args([])
    assert args.in_file == "README.md"
    assert args.out_file == "votesmart"
    assert args.format == "json"


def test_short_arguments():
    args = get_args(["READYOURSELF.md", "-f", "yaml", "-o", "outfile"])
    assert args.in_file == "READYOURSELF.md"
    assert args.out_file == "outfile"
    assert args.format == "yaml"


def test_long_arguments():
    args = get_args(["PUTINVOR.md", "--format", "bson", "--out-file", "f"])
    assert args.in_file == "PUTINVOR.md"
    assert args.out_file == "f"
    assert args.format == "bson"


def test_invalid_arguments(capsys):
    with pytest.raises(SystemExit):
        get_args(["-z", "foo"])
    capsys.readouterr()


def test_too_many_arguments(capsys):
    with pytest.raises(SystemExit):
        get_args(["foo", "bar"])
    capsys.readouterr()
