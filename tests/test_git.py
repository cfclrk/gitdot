import json
from pathlib import Path

import pytest

from gitdot import git
from gitdot.utils import run

GOLDEN_DIR = Path(__file__).parent / "golden"


@pytest.mark.parametrize("test_num", [1, 2])
def test_for_each_ref(git_project, test_num: int):
    """Test the `git.for_each_ref` function.

    This test is run once for each file specified in the @pytest.mark.parameterize
    decorator.
    """
    # Create a git project and run "git for-each-ref"
    script_path = GOLDEN_DIR / f"{test_num}.sh"
    run([str(script_path)], cwd=git_project)
    git_refs = git.for_each_ref(cwd=git_project)

    # Load golden file for comparison
    golden_refs_path = GOLDEN_DIR / f"{test_num}_refs.json"
    with golden_refs_path.open() as f:
        golden_refs = json.loads(f.read())

    # Assert the git refs are the same as the golden refs. Commit hashes will be
    # different for each test run, so only compare the "refname" field.

    keys = ["refname"]
    git_refs_filtered = [{k: d[k] for k in keys} for d in git_refs]
    golden_log_filtered = [{k: d[k] for k in keys} for d in golden_refs]
    assert git_refs_filtered == golden_log_filtered


@pytest.mark.parametrize("test_num", [1, 2])
def test_log(git_project, test_num: int):
    """Test the `git.log` function.

    `git_project` is a pytest fixture defined in conftest.py. It creates a temporary git
    project.

    This test is run for each file specified in the @pytest.mark.parameterize decorator.
    """
    # Create a git project and run "git log"
    script_path = GOLDEN_DIR / f"{test_num}.sh"
    run([str(script_path)], cwd=git_project)
    git_log = git.log(log_opts=["--all"], cwd=git_project)

    # Load golden file for comparison
    golden_log_path = GOLDEN_DIR / f"{test_num}_log.json"
    with golden_log_path.open() as f:
        golden_log = json.loads(f.read())

    # Assert the git log is same as the golden log. Commit SHAs will be different for
    # each test run, so only compare fields that are not SHAs.

    keys = ["subject", "ref_names"]
    git_log_filtered = [{k: d[k] for k in keys} for d in git_log.values()]
    golden_log_filtered = [{k: d[k] for k in keys} for d in golden_log.values()]
    assert git_log_filtered == golden_log_filtered


@pytest.mark.parametrize("test_num", [1, 2])
def test_add_refs_to_log(test_num: int):
    """Test the `git.add_refs_to_log` function.

    This test is run once for each file specified in the @pytest.mark.parameterize
    decorator.
    """
    refs_path = GOLDEN_DIR / f"{test_num}_refs.json"
    log_path = GOLDEN_DIR / f"{test_num}_log.json"

    with refs_path.open() as refs_buf, log_path.open() as log_buf:
        refs = json.loads(refs_buf.read())
        log = json.loads(log_buf.read())

    enriched_log = git.add_refs_to_log(refs, log)

    # Load golden file for comparison
    golden_enriched_log_path = GOLDEN_DIR / f"{test_num}_log_enriched.json"
    with golden_enriched_log_path.open() as f:
        golden_enriched_log = json.loads(f.read())

    # Assert the git log is same as the golden log. Commit SHAs will be different for
    # each test run, so only compare fields that are not SHAs.

    def without_shas(log_item: dict) -> dict:
        refs = log_item.setdefault("refs", [])
        new_item = {
            "subject": log_item["subject"],
            "ref_names": log_item["ref_names"],
            "refs": [
                {"objecttype": ref["objecttype"], "refname": ref["refname"]}
                for ref in refs
            ],
        }
        return new_item

    git_log_no_shas = [without_shas(i) for i in enriched_log.values()]
    golden_log_no_shas = [without_shas(i) for i in golden_enriched_log.values()]
    assert git_log_no_shas == golden_log_no_shas
