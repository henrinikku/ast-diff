from typer.testing import CliRunner

from astdiff.generator.factory import EditScriptGeneratorType
from astdiff.main import app
from astdiff.matcher.factory import MatcherType
from astdiff.parser.factory import ParserType

default_input = "print('bar')", "print('foo')"


def test_app_parso_parser(cli_runner: CliRunner):
    result = cli_runner.invoke(app, default_input + ("--parser-type", ParserType.PARSO))

    assert result.exit_code == 0
    assert "Edit script (1 ops)" in result.output
    assert "Update" in result.output


def test_app_builtin_parser(cli_runner: CliRunner):
    result = cli_runner.invoke(
        app, default_input + ("--parser-type", ParserType.BUILTIN_AST)
    )

    assert result.exit_code == 0
    assert "Edit script (1 ops)" in result.output
    assert "Update" in result.output


def test_app_gumtree_matcher(cli_runner: CliRunner):
    result = cli_runner.invoke(
        app, default_input + ("--matcher-type", MatcherType.GUMTREE)
    )

    assert result.exit_code == 0
    assert "Edit script (1 ops)" in result.output
    assert "Update" in result.output


def test_app_stub_matcher(cli_runner: CliRunner):
    result = cli_runner.invoke(
        app, default_input + ("--matcher-type", MatcherType.STUB)
    )

    assert result.exit_code == 0
    assert "Edit script (12 ops)" in result.output
    assert "Insert" in result.output
    assert "Delete" in result.output
    assert "Update" not in result.output
    assert "Move" not in result.output


def test_app_change_distilling_matcher_not_implemented(cli_runner: CliRunner):
    result = cli_runner.invoke(
        app, default_input + ("--matcher-type", MatcherType.CHANGE_DISTILLER)
    )

    assert result.exit_code == 1
    assert type(result.exception) is NotImplementedError


def test_app_with_move_edit_script_generator(cli_runner: CliRunner):
    result = cli_runner.invoke(
        app,
        default_input + ("--script-generator-type", EditScriptGeneratorType.WITH_MOVE),
    )

    assert result.exit_code == 0
    assert "Edit script (1 ops)" in result.output
    assert "Update" in result.output


def test_app_invalid_parser(cli_runner: CliRunner):
    result = cli_runner.invoke(app, default_input + ("--parser-type", "invalid"))

    assert result.exit_code == 2
    assert type(result.exception) is SystemExit
    assert "Invalid value for '--parser-type'" in result.output


def test_app_invalid_matcher(cli_runner: CliRunner):
    result = cli_runner.invoke(app, default_input + ("--matcher-type", "invalid"))

    assert result.exit_code == 2
    assert type(result.exception) is SystemExit
    assert "Invalid value for '--matcher-type'" in result.output


def test_app_invalid_edit_script_generator(cli_runner: CliRunner):
    result = cli_runner.invoke(
        app, default_input + ("--script-generator-type", "invalid")
    )

    assert result.exit_code == 2
    assert type(result.exception) is SystemExit
    assert "Invalid value for '--script-generator-type'" in result.output


def test_app_empty_args(cli_runner: CliRunner):
    result = cli_runner.invoke(app)

    assert result.exit_code == 2
    assert type(result.exception) is SystemExit
    assert "Usage: diff [OPTIONS] SOURCE TARGET" in result.output


def test_app_help(cli_runner: CliRunner):
    result = cli_runner.invoke(app, default_input + ("--help",))

    assert result.exit_code == 0
    assert "Usage: diff [OPTIONS] SOURCE TARGET" in result.output
