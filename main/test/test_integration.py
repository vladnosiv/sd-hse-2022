from sys import stdin, stdout
from os import linesep
from io import StringIO
from environment import EnvironmentHandler
from ..main import Main


class MockCLI:
    def __init__(self, commands, out):
        self.input = commands
        self.output = out

    def read(self):
        if self.input:
            return self.input.pop(0)
        else:
            raise EOFError

    def write(self, to_write):
        self.output.write(to_write)


def user_input(commands):
    print(linesep.join(commands))
    return StringIO(linesep.join(commands))


def test_scenario_1(tmp_path):
    tmp_path.joinpath('01', '02', '03').mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath('01', '12', '03').mkdir(parents=True, exist_ok=True)
    tmp_path.joinpath('01', 'text').write_text('Some text')
    EnvironmentHandler.set_current_working_directory(tmp_path)

    uin, uout = ['ls', 'cd 01', 'cat text | wc', 'cd 02'], StringIO()  # Grep is broken
    main = Main(cli=MockCLI(uin, uout), is_testing=True)

    try:
        main.run()
    except EOFError:
        pass

    uout.seek(0)

    assert uout.read() == '01\t1\t2\t9\t'
