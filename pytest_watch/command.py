"""\
pytest_watch.command
~~~~~~~~~~~~~~~~~~~~

Implements the command-line interface for pytest-watch.

All positional arguments are passed directly to py.test executable.


Usage:
  ptw [options] [--] [<args>...]

Options:
  -h --help               Show this help.
  --version               Show version.
  --watch=<dirs>          Command-separated list of directories to watch recursively
                          (default: current directory).
  --norecursedirs=<dirs>  Command-separated list of directories to not recurse to
                          (if relative: starting from the root of each watched dir).
  -c --clear              Automatically clear the screen before each run.
  --onpass=<cmd>          Run arbitrary command on pass.
  --onfail=<cmd>          Run arbitrary command on failure.
  --nobeep                Do not beep on failure.
  -p --poll               Use polling instead of events (useful in VMs).
  --ext=<exts>            Comma-separated list of file extensions that trigger a
                          new test run when changed (default: .py).
"""

import sys

import colorama
from docopt import docopt

from .watcher import watch
from . import __version__


def main(argv=None):
    """The entry point of the application."""
    colorama.init()

    if argv is None:
        argv = sys.argv[1:]
    usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
    version = 'pytest-watch ' + __version__

    args = docopt(usage, argv=argv, version=version)
    return watch(directories=(args['--watch'] or '').split(','),
                 norecursedirs=(args['--norecursedirs'] or '').split(','),
                 auto_clear=args['--clear'],
                 beep_on_failure=not args['--nobeep'],
                 onpass=args['--onpass'],
                 onfail=args['--onfail'],
                 poll=args['--poll'],
                 extensions=(args['--ext'] or '.py').split(','),
                 args=args['<args>'])
