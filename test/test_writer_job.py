import unittest
import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hunter.writer import FilePool


class FileMock:

    def __init__(self, value):
        self.value = value

    def __eq__(self, obj):
        return self.value == obj.value

    def __repr__(self):
        return self.value

    def close(self):
        pass


class TestFilePool(unittest.TestCase):

    def test_pop(self):
        pool_max_size = 2
        fp = FilePool(maxsize=pool_max_size)

        self.assertTrue(not fp.get('key1'))
        fp['key1'] = FileMock('value1')
        self.assertEqual(fp.get('key1'), FileMock('value1'))
        fp['key2'] = FileMock('value2')
        fp['key3'] = FileMock('value3')
        self.assertEqual(fp.get('key2'), FileMock('value2'))
        self.assertEqual(fp.get('key3'), FileMock('value3'))
        self.assertTrue(not fp.get('key1'))
        self.assertEqual(len(fp), 2)
