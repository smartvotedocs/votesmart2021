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
        "json",
        {"ascii": 0, "beautify": 0}
    )

    out, _ = capsys.readouterr()

    assert out == '{"putin":["vor","zhooleek","dictator"],'\
        '"navalny":"topcheek","pevcheeh":"OverflowError"}'


def test_write_result_json_beautified(capsys):
    write_result(
        {
            "putin": ["vor", "zhooleek", "dictator"],
            "navalny": "topcheek",
            "pevcheeh": "OverflowError"
        },
        "-",
        "json",
        {"ascii": 0, "beautify": 1}
    )

    out, _ = capsys.readouterr()

    assert out == "\n".join([
        '{',
        '  "putin": [',
        '    "vor",',
        '    "zhooleek",',
        '    "dictator"',
        '  ],',
        '  "navalny": "topcheek",',
        '  "pevcheeh": "OverflowError"',
        '}'
    ])


def test_write_result_json_ascii(capsys):
    write_result(
        {
            "Сегодня": [
                "Мы увидим то, что считается невозможным увидеть вблизи.",
                "Мы зайдем туда, куда никого не пускают.",
                "Мы попадем в гости к Путину."
            ],
            "Своими глазами убедимся в том, что": {
                "Этот человек в своей тяге ": [
                    "к роскоши",
                    "к богатству"
                ],
                "Спятил": "совершенно"
            }
        },
        "-",
        "json",
        {"ascii": 1, "beautify": 0}
    )

    out, _ = capsys.readouterr()

    assert out == '{"\\u0421\\u0435\\u0433\\u043e\\u0434\\u043d\\u044f":[' \
        '"\\u041c\\u044b \\u0443\\u0432\\u0438\\u0434\\u0438\\u043c \\u0442' \
        '\\u043e, \\u0447\\u0442\\u043e \\u0441\\u0447\\u0438\\u0442\\u0430' \
        '\\u0435\\u0442\\u0441\\u044f \\u043d\\u0435\\u0432\\u043e\\u0437' \
        '\\u043c\\u043e\\u0436\\u043d\\u044b\\u043c \\u0443\\u0432\\u0438' \
        '\\u0434\\u0435\\u0442\\u044c \\u0432\\u0431\\u043b\\u0438\\u0437' \
        '\\u0438.","\\u041c\\u044b \\u0437\\u0430\\u0439\\u0434\\u0435\\u043c' \
        ' \\u0442\\u0443\\u0434\\u0430, \\u043a\\u0443\\u0434\\u0430 \\u043d' \
        '\\u0438\\u043a\\u043e\\u0433\\u043e \\u043d\\u0435 \\u043f\\u0443' \
        '\\u0441\\u043a\\u0430\\u044e\\u0442.","\\u041c\\u044b \\u043f\\u043e' \
        '\\u043f\\u0430\\u0434\\u0435\\u043c \\u0432 \\u0433\\u043e\\u0441' \
        '\\u0442\\u0438 \\u043a \\u041f\\u0443\\u0442\\u0438\\u043d\\u0443.' \
        '"],"\\u0421\\u0432\\u043e\\u0438\\u043c\\u0438 \\u0433\\u043b\\u0430' \
        '\\u0437\\u0430\\u043c\\u0438 \\u0443\\u0431\\u0435\\u0434\\u0438' \
        '\\u043c\\u0441\\u044f \\u0432 \\u0442\\u043e\\u043c, \\u0447\\u0442' \
        '\\u043e":{"\\u042d\\u0442\\u043e\\u0442 \\u0447\\u0435\\u043b\\u043e' \
        '\\u0432\\u0435\\u043a \\u0432 \\u0441\\u0432\\u043e\\u0435\\u0439 ' \
        '\\u0442\\u044f\\u0433\\u0435 ":["\\u043a \\u0440\\u043e\\u0441' \
        '\\u043a\\u043e\\u0448\\u0438","\\u043a \\u0431\\u043e\\u0433\\u0430' \
        '\\u0442\\u0441\\u0442\\u0432\\u0443"],"\\u0421\\u043f\\u044f\\u0442' \
        '\\u0438\\u043b":"\\u0441\\u043e\\u0432\\u0435\\u0440\\u0448\\u0435' \
        '\\u043d\\u043d\\u043e"}}'


def test_write_result_yaml(capsys):
    write_result(
        {
            "putin": ["vor", "zhooleek", "dictator"],
            "navalny": "topcheek",
            "pevcheeh": "OverflowError"
        },
        "-",
        "yaml",
        {"ascii": 0, "beautify": 0}
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
        "json",
        {"ascii": 0, "beautify": 0}
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
        "json",
        {"ascii": 0, "beautify": 0}
    )

    out, _ = capsys.readouterr()

    assert out == '{"putin":["vor","zhooleek","dictator"],'\
        '"navalny":"topcheek","pevcheeh":"OverflowError"}'


def test_write_result_invalid_format():
    with pytest.raises(ValueError):
        write_result(
            {},
            "-",
            "not-a-format",
            {"ascii": 0, "beautify": 0}
        )
