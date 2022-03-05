import pytest
from io import BytesIO
from pathlib import Path
from environment import EnvironmentHandler
from ..functions import shell_ls


def zero_arg_prepare(path):
    path.joinpath('01', '02').mkdir(parents=True)
    path.joinpath('11').mkdir()
    (path / 'file').write_text('')


@pytest.mark.parametrize("config", [
    (zero_arg_prepare, ['11'], []),
    (zero_arg_prepare, ['01', '02'], []),
    (zero_arg_prepare, ['.'], ['01', '11', 'file']),
    (zero_arg_prepare, ['01'], ['02'])
])
def test_zero_arg(tmp_path, config):
    prepare, start, result = config
    prepare(tmp_path)
    EnvironmentHandler.set_current_working_directory(tmp_path.joinpath(*start))

    code, out, err = shell_ls(BytesIO())

    assert code == 0
    assert all(map(lambda w: w in out.getvalue().decode(), result))
    assert err.getvalue() == b''
    assert EnvironmentHandler.get_current_working_directory() == tmp_path.joinpath(*start)


def incorrect_arg_prepare(path):
    path.joinpath('1').mkdir()


@pytest.mark.parametrize("config", [
    (incorrect_arg_prepare, ['.'], ['2']),
    (incorrect_arg_prepare, ['.'], ['1', '2']),
    (incorrect_arg_prepare, ['1'], ['2'])
])
def test_incorrect_arg(tmp_path, config):
    prepare, start, args = config
    prepare(tmp_path)
    EnvironmentHandler.set_current_working_directory(tmp_path.joinpath(*start))

    code, out, err = shell_ls(BytesIO(), str(Path(*args)))

    assert code != 0
    assert len(err.getvalue()) > 0
    assert EnvironmentHandler.get_current_working_directory() == tmp_path.joinpath(*start)


def correct_arg_prepare(path):
    path.joinpath('01', '02').mkdir(parents=True)
    path.joinpath('11').mkdir()
    (path / 'file').write_text('')


@pytest.mark.parametrize("config", [
    (correct_arg_prepare, ['.'], ['01'], ['02']),
    (correct_arg_prepare, ['.'], ['.'], ['01', '11', 'file']),
    (correct_arg_prepare, ['01'], ['..'], ['01', '11', 'file']),
    (correct_arg_prepare, ['11'], ['..', '01'], ['02'])
])
def test_correct_arg(tmp_path, config):
    prepare, start, args, result = config
    prepare(tmp_path)
    EnvironmentHandler.set_current_working_directory(tmp_path.joinpath(*start))

    code, out, err = shell_ls(BytesIO(), str(Path(*args)))

    assert code == 0
    assert all(map(lambda w: w in out.getvalue().decode(), result))
    assert err.getvalue() == b''
    assert EnvironmentHandler.get_current_working_directory() == tmp_path.joinpath(*start)
