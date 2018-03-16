from os.path import expanduser
try: from pathlib import Path as pl_path
except ImportError: from pathlib2 import Path as pl_path

from six import string_types

__all__ = ['Path']

def Path(*args, **kwargs):
    """ A passthrough to Pathlib, but it automatically expands "~" in strings """
    if len(args) >0 and isinstance(args[0], string_types):
        expArg = expanduser(args[0])
        return pl_path(expArg, *args[1:], **kwargs)
    return pl_path(*args, **kwargs)