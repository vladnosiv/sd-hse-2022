from io import BytesIO
from ..grep import grep


def stream(string=''):
    return BytesIO(string.encode())


def grep_case(*args, expected_code='zero', expected_out=None, expected_err=None):
    code, out, err = grep(*args)

    if expected_code == 'zero':
        assert code == 0
    elif expected_code == 'non zero':
        assert code != 0

    if expected_err is not None:
        assert err.getvalue() == expected_err.encode()

    if expected_out is not None:
        assert out.getvalue() == expected_out.encode()


def test_pattern(tmp_path):
    content = '123\n1\n2\n3\n'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), '1', str((tmp_path / 'test.txt').absolute()),
        expected_out='123\n1\n',
        expected_err=''
    )


def test_newlines(tmp_path):
    content = '123\n1\n2\n3'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), '3', str((tmp_path / 'test.txt').absolute()),
        expected_out='123\n3\n',
        expected_err=''
    )


def test_regex(tmp_path):
    content = '123\n1\n2\n3'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), '1.*3', str((tmp_path / 'test.txt').absolute()),
        expected_out='123\n',
        expected_err=''
    )


def test_whole_word_basic(tmp_path):
    content = '123\n1\n2\n3\n'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), '1', str((tmp_path / 'test.txt').absolute()), '-w',
        expected_out='1\n',
        expected_err=''
    )


def test_whole_word(tmp_path):
    content = 'needle_needle\nneedle\nneedle-needle\nneedle+needle\nneedle needle\nneedleXneedle'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), 'needle', str((tmp_path / 'test.txt').absolute()), '-w',
        expected_out='needle\nneedle-needle\nneedle+needle\nneedle needle\n',
        expected_err=''
    )


def test_case_ignore(tmp_path):
    content = 'word\nWoRd\n_WORD\nwtf\n'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), 'word', str((tmp_path / 'test.txt').absolute()), '-i',
        expected_out='word\nWoRd\n_WORD\n',
        expected_err=''
    )


def test_case_ignore_whole_word(tmp_path):
    content = 'word\nWoRd\n_WORD\nwtf\n'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), 'word', str((tmp_path / 'test.txt').absolute()), '-w', '-i',
        expected_out='word\nWoRd\n',
        expected_err=''
    )


def test_after_context(tmp_path):
    content = 'needle\nwtf\nneedle\ngarbage\nneedle\ndont ignore\nignore\n'
    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), 'needle', str((tmp_path / 'test.txt').absolute()), '-A', '1',
        expected_out='needle\nwtf\nneedle\ngarbage\nneedle\ndont ignore\n',
        expected_err=''
    )


def test_input_stream():
    content = 'needle\nwtf\nneedle\ngarbage\nneedle\ndont ignore\nignore\n'

    grep_case(stream(content), 'needle', '-A', '1',
        expected_out='needle\nwtf\nneedle\ngarbage\nneedle\ndont ignore\n',
        expected_err=''
    )


def test_only_needle():
    grep_case(stream(), 'needle',
        expected_code='zero',
        expected_err=''
    )


def test_invalid_arguments():
    grep_case(stream(), 'needle', '/random_path/test.txt', '-A', '-1',
        expected_code='non zero'
    )

    grep_case(stream(),
        expected_code='non zero'
    )


def strip_all_lines(string):
    return '\n'.join(map(lambda s: s.strip('\n\t '), string.split('\n')))


def test_hard_regex(tmp_path):
    regex = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'  # a real number, possible in exponential notation

    content = '''0
        1
        123
        4e5
        4E5
        1.4
        .2
        -2.0
        -123e14
        -.1e-17
        -.2E-0
        2e-13
        2E-13
        .15e18
        .15E18
        2.9e6
        2.9E6
        2.9e-6
        2.9E-6
        +17
        +17.1
        +.2e+14
        +.2E+14
        +.2E-14
        +1.2E-14
        +1.2E14
    '''

    content = strip_all_lines(content)

    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), regex, str((tmp_path / 'test.txt').absolute()), '-w',
        expected_out=content,
        expected_err=''
    )


def test_hard_regex_unmatch(tmp_path):
    regex = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'  # a real number, possible in exponential notation

    content = '''
        1_23
        wtf
        4X5
        1k4
    '''

    content = strip_all_lines(content)

    (tmp_path / 'test.txt').write_text(content)
    grep_case(stream(), regex, str((tmp_path / 'test.txt').absolute()), '-w',
        expected_out='',
        expected_err=''
    )
