import argparse
import logging
import logging.config
import sys

from gitdot import __summary__, __version__, config, main


LOG = logging.getLogger(__name__)


def arg_parser() -> argparse.ArgumentParser:
    """
    Define a CLI parser for this program.
    """
    parser = argparse.ArgumentParser(description=__summary__)
    parser.add_argument(
        "-v", "--version", default=False, action="version", version=__version__
    )
    parser.add_argument(
        "-o", dest="outfile", metavar="FILE", type=str, help="Write output to a file."
    )
    parser.add_argument(
        "--png", action="store_true", help="Create a PNG image of the dot diagram"
    )
    parser.add_argument(
        "--log-opts",
        type=str,
        nargs="*",
        help="Extra options/arguments to pass to the `git log` command",
    )
    parser.add_argument(
        "--msg",
        action="store_true",
        help="Use commit messages (instead of hashes) as node names",
    )
    parser.add_argument(
        "--theme",
        type=str,
        choices=config.THEMES.keys(),
        default="dark",
        help="A color theme that defines graphviz element colors",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug logging to stdout",
    )
    return parser


def cli() -> None:
    """Parse command line arguments and pass them to main.main().

    This is the interactive (CLI) entry-point to the program.
    """
    cli_parser = arg_parser()
    cli_args = cli_parser.parse_args()

    # When using the CLI, initialize logging
    if cli_args.debug:
        config.LOG_CONFIG["loggers"]["gitdot"]["level"] = "INFO"
    logging.config.dictConfig(config.LOG_CONFIG)

    cli_vars = vars(cli_args)
    out = main.main(cli_vars)

    # Write output to stdout or a file
    if cli_args.outfile:
        with open(cli_args.outfile, "wb") as f:
            f.write(out)
    else:
        sys.stdout.buffer.write(out)


# When executed interactively (vs being programmatically imported), use the CLI.
if __name__ == "__main__":
    cli()
