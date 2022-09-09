# type: ignore
"""Test filemanager CLI."""
import re
from pathlib import Path

from typer.testing import CliRunner

from filemanager.cli import app
from tests.helpers import Regex

runner = CliRunner()


def test_filenames_in_dryrun(test_files, tmp_path):
    """Test clean command."""
    result = runner.invoke(app, ["-n", str(test_files[3])])
    assert result.exit_code == 0
    assert (
        result.output
        == "DRYRUN   | 2022-08-28 a_FIne &(filename).txt -> 2022-08-28 FIne filename.txt\n"
    )

    result = runner.invoke(app, ["-n", "--sep", "space", str(test_files[7])])
    assert result.exit_code == 0
    assert result.output == "DRYRUN   | __stripped separators--.txt -> stripped separators.txt\n"

    originals = Path(tmp_path / "originals")
    result = runner.invoke(app, ["-n", "--sep", "space", str(originals)])
    assert result.exit_code == 0

    result = runner.invoke(
        app, ["-nd", "--sep", "underscore", "--case", "title", str(test_files[14])]
    )
    assert result.exit_code == 0
    assert result.output == Regex(
        r".*month-DD-YYYY file january 01 2016\.txt.*->.*2016-01-01_Month_Dd_Yyyy_File\.txt",
        re.I | re.DOTALL,
    )

    result = runner.invoke(app, ["-nr", "--sep", "dash", "--case", "upper", str(test_files[14])])
    assert result.exit_code == 0
    assert result.output == Regex(
        r".*month-DD-YYYY file january 01 2016.txt.*->.*MONTH-DD-YYYY-FILE.txt", re.I | re.DOTALL
    )

    result = runner.invoke(
        app,
        [
            "-n",
            "--no-clean",
            str(test_files[19]),
        ],
    )
    assert result.exit_code == 0
    assert result.output == "INFO     | specialChars(@#$)-&*.txt -> No change\n"

    result = runner.invoke(app, ["-nd", "--sep", "dash", str(test_files[8])])
    assert result.exit_code == 0
    assert result.output == Regex(r"ALLCAPS\.txt -> \d{4}-\d{2}-\d{2}-ALLCAPS\.txt")

    result = runner.invoke(app, ["--overwrite", str(test_files[21])])
    assert result.exit_code == 0
    assert result.output == Regex(r"testfile\.txt -> No change")
    assert Path(tmp_path / "originals" / "testfile.txt").exists()

    result = runner.invoke(app, ["--case", "lower", "--sep", "space", str(test_files[24])])
    assert result.exit_code == 0
    assert result.output == Regex(r"TESTFILE\.txt -> testfile 2\.txt")
    assert Path(tmp_path / "originals" / "testfile 2.txt").exists()
