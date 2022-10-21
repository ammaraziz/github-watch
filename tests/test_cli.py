import tempfile
import pytest
from typer.testing import CliRunner

from github_watch import app

@pytest.fixture()
def out_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

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

@pytest.mark.parametrize(
    "options,expected", 
    [
        (["check", "--db", "tests/test.json"], "cov-lineages/pango-designation"),
        (["check", "--slack", "https://hooks.slack.com/services/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", "--db", "tests/test.json"], "Sending update to slack"),
])
def test_check(options,expected):
    import json
    with open('tests/test.json', 'w') as f:
        json.dump({'cov-lineages/pango-designation':{'url':'fake'}}, f)
    result = runner.invoke(app, options)
    assert result.exit_code == 0
    assert expected in result.stdout
