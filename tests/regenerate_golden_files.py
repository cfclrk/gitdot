"""Regenerate golden test files.

This can only be run using: "python regenerate_golden_files.py".
"""

import glob
import json
import tempfile
from pathlib import Path

from gitdot import git, main, utils

SCRIPT_PATHS = [Path(i) for i in glob.glob("**/*.sh", recursive=True)]


for script_path in SCRIPT_PATHS:
    test_num = script_path.stem

    golden_log_path = script_path.with_name(f"{test_num}_log.json")
    golden_refs_path = script_path.with_name(f"{test_num}_refs.json")
    golden_enriched_log_path = script_path.with_name(f"{test_num}_log_enriched.json")
    golden_dot_path = script_path.with_name(f"{test_num}.dot")
    png_path = script_path.with_name(f"{test_num}.png")

    # Create a temporary git project directory
    with tempfile.TemporaryDirectory() as tmpdir:
        out = utils.run(["git", "init"], cwd=tmpdir)
        print(out)

        # Run the repo script
        utils.run([str(script_path.resolve())], cwd=tmpdir)

        # Regenerate the git log file
        git_log = git.log(log_opts=["--all"], cwd=tmpdir)
        with golden_log_path.open("w") as f:
            print(f"Rewriting {golden_log_path}")
            f.write(json.dumps(git_log, indent=2))

        # Regenerate the git refs file
        git_refs = git.for_each_ref(cwd=tmpdir)
        with golden_refs_path.open("w") as f:
            print(f"Rewriting {golden_refs_path}")
            f.write(json.dumps(git_refs, indent=2))

        # Regenerate enriched log file
        enriched_log = git.add_refs_to_log(git_refs, git_log)
        with golden_enriched_log_path.open("w") as f:
            print(f"Rewriting {golden_enriched_log_path}")
            f.write(json.dumps(enriched_log, indent=2))

        # Regenerate the dot file
        dot = main.make_dot(enriched_log)
        with golden_dot_path.open("w") as f:
            print(f"Rewriting {golden_dot_path}")
            f.write(str(dot))

        # Regenerate the png file
        dot_msg = main.make_dot(enriched_log, msg=True)
        png = dot_msg.create_png()  # type: bytes
        with png_path.open("wb") as f:
            print(f"Rewriting {png_path}")
            f.write(png)
