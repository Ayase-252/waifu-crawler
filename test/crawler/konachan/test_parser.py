from unittest import TestCase

from test.utility import read_file
from crawler.konachan.parser import *


class TestParseQueryPage(TestCase):

    def test_parse_query_test_sample(self):
        sample = read_file('test/crawler/konachan/query_page_sample')
        result = parse_query_page(sample)
        self.assertIn({
            'id': 234859,
            'rating': 'Safe',
            'score': 14,
            'tags': ['animal ears', 'mazume', 'original'],
            'link': 'http://konachan.net/post/show/234859',
        }, result)
        self.assertIn({
            'id': 234858,
            'rating': 'Safe',
            'score': 55,
            'tags': ['cropped', 'ichinose shiki', 'idolmaster',
                     'idolmaster cinderella girls', 'mossi'],
            'link': 'http://konachan.net/post/show/234858'
        }, result)


class TestParseDetailPage(TestCase):

    def test_parse_detail_page(self):
        sample = read_file('test/crawler/konachan/detail_page_png')
        result = parse_detail_page(sample)
        self.assertIn({
            'type': 'png',
            'link': 'http://konachan.net/image/507cc0ad7ced2572b81c0aa5372ec30'
                    '9/Konachan.com%20-%20230187%20animal%20animal_ears%20biki'
                    'ni%20blush%20breasts%20cat%20catgirl%20cleavage%20fang%20'
                    'kantoku%20kurumi_%28kantoku%29%20long_hair%20original%20p'
                    'hotoshop%20scan%20skirt%20swimsuit%20tail%20white.png'
        }, result)
        self.assertIn({
            'type': 'jpeg',
            'link': 'http://konachan.net/jpeg/507cc0ad7ced2572b81c0aa5372ec309'
            '/Konachan.com%20-%20230187%20animal%20animal_ears%20bikini%20blus'
            'h%20breasts%20cat%20catgirl%20cleavage%20fang%20kantoku%20kurumi_'
            '%28kantoku%29%20long_hair%20original%20photoshop%20scan%20skirt'
            '%20swimsuit%20tail%20white.jpg'
        }, result)
