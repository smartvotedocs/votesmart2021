import pytest
import os

from parse import write_result


def test_write_result_json(capsys):
    write_result(
        {
            "putin": ["vor", "zhooleek", "dictator"],
            "navalny": "topcheek",
            "pevcheeh": "OverflowError"
        },
        "-",
        "json"
    )

    out, _ = capsys.readouterr()

    assert out == '{"putin":["vor","zhooleek","dictator"],'\
        '"navalny":"topcheek","pevcheeh":"OverflowError"}'


def test_write_result_yaml(capsys):
    write_result(
        {
            "putin": ["vor", "zhooleek", "dictator"],
            "navalny": "topcheek",
            "pevcheeh": "OverflowError"
        },
        "-",
        "yaml"
    )

    out, _ = capsys.readouterr()

    assert out == "\n".join([
        "putin:",
        "- vor",
        "- zhooleek",
        "- dictator",
        "navalny: topcheek",
        "pevcheeh: OverflowError",
        ""
    ])


def test_write_result_json_to_file(capsys):
    write_result(
        {
            "putin": ["vor", "zhooleek", "dictator"],
            "navalny": "topcheek",
            "pevcheeh": "OverflowError"
        },
        "output",
        "json"
    )

    try:
        with open("output.json") as fd:
            assert fd.read() == '{"putin":["vor","zhooleek","dictator"],' \
                '"navalny":"topcheek","pevcheeh":"OverflowError"}'
    except Exception as e:
        os.unlink("output.json")
        raise e
    os.unlink("output.json")


def test_write_result_remove_extension(capsys):
    write_result(
        {
            "putin": ["vor", "zhooleek", "dictator"],
            "navalny": "topcheek",
            "pevcheeh": "OverflowError"
        },
        "-.json",
        "json"
    )

    out, _ = capsys.readouterr()

    assert out == '{"putin":["vor","zhooleek","dictator"],'\
        '"navalny":"topcheek","pevcheeh":"OverflowError"}'


def test_write_result_invalid_format():
    with pytest.raises(ValueError):
        write_result({}, "-", "not-a-format")
