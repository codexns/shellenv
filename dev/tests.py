# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import unittest

import sys
from os import path

if sys.version_info < (3,):
    str_cls = unicode  #pylint: disable=E0602
else:
    str_cls = str

from .unittest_data import data, DataDecorator

import shellenv


@DataDecorator
class ShellenvTests(unittest.TestCase):

    #pylint: disable=C0326
    @staticmethod
    def shells():
        if sys.platform == 'win32':
            return ((None))

        output = [(None,)]

        shell_map = {}
        with open('/etc/shells', 'rb') as f:
            contents = f.read().decode('utf-8')

            for line in contents.splitlines():
                line = line.strip()
                if len(line) < 1:
                    continue
                if line[0] == '#':
                    continue

                name = path.basename(line)
                shell_map[name] = line

        for name in shell_map:
            to_add = (shell_map[name],)
            output.append(to_add)

        return output

    @data('shells')
    def env_types(self, shell):
        shell, env = shellenv.get_env(shell)

        self.assertEqual(str_cls, type(shell))

        self.assertTrue(len(env) > 0)

        for key in env:
            self.assertEqual(str_cls, type(key))
            self.assertEqual(str_cls, type(env[key]))

    @data('shells')
    def path_types(self, shell):
        dirs = shellenv.get_path(shell)

        self.assertTrue(len(dirs) > 0)

        for dir_ in dirs:
            self.assertEqual(str_cls, type(dir_))
