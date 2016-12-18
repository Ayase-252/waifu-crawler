from unittest import TestCase

from yandere import parser
from test.utility import *


class QueryListParserTest(TestCase):
    def test_parse_query_list_snippet(self):
        test_snippet = read_file('test/yandere/query_list_test_1')

        pictures = parser.parse_query_list(test_snippet)
        self.assertIn({
            'id': 377505,
            'tags': ['kimi no na wa', 'miyamizu mitsuha', 'seifuku'],
            'score': 21,
            'rating': 'Safe',
            'detail url': 'https://yande.re/post/show/377505'
        }, pictures)
