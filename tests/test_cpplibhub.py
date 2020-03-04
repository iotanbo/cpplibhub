
import pytest
from click.testing import CliRunner

from cpplibhub.cli import main


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_main(runner):
    # assert main([]) == 0  # run without click
    result = runner.invoke(main)
    # result = runner.invoke(main, ['--name', 'Amy'])
    assert result.exit_code == 0
    # assert result.output == 'Hello Amy!\n'
