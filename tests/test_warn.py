from parse import warn


def test_warn_a(capsys):
    warn(0, "SmartVote ruuules")
    _, err = capsys.readouterr()

    assert err == "WARNING: l.1: SmartVote ruuules\n"


def test_warn_b(capsys):
    warn(2018, "RKN suuucks")
    _, err = capsys.readouterr()

    assert err == "WARNING: l.2019: RKN suuucks\n"
