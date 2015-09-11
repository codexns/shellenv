# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import os
import locale
import sys
import ctypes

from ._types import str_cls


_sys_encoding = locale.getpreferredencoding()

kernel32 = ctypes.windll.kernel32

kernel32.GetEnvironmentStringsW.argtypes = []
kernel32.GetEnvironmentStringsW.restype = ctypes.c_void_p


def get_env(shell=None):
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

    if sys.version_info < (3,):
        str_pointer = kernel32.GetEnvironmentStringsW()
        string = ctypes.wstring_at(str_pointer)

        values = {}
        while string != '':
            if string[0].isalpha():
                name, value = string.split(u'=', 1)
                values[name] = value
            # Include the trailing null byte, and measure each
            # char as 2 bytes since Windows uses UTF-16 for
            # wide chars
            str_pointer += (len(string) + 1) * 2
            string = ctypes.wstring_at(str_pointer)
    else:
        values = dict(os.environ)

    return (shell, values)
