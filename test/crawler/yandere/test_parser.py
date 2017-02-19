from unittest import TestCase

from crawler.yandere import parser
from test.utility import *


class QueryListParserTest(TestCase):

    def test_parse_query_list_snippet(self):
        test_snippet = read_file('test/crawler/yandere/query_list_test_1')

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
        test_snippet = read_file('test/crawler/yandere/detail_page_test_1')

        picture_detail = parser.parse_detail_page(test_snippet)
        self.assertEqual({
            'png': 'https://files.yande.re/image/ca41485c5427540bf1c975bee7dd768a/yande.re%20377574%20chuuko_demo_koi_ga_shitai%21%20digital_version%20redrop%20seifuku.png',
            'jpeg': 'https://files.yande.re/jpeg/ca41485c5427540bf1c975bee7dd768a/yande.re%20377574%20chuuko_demo_koi_ga_shitai%21%20digital_version%20redrop%20seifuku.jpg'
        }, picture_detail)

    def test_parse_detail_page_snippet_no_png(self):
        test_snippet = read_file(
            'test/crawler/yandere/detail_page_test_no_png')

        picture_detail = parser.parse_detail_page(test_snippet)
        self.assertEqual({
            'jpeg': 'https://files.yande.re/jpeg/ca41485c5427540bf1c975bee7dd768a/yande.re%20377574%20chuuko_demo_koi_ga_shitai%21%20digital_version%20redrop%20seifuku.jpg'
        }, picture_detail)


class TitleParserTest(TestCase):

    def test_title_parser_1(self):
        title_text = 'Rating: Questionable Score: 3 Tags: christmas cleavage erect_nipples kantai_collection no_bra open_shirt pantsu suzuya_(kancolle) thighhighs yuzuka User: mash'
        result = parser.parse_title(title_text)

        self.assertEqual(result,
                         {
                             'rating': 'Questionable',
                             'score': 3,
                             'tags': ['christmas', 'cleavage', 'erect nipples',
                                      'kantai collection', 'no bra', 'open shirt', 'pantsu',
                                      'suzuya (kancolle)', 'thighhighs', 'yuzuka']
                         })

    def test_title_parser_2(self):
        title_text = 'Rating: Safe Score: 10 Tags: aqua_(kono_subarashii_sekai_ni_shukufuku_wo!) kono_subarashii_sekai_ni_shukufuku_wo! saraki see_through User: Humanpinka'
        result = parser.parse_title(title_text)

        self.assertEqual(result,
                         {
                             'rating': 'Safe',
                             'score': 10,
                             'tags': ['aqua (kono subarashii sekai ni shukufuku wo!)',
                                      'kono subarashii sekai ni shukufuku wo!',
                                       'saraki',
                                      'see through']
                         })
