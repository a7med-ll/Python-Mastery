from typer.testing import CliRunner
from wordcount.main import app

runner = CliRunner()

def test_main():
    result = runner.invoke(app, ["sample.txt"])
    assert result.exit_code == 0
    assert "Words: " in result.output
    assert "Lines: " in result.output
    assert "Characters: " in result.output