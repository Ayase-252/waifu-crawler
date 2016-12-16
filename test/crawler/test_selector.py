import unittest
from crawler.selector import *


class PictureFliterTest(unittest.TestCase):

    def test_normal_selector(self):
        to_testlist = [{
            'id': 1,
            'score': 60,
            'tags': ['select it', 'whatever'],
        }, {
            'id': 2,
            'score': 70,
            'tags': ['whatever'],
        }, {
            'id': 3,
            'score': 80,
            'tags': ['bouns']
        }]

        selector = Selector()
        selector.add_normal_selector(
            lambda picture_info: picture_info['score'] > 70)
        result = selector.select(to_testlist)

        self.assertIn({
            'id': 3,
            'score': 80,
            'tags': ['bouns']}, result)

    def test_decisive_selector(self):
        to_testlist = [{
            'id': 1,
            'score': 60,
            'tags': ['select it', 'whatever'],
        }, {
            'id': 2,
            'score': 70,
            'tags': ['whatever'],
        }, {
            'id': 3,
            'score': 80,
            'tags': ['bouns']
        }]
        selector = Selector()
        selector.add_decisive_selector(
            lambda picture_info: 'select it' in picture_info['tags'])
        result = selector.select(to_testlist)

        self.assertIn({
            'id': 1,
            'score': 60,
            'tags': ['select it', 'whatever'],
        }, result)
