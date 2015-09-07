# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import os
import locale

from ._types import str_cls


_sys_encoding = locale.getpreferredencoding()


def get_env(shell=None):  #pylint: disable=W0613
    """
    Return environment variables for the current user

    :param shell:
        The shell to get the env from - unused on Windows

    :return:
        A 2-element tuple:
         - [0] unicode string shell path
         - [1] env dict with keys and values as unicode strings
    """

    shell = os.environ['ComSpec']
    if not isinstance(shell, str_cls):
        shell = shell.decode(_sys_encoding)

    return (shell, dict(os.environ))
