from unittest import TestCase

from test.utility import read_file
from crawler.konachan.parser import *


class TestParseQueryPage(TestCase):

    def test_parse_query_test_sample(self):
        sample = read_file('test/crawler/konachan/query_page_sample')
        result = parse_query_page_new(sample)
        self.assertIn({
            'id': 234859,
            'rating': 'Safe',
            'score': 14,
            'tags': ['anime ears', 'mazume', 'original'],
            'link': 'http://konachan.net/post/show/234859',
        }, result)
        self.assertIn({
            'id': 234858,
            'rating': 'Safe',
            'score': 55,
            'tags': ['cropped', 'ichinose shiki', 'idolmaster', 'idolmaster \
                     cinderella girls', 'mossi'],
            'link': 'http://konachan.net/post/show/234858'
        })
