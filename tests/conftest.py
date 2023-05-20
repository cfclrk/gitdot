import tempfile

import pytest

from gitdot.utils import run


@pytest.fixture
def git_project():
    """A pytest fixture that provides an empty temporary git project dir.

    The directory is deleted after a test finishes.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        out = run(["git", "init"], cwd=tmpdir)
        print(out)
        yield tmpdir
