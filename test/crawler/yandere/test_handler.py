from unittest import TestCase

from crawler.yandere.handler import QueryPageHandler
from crawler.selector import Selector
from test.utility import read_file

# TODO: CODE DUPLICATION, REFACOTOR FURTHER


class TestQueryPageHandler(TestCase):

    def setUp(self):
        self.test_html = read_file('test/crawler/yandere/query_list_test_1')

    def test_query_page_handler(self):
        selector = Selector()
        selector.add_normal_selector(lambda pic: pic['score'] > 20)

        querypage_handler = QueryPageHandler(selector)
        result = querypage_handler(self.test_html)

        self.assertEqual(len(result), 1)

    def test_query_page_handler_false_example(self):
        selector = Selector()
        selector.add_normal_selector(lambda pic: pic['score'] > 30)

        querypage_handler = QueryPageHandler(selector)
        result = querypage_handler(self.test_html)

        self.assertEqual(len(result), 0)
