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


class DetailPageParserTest(TestCase):

    def test_parse_detail_page_snippet(self):
        test_snippet = read_file('test/yandere/detail_page_test_1')

        picture_detail = parser.parse_detail_page(test_snippet)
        self.assertEqual({
            'download links': [{
                'type': 'png',
                'link': 'https://files.yande.re/image/ca41485c5427540bf1c975bee7dd768a/yande.re%20377574%20chuuko_demo_koi_ga_shitai%21%20digital_version%20redrop%20seifuku.png'
            }, {
                'type': 'jpeg',
                'link': 'https://files.yande.re/jpeg/ca41485c5427540bf1c975bee7dd768a/yande.re%20377574%20chuuko_demo_koi_ga_shitai%21%20digital_version%20redrop%20seifuku.jpg'
            }]
        }, picture_detail)

    def test_parse_detail_page_snippet_no_png(self):
        test_snippet = read_file('test/yandere/detail_page_test_no_png')

        picture_detail = parser.parse_detail_page(test_snippet)
        self.assertEqual({
            'download links': [{
                'type': 'jpeg',
                'link': 'https://files.yande.re/jpeg/ca41485c5427540bf1c975bee7dd768a/yande.re%20377574%20chuuko_demo_koi_ga_shitai%21%20digital_version%20redrop%20seifuku.jpg'
            }]
        }, picture_detail)
