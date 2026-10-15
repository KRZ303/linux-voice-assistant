"""Regression checks for development script environments."""

import os
import runpy
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "script"


@pytest.mark.parametrize("name", ["lint_black", "lint_isort", "lint_flake8", "lint_mypy", "run", "tests"])
@pytest.mark.parametrize("has_venv", [False, True])
def test_script_uses_existing_interpreter(tmp_path, name, has_venv):
    script = tmp_path / "script" / name
    script.parent.mkdir()
    script.write_text((SCRIPTS / name).read_text())
    if has_venv:
        (tmp_path / ".venv" / "bin").mkdir(parents=True)
    expected = str(tmp_path / ".venv" / "bin" / "python3") if has_venv else "python3"

    with patch("subprocess.check_call") as check_call, patch("subprocess.run", return_value=MagicMock(returncode=0)) as run:
        if name == "run":
            with pytest.raises(SystemExit) as exc:
                runpy.run_path(str(script), run_name="__main__")
            assert exc.value.code == 0
            assert run.call_args.args[0][0] == expected
        else:
            runpy.run_path(str(script), run_name="__main__")
            assert check_call.call_args.args[0][0] == expected
    assert not (tmp_path / ".venv" / "lib").exists()


@pytest.mark.parametrize("platform", ["darwin", "linux"])
@pytest.mark.parametrize("configured_path", [None, "/custom/lib"])
def test_test_script_library_path(platform, configured_path):
    with patch.dict(os.environ, {}, clear=True), patch("sys.platform", platform), patch("subprocess.check_call") as check_call:
        if configured_path is not None:
            os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = configured_path
        runpy.run_path(str(SCRIPTS / "tests"), run_name="__main__")
        env = check_call.call_args.kwargs["env"]
        if configured_path is not None:
            assert env["DYLD_FALLBACK_LIBRARY_PATH"] == configured_path
        elif platform == "darwin":
            assert "/opt/homebrew/lib" in env["DYLD_FALLBACK_LIBRARY_PATH"].split(":")
            assert "/usr/local/lib" in env["DYLD_FALLBACK_LIBRARY_PATH"].split(":")
        else:
            assert "DYLD_FALLBACK_LIBRARY_PATH" not in env
