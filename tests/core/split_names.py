import unittest

from xumes.core.xumes_cli import split_names


class SplitNamesTest(unittest.TestCase):

    def test_split_names_empty(self):
        self.assertEqual(split_names(''), [])

    def test_split_names_one_name(self):
        self.assertEqual(split_names('name'), ['name'])

    def test_split_names_two_names(self):
        self.assertEqual(split_names('name1,name2'), ['name1', 'name2'])

    def split_names_comma(self):
        self.assertEqual(split_names('"name,1","name,2","name3"'), ['name,1', 'name,2', 'name3'])
