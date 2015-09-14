# coding: utf-8
from __future__ import unicode_literals, division, absolute_import, print_function

import unittest

import sys
from os import path

if sys.version_info < (3,):
    str_cls = unicode  # noqa
else:
    str_cls = str

from .unittest_data import data, data_class

import shellenv


@data_class
class ShellenvTests(unittest.TestCase):

    @staticmethod
    def shells():
        if sys.platform == 'win32':
            return [(None,)]

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
        # rbash is a really limited shell, so we don't
        # even bother trying to test it
        if shell and path.basename(shell) == 'rbash':
            return

        shell, env = shellenv.get_env(shell)

        self.assertEqual(str_cls, type(shell))

        self.assertTrue(len(env) > 0)

        for key in env:
            self.assertEqual(str_cls, type(key))
            self.assertEqual(str_cls, type(env[key]))

    @data('shells')
    def env_types_subprocess(self, shell):
        # rbash is a really limited shell, so we don't
        # even bother trying to test it
        if shell and path.basename(shell) == 'rbash':
            return

        shell, env = shellenv.get_env(shell, for_subprocess=True)

        self.assertEqual(str, type(shell))

        self.assertTrue(len(env) > 0)

        for key in env:
            self.assertEqual(str, type(key))
            self.assertEqual(str, type(env[key]))

    @data('shells')
    def path_types(self, shell):
        # rbash is a really limited shell, so we don't
        # even bother trying to test it
        if shell and path.basename(shell) == 'rbash':
            return

        shell, dirs = shellenv.get_path(shell)

        self.assertEqual(str_cls, type(shell))

        self.assertTrue(len(dirs) > 0)

        for dir_ in dirs:
            self.assertEqual(str_cls, type(dir_))
