# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import os

from .._posix import get_shell_env, get_user
from .getent import get_user_login_shell


def get_env(shell=None):
    """
    Fetches the environmental variables for the current user. This is necessary
    since depending on how the sublime_text binary is launched, the process will
    not get the environment a user has in the terminal.

    Because sublime_text may have been launched from the terminal, the env from
    the shell specified and python's os.environ are compared to see which
    contains more information.

    :param shell:
        The shell to get the env from, if None, uses the current user's login
        shell

    :return:
        A 2-element tuple:
         - [0] unicode string shell path
         - [1] env dict with keys and values as unicode strings
    """

    # If we should compare the login shell env and os.environ
    # to see which seems to contain the correct information
    compare = False

    login_shell = get_user_login_shell(get_user())

    if shell is None:
        compare = True
    elif shell == login_shell:
        compare = True

    if not compare:
        return get_shell_env(shell)

    _, login_env = get_shell_env(shell)
    if len(login_env) > len(os.environ):
        return (shell, login_env)

    return (shell, dict(os.environ))
