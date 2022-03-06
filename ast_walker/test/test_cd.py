import os

import pytest
from io import BytesIO
from pathlib import Path
from environment import EnvironmentHandler
from ..functions import shell_cd


def test_zero_arg():
    code, out, err = shell_cd(BytesIO())

    assert code == 0
    assert out.getvalue() == b''
    assert err.getvalue() == b''


def test_unexisting_path(tmp_path):
    EnvironmentHandler.set_current_working_directory(tmp_path)

    code, out, err = shell_cd(BytesIO(), 'any-path')

    assert code != 0
    assert out.getvalue() == b''
    assert len(err.getvalue()) > 0
    assert EnvironmentHandler.get_current_working_directory() == tmp_path


def test_to_file(tmp_path):
    EnvironmentHandler.set_current_working_directory(tmp_path)
    (tmp_path / 'any-file.txt').write_text('You cannot cd here')

    code, out, err = shell_cd(BytesIO(), 'any-file.txt')

    assert code != 0
    assert out.getvalue() == b''
    assert len(err.getvalue()) > 0
    assert EnvironmentHandler.get_current_working_directory() == tmp_path


def prepare_1(path):
    path.joinpath('1', '2').mkdir(parents=True, exist_ok=True)


def prepare_2(path):
    path.joinpath('1').joinpath('21').mkdir(parents=True, exist_ok=True)
    path.joinpath('1').joinpath('22').mkdir(parents=True, exist_ok=True)


@pytest.mark.parametrize("config", [
    (prepare_1, ['1'], ['2']),
    (prepare_1, ['2'], ['..']),
    (prepare_2, ['1', '21'], ['..', '21']),
    (prepare_2, ['1', '21'], ['..', '22'])
])
def test_happy_path(config, tmp_path):
    prepare, start, argument = config
    prepare(tmp_path)  # setting up the environment
    EnvironmentHandler.set_current_working_directory(tmp_path.joinpath(*start))  # setting up start directory

    code, out, err = shell_cd(BytesIO(), str(Path(*argument)))

    assert code == 0
    assert out.getvalue() == b''
    assert err.getvalue() == b''
    expected = Path(os.path.abspath(tmp_path.joinpath(*start, *argument)))
    assert EnvironmentHandler.get_current_working_directory() == expected
