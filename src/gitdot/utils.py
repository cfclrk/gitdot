import subprocess
import logging

from textwrap import dedent

LOG = logging.getLogger(__name__)


def run(cmd: list, **kwargs) -> str:
    """Execute cmd as a subprocess.

    Return stdout as a string.
    """
    try:
        LOG.info(f"Running command: {cmd}")
        proc = subprocess.run(
            cmd,
            text=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            **kwargs,
        )
    except subprocess.CalledProcessError as ex:
        msg = dedent(
            f"""
            Error running command: {ex.args}
            Return Code: {ex.returncode}
              [stdout]: {ex.stdout}
              [stderr]: {ex.stderr}
            """
        )
        LOG.error(msg)
        raise

    return proc.stdout
