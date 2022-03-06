import re
import argparse
from io import BytesIO, StringIO
from ast_walker.functions import cat
import contextlib


def get_parser():  # function construct argument parser
    parser = argparse.ArgumentParser(prog='grep')
    parser.add_argument('pattern', help='pattern for search', type=str)
    parser.add_argument('files', nargs='*', metavar='file')
    parser.add_argument('-i', help='ignore case', dest='case_ignore', action='store_true')
    parser.add_argument('-w', help='force pattern to match only whole words', dest='whole_words', action='store_true')
    parser.add_argument(
        '-A',
        help='print NUM lines of trailing context',
        dest='after_context',
        type=int,
        default=0,
        metavar='NUM'
    )

    return parser


def grep(input_stream, *args):
    parser = get_parser()

    returncode, out, err = 0, BytesIO(), BytesIO()

    out_str = StringIO()
    err_str = StringIO()

    try:
        with contextlib.redirect_stdout(out_str) and contextlib.redirect_stderr(err_str):
            arguments = parser.parse_args(args)
    except SystemExit:  # it raises when arguments are invalid
        returncode = 1
        out.write(out_str.getvalue().encode())
        err.write(err_str.getvalue().encode())
        return returncode, out, err
    except Exception as e:
        returncode = 1
        err.write(str(e).encode())
        return returncode, out, err

    if arguments.after_context < 0:  # after_context can't be negative
        returncode = 1
        err.write(b'after_context must be non-negative integer value\n')
        err.write(parser.format_usage().encode())
        return returncode, out, err

    pattern = arguments.pattern
    if arguments.whole_words:
        pattern = rf'\b{pattern}\b'

    flags = re.IGNORECASE if arguments.case_ignore else 0
    after_context = arguments.after_context

    def process_stream(stream):  # inner function for filter needed lines from stream
        context = 0
        out = BytesIO()
        stream.seek(0)
        for line in stream.readlines():
            s = re.search(pattern, line.decode(), flags=flags)
            line = line.rstrip(b'\n') + b'\n'
            if s:
                out.write(line)
                context = after_context
            elif context > 0:
                out.write(line)
                context -= 1
        return out

    if not arguments.files:
        out = process_stream(input_stream)
    else:
        for filename in arguments.files:
            cat_returncode, cat_out, cat_err = cat(BytesIO(), filename)
            err.write(cat_err.getvalue())

            if cat_returncode != 0:
                returncode = cat_returncode

            out.write(process_stream(cat_out).getvalue())

    return returncode, out, err
