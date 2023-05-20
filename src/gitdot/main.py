import pydot

from collections import OrderedDict

from gitdot import git, config


def main(opts: dict) -> bytes:
    """Run this program with the given options.

    Options are of the form:

        {
          "log_opts": [],
          "png": False,
          "msg": True,
          "theme": "dark",
        }

    """
    git_log = git.log(opts.get("log_opts"))
    git_refs = git.for_each_ref()
    enriched_log = git.add_refs_to_log(git_refs, git_log)

    dot = make_dot(enriched_log, config.THEMES[opts["theme"]], opts["msg"])
    out = str(dot).encode("utf-8")

    if opts.get("png"):
        out = dot.create_png()

    return out


def make_dot(
    enriched_git_log: OrderedDict[str, dict],
    theme: dict = config.THEMES["dark"],
    msg: bool = False,
) -> pydot.Dot:
    """Generate a pydot.Dot from the given git log.

    The enriched_git_log is a list of dictionaries, where each dict is git log entry
    joined with some additional information about refs.
    """
    dot = pydot.Dot("G", graph_type="graph", rankdir="LR", **theme["graph_defaults"])
    dot.set_node_defaults(**theme["node_defaults"])
    dot.set_edge_defaults(**theme["edge_defaults"], dir="back")

    # TODO: instead of iterating through commits, start with the first one and then just
    # recursively add parents.

    for commit_sha, commit_info in enriched_git_log.items():

        # Add the commit node
        commit_node = make_commit_node(commit_sha, commit_info, msg, theme)
        dot.add_node(commit_node)

        # Add parent node(s) and edge(s)
        for parent_sha in commit_info["parents"]:

            # The parent might not be in the log if we've used a revision range to
            # restrict the log output
            if enriched_git_log.get(parent_sha):
                parent_info = enriched_git_log[parent_sha]
                parent_node = make_commit_node(parent_sha, parent_info, msg, theme)
                dot.add_edge(pydot.Edge(parent_node, commit_node))

        # Add ref nodes
        if len(commit_info.get("refs", [])) > 0:
            subgraph = pydot.Subgraph(rank="same")
            for ref in commit_info["refs"]:
                ref_node = make_ref_node(ref, theme)
                subgraph.add_node(ref_node)
                edge = pydot.Edge(commit_node, ref_node)
                subgraph.add_edge(edge)
            dot.add_subgraph(subgraph)

    return dot


def make_commit_node(
    commit_sha: str, commit_info: dict, msg: bool, theme: dict
) -> pydot.Node:
    """"Create a pydot.Node for a git commit."""
    if msg:
        node_name = commit_info["subject"]
    else:
        node_name = commit_sha[0:5]

    node_args = theme["commit"]
    node = pydot.Node(node_name, **node_args)
    return node


def make_ref_node(ref, theme) -> pydot.Node:
    """Create a pydot.Node for a git ref."""
    node_type = ref["type"]
    node_args = theme.get(node_type, theme["default"])
    node = pydot.Node(ref["name"], **node_args)
    return node
