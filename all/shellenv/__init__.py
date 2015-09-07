# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import os

from ._types import str_cls, type_name

if sys.platform == 'win32':
    from ._win import get_env

elif sys.platform == 'darwin':
    from ._osx import get_env

else:
    from ._linux import get_env


__version__ = '1.0.0'
__version_info__ = (1, 0, 0)


_paths = {}

def get_path(shell=None):
    """
    Returns the PATH as defined by the shell. If no shell is provided, gets the
    path from the user's login shell.

    :param shell:
        A unicode string of the shell to get the PATH from. Pass None to use
        the current user's login shell.

    :return:
        A list of unicode strings of the directories that are part of the PATH
    """

    if shell is not None and not isinstance(shell, str_cls):
        raise TypeError('shell must be a unicode string, not %s' % type_name(shell))

    shell_key = shell if shell else 'default'
    if shell_key not in _paths:
        _, env = get_env(shell)
        _paths[shell_key] = env.get('PATH', '').split(os.pathsep)
    return _paths[shell_key]
