import pytest
from typer.testing import CliRunner

from github_watch import app

runner = CliRunner()

@pytest.mark.parametrize(
    "options,expected", 
    [
        (["add", "cov-lineages/pango-designation", "--db", "tests/test.json"], "cov-lineages/pango-designation"),
])
def test_add(options,expected):
    result = runner.invoke(app, options)
    assert result.exit_code == 0
    assert expected in result.stdout
