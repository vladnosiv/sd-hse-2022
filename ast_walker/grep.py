#!/usr/bin/env python3
from typing import List, Tuple, TextIO, Callable
import sys
import re
import argparse


def read_files(input_stream: TextIO, name_files: List[str]) -> List[Tuple[str, List[str]]]:

    def get_lines_of_file(current_stream: TextIO) -> List[str]:
        return [line.rstrip('\n') for line in current_stream.readlines()]

    data = []
    if len(name_files) > 0:
        for current_file in name_files:
            with open(current_file, 'r') as f:
                data.append((current_file, get_lines_of_file(f)))
    else:
        data.append(('sys.stdin', get_lines_of_file(input_stream)))
    return data


def check_entry_generator(
        pattern: str, is_regex: bool, rev: bool,
        full_match: bool, case_ignore: bool) -> Callable[[str], bool]:
    pattern = pattern if is_regex else re.escape(pattern)
    searcher = re.fullmatch if full_match else re.search
    flags = re.IGNORECASE if case_ignore else 0

    def check_entry(line: str):
        return bool(searcher(pattern, line, flags=flags)) ^ rev

    return check_entry


def search_in_file(
        name_file: str, check_entry: Callable[[str], bool], lines: List[str], fmt: str) -> bool:
    entry = 0
    for line in lines:
        if check_entry(line):
            entry = 1
            if fmt != '{0}':
                print(fmt.format(name_file, line))
    return bool(entry)


def count_in_lines(lines: List[str], check_entry: Callable[[str], bool]) -> int:
    res = 0
    for line in lines:
        res += check_entry(line)
    return res


def search_in_files(
        parse_data: List[Tuple[str, List[str]]], check_entry: Callable[[str], bool],
        count_output: bool, fmt: str, rev_names: bool):
    files_with_entry = []
    files_without_entry = []
    for current_file, lines_of_file in parse_data:
        if count_output:
            print(fmt.format(current_file, count_in_lines(lines_of_file, check_entry)))
        else:
            entry = search_in_file(current_file, check_entry, lines_of_file, fmt)
            if entry:
                files_with_entry.append(current_file)
            else:
                files_without_entry.append(current_file)
    if fmt == '{0}':
        if rev_names:
            for current_file in files_without_entry:
                print(fmt.format(current_file, ''))
        else:
            for current_file in files_with_entry:
                print(fmt.format(current_file, ''))


def grep(input_stream, args_str: List[str]):
    parser = argparse.ArgumentParser(prog='grep')
    parser.add_argument('needle', help='pattern for search', type=str)
    parser.add_argument('files', nargs='*')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', help='count pattern in files', dest='count', action='store_true')
    group.add_argument('-l', help='names files with pattern', dest='names', action='store_true')
    group.add_argument(
        '-L', help='names files without pattern', dest='rev_names', action='store_true'
    )
    parser.add_argument('-E', help='if pattern is regex', dest='regex', action='store_true')
    parser.add_argument('-i', help='ignore case', dest='case_ignore', action='store_true')
    parser.add_argument('-v', help='rev result', dest='rev', action='store_true')
    parser.add_argument('-x', help='full match', dest='full_match', action='store_true')
    args = parser.parse_args(args_str)

    if args.names or args.rev_names:
        fmt = '{0}'
    elif len(args.files) > 1:
        fmt = '{0}:{1}'
    else:
        fmt = '{1}'

    check_entry = check_entry_generator(
        args.needle, args.regex, args.rev, args.full_match, args.case_ignore)

    read_data = read_files(input_stream, args.files)

    search_in_files(read_data, check_entry, args.count, fmt, args.rev_names)
