import json
from pathlib import Path

import pytest

from gitdot import main

GOLDEN_DIR = Path(__file__).parent / "golden"


@pytest.mark.parametrize("test_num", [1, 2, 3])
def test_make_dot(test_num: int):
    enriched_log_path = GOLDEN_DIR / f"{test_num}_log_enriched.json"
    with enriched_log_path.open() as f:
        enriched_log = json.loads(f.read())

    dot = main.make_dot(enriched_log)

    golden_dot_path = GOLDEN_DIR / f"{test_num}.dot"
    with golden_dot_path.open() as f:
        golden_dot = f.read()

    # Compare generated dot to golden dot file
    assert str(dot) == golden_dot
