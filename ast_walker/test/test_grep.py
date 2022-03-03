#!/usr/bin/env python3
import io
from environment import EnvironmentHandler
from ..grep import *


def test_check_entry():
    check_entry = check_entry_generator('needle', False, True, False, False)
    assert not check_entry('trash_needle_trash')
    check_entry = check_entry_generator('needle', False, False, False, False)
    assert not check_entry('trash_nedle_trash')
    check_entry = check_entry_generator('ne.d.e', True, False, False, False)
    assert check_entry('needle')
    check_entry = check_entry_generator('neEdLe', False, True, True, True)
    assert not check_entry('needle')


def test_read_files(tmp_path, monkeypatch):
    (tmp_path / 'a.txt').write_text('first line\nsecond line\nthird line')
    (tmp_path / 'b.txt').write_text('FIRST LINE\nSECOND LINE\nTHIRD LINE')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    lines = read_files(None, ['a.txt', 'b.txt'])
    assert lines == [('a.txt', ['first line', 'second line', 'third line']), (
        'b.txt', ['FIRST LINE', 'SECOND LINE', 'THIRD LINE'])]
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'first line\n second line\n'))
    lines = read_files(sys.stdin, [])
    assert lines == [('sys.stdin', ['first line', ' second line'])]


def test_search_in_file(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\nnedle\nneedle needle needle\ntrash')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    check_entry = check_entry_generator('needle', False, False, False, False)
    data = read_files(None, ['a.txt'])
    lines = data[0][1]
    search_in_file('a.txt', check_entry, lines, '{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\nneedle needle needle\n'
    check_entry = check_entry_generator('ne.d.e', True, False, False, False)
    search_in_file('a.txt', check_entry, lines, '{1}')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needle\nneedle needle needle\n'


def test_count_in_lines():
    lines = ['needle', 'needle needle needle', 'nedle', 'trash']
    check_entry = check_entry_generator('needle', False, False, False, False)
    counter = count_in_lines(lines, check_entry)
    assert counter == 2
    check_entry = check_entry_generator('nee?d.e', True, False, False, False)
    counter = count_in_lines(lines, check_entry)
    assert counter == 3


def test_search_in_files(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('first line\nsecond line\nthird line')
    (tmp_path / 'b.txt').write_text('LINE LINE LINE\nTRRRRASH')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    data = read_files(None, ['a.txt', 'b.txt'])
    check_entry = check_entry_generator('line', False, False, False, True)
    search_in_files(data, check_entry, True, '{0}:{1}', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:3\nb.txt:1\n'
    data = read_files(None, ['a.txt', 'b.txt'])
    check_entry = check_entry_generator('line', False, False, False, False)
    search_in_files(data, check_entry, False, '{0}:{1}', False)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:first line\na.txt:second line\na.txt:third line\n'


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep(sys.stdin, ['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep(sys.stdin, ['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep(sys.stdin, ['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    grep(None, ['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    grep(None, ['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    grep(None, ['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_format_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needle\ntrash\ni want to pass ALGEBRA\n')
    (tmp_path / 'b.txt').write_text('ALGeBRAAA\nI hate algebra?\nI love algebra?\n')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    grep(None, ['-li', 'algebra', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'
    grep(None, ['-Lx', 'ALGEBRA', 'a.txt', 'b.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\nb.txt\n'


def test_integrate_all_keys_print_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    grep(None, ['-livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt\n'


def test_integrate_all_keys_print_not_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    grep(None, ['-Livx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt\n'


def test_integrate_all_keys_count_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fO\nFO\nFoO\n')
    (tmp_path / 'b.txt').write_text('hello fo?o world\nxfooyfoz\nfooo\n')
    EnvironmentHandler.set_current_working_directory(tmp_path)
    grep(None, ['-civx', '-E', 'fo?o', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:3\na.txt:0\n'
