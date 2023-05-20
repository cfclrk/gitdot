import json
from collections import OrderedDict
from typing import Dict, List

from gitdot.utils import run


def log(log_opts: List[str] = None, **run_kwargs) -> OrderedDict[str, dict]:
    """Run a "git log" command.

    If log_opts is not provided, default to running "git log --all".

    The git output is formatted as line-delimeted JSON, which allows us to leverage the
    python json library to parse the git output and return it as a list of dictionaries.
    """
    if log_opts is None:
        log_opts = ["--all"]

    # TODO: A quote in the commit subject would cause an error
    fmt = json.dumps(
        {"commit": "%H", "parent": "%P", "subject": "%s", "ref_names": "%D"}
    )
    cmd = ["git", "log", f"--format={fmt}", *log_opts]
    stdout = run(cmd, **run_kwargs)

    # Parse the output into an ordered dictionary keyed by commit
    log = OrderedDict()
    for line in stdout.strip().split("\n"):
        parsed_line = json.loads(line)
        log[parsed_line["commit"]] = {
            "parents": parsed_line["parent"].split(),
            "subject": parsed_line["subject"],
            "ref_names": parsed_line["ref_names"],
        }

    return log


def for_each_ref(patterns: List[str] = None, **run_kwargs) -> List[Dict[str, str]]:
    """Run a "git for-each-ref" command.

    If no `patterns` are provided, default to heads (i.e. branches) and tags.

    Some examples of `patterns`:

      - "refs/pullreqs[3-7]"  # GitHub PRs 3 through 7
      - "refs/remotes"        # Remotes
      - "refs/tags/v0.0.*"    # Tags that start with v0.0
    """
    if patterns is None:
        patterns = ["refs/heads", "refs/tags"]

    fmt = json.dumps(
        {
            "objectname": "%(objectname)",
            "objecttype": "%(objecttype)",
            "refname": "%(refname)",
            "subject": "%(subject)",
        }
    )
    cmd = ["git", "for-each-ref", f"--format={fmt}", *patterns]
    stdout = run(cmd, **run_kwargs)

    # Parse the output
    refs = []
    for line in stdout.strip().split("\n"):
        parsed_line = json.loads(line)
        _, reftype, refname = parsed_line["refname"].split("/", 2)
        parsed_line["type"] = reftype
        parsed_line["name"] = refname

        # If this is an annotated tag, get the commit it points to.
        if parsed_line["objecttype"] == "tag":
            cmd = ["git", "rev-list", "-1", parsed_line["refname"]]
            commit = run(cmd, **run_kwargs).rstrip()
            parsed_line["points-at"] = commit
        else:
            parsed_line["points-at"] = parsed_line["objectname"]

        refs.append(parsed_line)

    return refs


def add_refs_to_log(
    refs: List[Dict[str, str]], log: OrderedDict[str, dict]
) -> OrderedDict[str, dict]:
    """Merge git refs into a git log."""
    for ref in refs:
        commit = ref["points-at"]
        if log.get(commit):
            log[commit].setdefault("refs", []).append(ref)
    return log
