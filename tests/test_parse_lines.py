from parse import parse_lines


def test_parse_lines_single_candidate(capsys):
    result = parse_lines([
        "# <a name=\"name\"></a> Some district",
        "| Округ | ФИО кандидата | Партия |",
        "| ----- | ------------- | ------ |",
        "| 123 Station Name | Candidate Name | Party Name |"
    ])

    assert 123 in result["candidates"]
    assert result["candidates"][123] == {
        "candidate":    "Candidate Name",
        "party":        0,
        "station":      "Station Name"
    }
    assert result["districts"] == {"Some district": [123]}
    assert result["parties"] == ["Party Name"]


def test_parse_lines_two_candidates_same_district(capsys):
    result = parse_lines([
        "# <a name=\"name\"></a> Some district",
        "| Округ | ФИО кандидата | Партия |",
        "| ----- | ------------- | ------ |",
        "| 123 Station A | Candidate A | Party A |",
        "| 321 Station B | Candidate B | Party B |"
    ])

    assert 123 in result["candidates"]
    assert result["candidates"][123] == {
        "candidate":    "Candidate A",
        "party":        0,
        "station":      "Station A"
    }
    assert 321 in result["candidates"]
    assert result["candidates"][321] == {
        "candidate":    "Candidate B",
        "party":        1,
        "station":      "Station B"
    }
    assert result["districts"] == {"Some district": [123, 321]}
    assert result["parties"] == ["Party A", "Party B"]


def test_parse_lines_two_candidates_different_districts(capsys):
    result = parse_lines([
        "# <a name=\"name\"></a> District A",
        "| Округ | ФИО кандидата | Партия |",
        "| ----- | ------------- | ------ |",
        "| 123 Station A | Candidate A | Party A |",
        "# <a name=\"name\"></a> District B",
        "| Округ | ФИО кандидата | Партия |",
        "| ----- | ------------- | ------ |",
        "| 321 Station B | Candidate B | Party B |"
    ])

    assert 123 in result["candidates"]
    assert result["candidates"][123] == {
        "candidate":    "Candidate A",
        "party":        0,
        "station":      "Station A"
    }
    assert 321 in result["candidates"]
    assert result["candidates"][321] == {
        "candidate":    "Candidate B",
        "party":        1,
        "station":      "Station B"
    }
    assert result["districts"] == {"District A": [123], "District B": [321]}
    assert result["parties"] == ["Party A", "Party B"]


def test_parse_lines_many_candidates_combined_districts(capsys):
    result = parse_lines([
        "# <a name=\"name\"></a> District A",
        "| Округ | ФИО кандидата | Партия |",
        "| ----- | ------------- | ------ |",
        "| 123 Station A | Candidate A | Party A |",
        "| 456 Station B | Candidate B | Party B |",
        "# <a name=\"name\"></a> District B",
        "| Округ | ФИО кандидата | Партия |",
        "| ----- | ------------- | ------ |",
        "| 321 Station C | Candidate C | Party A |",
        "| 654 Station D | Candidate D | Party C |"
    ])

    assert 123 in result["candidates"]
    assert result["candidates"][123] == {
        "candidate":    "Candidate A",
        "party":        0,
        "station":      "Station A"
    }
    assert 456 in result["candidates"]
    assert result["candidates"][456] == {
        "candidate":    "Candidate B",
        "party":        1,
        "station":      "Station B"
    }
    assert 321 in result["candidates"]
    assert result["candidates"][321] == {
        "candidate":    "Candidate C",
        "party":        0,
        "station":      "Station C"
    }
    assert 654 in result["candidates"]
    assert result["candidates"][654] == {
        "candidate":    "Candidate D",
        "party":        2,
        "station":      "Station D"
    }
    assert result["districts"] == {
        "District A": [123, 456],
        "District B": [321, 654]
    }
    assert result["parties"] == ["Party A", "Party B", "Party C"]
