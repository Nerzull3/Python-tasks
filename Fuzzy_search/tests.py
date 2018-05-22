import unittest
import re

from main import search_for_entries, get_words
from levenshteins_distance import get_distance


class TestMethods(unittest.TestCase):
    def test_empty_text(self):
        sear_words = []
        text = ['a']
        with self.assertRaises(ValueError):
            search_for_entries(text, sear_words, '')

    def test_empty_list_of_words(self):
        sear_words = ['8']
        text = []
        with self.assertRaises(ValueError):
            search_for_entries(text, sear_words, '')

    def test_search_zero_words(self):
        sear_words = ['asd']
        text = ['123', 'aassd']
        self.assertEqual([], search_for_entries(text, sear_words, ''))

    def test_search_one_word(self):
        sear_words = ['asd']
        text = ['123', 'asd']
        self.assertEqual([('asd', 2, 1, 0)], search_for_entries(text, sear_words, ''))

        sear_words = ['a']
        text = ['a 123 = 123 a', 'aa ', 'tra-ta-ta']
        self.assertEqual(
            [('a', 1, 1, 0), ('a', 1, 4, 0), ('aa', 2, 1, 1)],
            search_for_entries(text, sear_words, ''))

    def test_search_two_words(self):
        sear_words = ['qwer', 'wert']
        text = ['Hello, qwer! How are you?', 'It\'s me.']
        self.assertEqual([('qwer', 1, 2, 0)], search_for_entries(text, sear_words, ''))

        sear_words = ['qwer', 'wert']
        text = ['Hello, qwer! How are you?', 'It\'s wert.']
        self.assertEqual([('qwer', 1, 2, 0), ('wert', 2, 2, 0)], search_for_entries(text, sear_words, ''))

    def test_search_many_entered(self):
        sear_words = ['a']
        text = []
        for i in range(500):
            text.append('ab')
        self.assertEqual([('ab', i + 1, 1, 1) for i in range(500)], search_for_entries(text, sear_words, ''))

    def test_search_very_many_entered(self):
        sear_words = ['a']
        text = []
        for i in range(500):
            text.append('a ' * 100)
        self.assertEqual(
            [('a', i + 1, j + 1, 0) for i in range(500) for j in range(100)],
            search_for_entries(text, sear_words, ''))

    def test_case_insensitivity(self):
        sear_words = ['abc']
        text = ['abc', 'Abc', 'ABc', 'ABC', 'aBC']
        self.assertEqual([('abc', 1, 1, 0),
                          ('Abc', 2, 1, 0),
                          ('ABc', 3, 1, 0),
                          ('ABC', 4, 1, 0),
                          ('aBC', 5, 1, 0)], search_for_entries(text, sear_words, ''))

        sear_words = ['AsF']
        text = ['asf', 'asd']
        self.assertEqual([('asf', 1, 1, 0), ('asd', 2, 1, 1)], search_for_entries(text, sear_words, ''))

    def test_line_break(self):
        sear_words = ['hello']
        text = ['hel-', 'lo']
        self.assertEqual([('hello', 1, 1, 0)], search_for_entries(text, sear_words, ''))

        sear_words = ['hello']
        text = ['hel-as', 'lo']
        self.assertEqual([], search_for_entries(text, sear_words, ''))

        sear_words = ['hello']
        text = ['hel-', '', 'lo']
        self.assertEqual([], search_for_entries(text, sear_words, ''))

        sear_words = ['hello']
        text = ['asd hel-', 'lo']
        self.assertEqual([('hello', 1, 2, 0)], search_for_entries(text, sear_words, ''))

        sear_words = ['asd-hello']
        text = ['asd-hel-', 'lo']
        self.assertEqual([('asd-hello', 1, 1, 0)], search_for_entries(text, sear_words, ''))

        sear_words = ['hello', 'lines']
        text = ['hel-', 'lo li-', 'nes']
        self.assertEqual([('hello', 1, 1, 0), ('lines', 2, 2, 0)], search_for_entries(text, sear_words, ''))

    def test_empty_list(self):
        regex = re.compile(r'[\w\d\'\"-]+')
        self.assertEqual([], get_words([], regex))

    def test_get_word_without_changes(self):
        regex = re.compile(r'[\w\d\'\"-]+')

        list = ['qwerty', 'qwer', 'qwe']
        self.assertEqual(list, get_words(list, regex))

        list = ['non-stop', '"Test"']
        self.assertEqual(['non-stop', '"Test"'], get_words(list, regex))

    def test_get_changed_list(self):
        regex = re.compile(r'[\w\d\'\"-]+')

        data = ['hello', 'a=', 'split!']
        self.assertEqual(['hello', 'a', 'split'], get_words(data, regex))

        data = ['a=a', '13!=12']
        self.assertEqual(['a', 'a', '13', '12'], get_words(data, regex))

        data = ['It\'s', ',asd,d', '===']
        self.assertEqual(['It\'s', 'asd', 'd'], get_words(data, regex))

    def test_distance_of_Levenshtein(self):
        self.assertEqual(0, get_distance('asdf', 'asdf'))

        self.assertEqual(1, get_distance('ab', 'ac'))
        self.assertEqual(1, get_distance('My name is Ssm', 'My name is Sam'))
        self.assertEqual(1, get_distance('asd', 'aasd'))

        self.assertEqual(2, get_distance('', 'as'))
        self.assertEqual(2, get_distance('as', ''))
        self.assertEqual(2, get_distance('hello', 'helol'))

        self.assertEqual(3, get_distance('1234', '1'))
        self.assertEqual(3, get_distance('qwe', 'rty'))
        self.assertEqual(3, get_distance('1', '1234'))
