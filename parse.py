#!/usr/bin/env python3

import sys
import argparse
import re
import json
import yaml
import bson


CANDIDATES_TABLE_HEADER = [
    "| Округ | ФИО кандидата | Партия |",
    "| ----- | ------------- | ------ |"
]
DISTRICT_TITLE_REGEX = '^#\\s*<a\\s+\\w+=".*"></a>\\s*'

DUMPERS = {
    "json": lambda data, args: json.dumps(
        data,
        separators=(",", ": ") if args["beautify"] else (*",:",),
        indent=2 if args["beautify"] else None,
        ensure_ascii=args["ascii"],
    ).encode(),
    "yaml": lambda data, args: yaml.dump(
        data,
        allow_unicode=not args["ascii"],
        sort_keys=False
    ).encode(),
    "bson": lambda data, args: bson.dumps(data)
}


def get_args(args):
    parser = argparse.ArgumentParser(
        description="Serialize the votesmart's README file into "
        "a computer-readable format."
    )

    parser.add_argument(
        "in_file", type=str, nargs="?",
        metavar="README.md", default="README.md",
        help="input file (default: README.md)"
    )
    parser.add_argument(
        "-o", "--out-file", type=str, nargs="?",
        metavar="votesmart", default="votesmart",
        help="output file, without the extension (default: votesmart); "
        "pass \"-\" to print to stdout"
    )
    parser.add_argument(
        "-f", "--format", type=str, metavar="json", nargs="?", default="json",
        help="output file format: "
        + "|".join(DUMPERS.keys())
        + " (default: json)"
    )
    parser.add_argument(
        "-a", "--ascii", action="store_true",
        default=False, help="if specified, forces ascii encoding on output "
        "(with \\uXXXX sequences for utf8 sequences)"
    )
    parser.add_argument(
        "-b", "--beautify", action="store_true",
        default=False, help="if specified, indents the output for readability "
        "(where applicable)"
    )

    return parser.parse_args(args)


def warn(i, *msg):
    print("WARNING:", f"l.{i + 1}:", *msg, file=sys.stderr)


def parse_candidate(result, line, current_district, i):
    *entries, = filter(None, map(str.strip, line.split("|")))

    if len(entries) != 3:
        return warn(
            i, f"Invalid row length. Expected 3 columns, got {len(entries)}."
        )

    try:
        id, station = entries[0].split(" ", 1)
        id = int(id)

        if id in result["candidates"]:
            return warn(i, f"Duplicate station ID {id}. Skipping candidate.")
    except ValueError:
        return warn(i, "Failed to parse station ID. Skipping candidate.")

    candidate, party = entries[1:]

    if current_district:
        result["districts"][current_district] += [id]

    if party not in result["parties"]:
        result["parties"] += [party]

    result["candidates"][id] = {
        "station":      station,
        "candidate":    candidate,
        "party":        result["parties"].index(party)
    }


def parse_lines(lines):
    result = {
        "parties":      [],
        "districts":    {},
        "candidates":   {}
    }
    current_district = None
    was_in_table = False

    for i, line in enumerate(lines):
        match = re.match(DISTRICT_TITLE_REGEX, line)
        if match:
            current_district = line[match.end():]
            if current_district not in result["districts"]:
                result["districts"][current_district] = []
        if (
            (
                (i > 1 and lines[i - 2:i] == CANDIDATES_TABLE_HEADER)
                or was_in_table
            )
            and line.count("|") > 1
        ):
            parse_candidate(result, line, current_district, i)
            was_in_table = True
        else:
            was_in_table = False

    result["candidates"] = {
        key: val for key, val in sorted(result["candidates"].items())
    }

    return result


def write_result(data, out_file, format, args):
    if format not in DUMPERS:
        raise ValueError("invalid format; retry with -h")

    output = DUMPERS[format](data, args)

    if out_file.endswith("." + format):
        out_file = out_file[:-len(format) - 1]

    if out_file == "-":
        return sys.stdout.buffer.write(output)

    with open(out_file + "." + format, "wb") as fd:
        fd.write(output)


def main():  # pragma: no cover
    args = get_args(sys.argv[1:])

    with open(args.in_file) as fd:
        *lines, = map(str.strip, fd.readlines())

        write_result(
            parse_lines(lines),
            args.out_file,
            args.format,
            args.__dict__
        )


if __name__ == "__main__":  # pragma: no cover
    try:
        main()
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        exit(1)
