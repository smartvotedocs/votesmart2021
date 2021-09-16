from parse import parse_candidate


def test_parse_candidate_station_name():
    result = {
        "parties": [],
        "districts": {"Some district": []},
        "candidates": {}
    }

    parse_candidate(
        result,
        "| 123 Station Name | Candidate Name | Party Name |",
        "Some district",
        0
    )

    assert 123 in result["candidates"]
    assert result["candidates"][123]["station"] == "Station Name"


def test_parse_candidate_candidate_name():
    result = {
        "parties": [],
        "districts": {"Some district": []},
        "candidates": {}
    }

    parse_candidate(
        result,
        "| 456 Station Name | Candidate Name | Party Name |",
        "Some district",
        0
    )

    assert 456 in result["candidates"]
    assert result["candidates"][456]["candidate"] == "Candidate Name"


def test_parse_candidate_party():
    result = {
        "parties": ["KPRF", "LDPR", "Self-nominated"],
        "districts": {"Some district": []},
        "candidates": {}
    }

    parse_candidate(
        result,
        "| 789 Station Name | Candidate Name | Party Name |",
        "Some district",
        0
    )

    assert 789 in result["candidates"]
    assert result["candidates"][789]["party"] == 3
    assert result["parties"][-1] == "Party Name"


def test_parse_candidate_invalid_line(capsys):
    parse_candidate(
        {},
        "| 12345 Only 2 columns :( | Second column |",
        "Some district",
        0
    )

    _, err = capsys.readouterr()

    assert err == "WARNING: l.1: Invalid row length. Expected 3 columns, " \
        "got 2.\n"


def test_parse_candidate_invalid_station_id(capsys):
    result = {
        "parties": [],
        "districts": {"Some district": []},
        "candidates": {}
    }

    parse_candidate(
        result,
        "| NaN Station Name | Candidate Name | Party Name |",
        "Some district",
        0
    )

    _, err = capsys.readouterr()

    assert err == "WARNING: l.1: Failed to parse station ID. " \
        "Skipping candidate.\n"


def test_parse_candidate_duplicate_station_id(capsys):
    result = {
        "parties": [],
        "districts": {"Loonteekgrad": []},
        "candidates": {32: "Loonteek"}
    }

    parse_candidate(
        result,
        "| 32 Loonteek Street | Not Loonteek | Loonteeks United |",
        "Loonteekgrad",
        0
    )

    _, err = capsys.readouterr()

    assert err == "WARNING: l.1: Duplicate station ID 32. Skipping candidate.\n"
    assert result["candidates"][32] == "Loonteek"
