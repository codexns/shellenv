# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import os
import sys
import subprocess
from getpass import getuser

from ._types import str_cls, type_name

if sys.platform == 'darwin':
    from ._osx.open_directory import get_user_login_shell
else:
    from ._linux.getent import get_user_login_shell


_envs = {'bytes': {}, 'unicode': {}}
_environ = {}
for key in ('HOME', 'LANG', 'USER', 'PATH'):
    if key in os.environ:
        _environ[key] = os.environ[key]


def get_shell_env(shell=None, for_subprocess=False):
    """
    Fetches the environmental variables that are set when a new shell is opened.

    :param shell:
        The shell to get the env from, if None, uses the current user's login
        shell

    :param for_subprocess:
        If True, and the code is being run in Sublime Text 2, the result will
        be byte strings instead of unicode strings

    :return:
        A 2-element tuple:

         - [0] unicode string shell path
         - [1] env dict with keys and values as unicode strings
    """

    if shell is not None and not isinstance(shell, str_cls):
        raise TypeError('shell must be a unicode string, not %s' % type_name(shell))

    if shell is None:
        shell = get_user_login_shell(get_user())
    _, shell_name = shell.rsplit('/', 1)

    output_type = 'bytes' if sys.version_info < (3,) and for_subprocess else 'unicode'

    if shell not in _envs[output_type]:
        if shell_name in ['tcsh', 'csh']:
            params = ['-l']
        else:
            params = ['-l', '-i']
        params.insert(0, shell)

        env_proc = subprocess.Popen(
            params,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=_environ
        )

        stdout, _ = env_proc.communicate(b'/usr/bin/env\n')

        _envs[output_type][shell] = {}

        entries = stdout.strip().split(b'\n(?=\\w+=)')
        for entry in entries:
            if entry == b'':
                continue
            parts = entry.split(b'=', 1)
            if len(parts) < 2:
                continue
            name = parts[0]
            value = parts[1]
            if output_type == 'unicode':
                name = name.decode('utf-8', 'replace')
                value = value.decode('utf-8', 'replace')
            _envs[output_type][shell][name] = value

    if output_type == 'bytes':
        shell = shell.encode('utf-8')

    return (shell, _envs[output_type][shell])


def get_user():
    """
    Returns the current username as a unicode string

    :return:
        A unicode string of the current user's username
    """

    output = getuser()
    if not isinstance(output, str_cls):
        output = output.decode('utf-8')
    return output
