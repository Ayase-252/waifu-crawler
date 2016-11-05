"""
Unit tests of Parser
"""
from unittest import TestCase

from crawler.parser import parse_query_page, parse_detail_page


class ParserTest(TestCase):
    """
    Unit tests of Parser
    """

    def test_parse_query_page(self):
        """
        Parse a query page.
        """
        test_page = open(r'test/crawler/query_page.html', encoding='utf-8')
        test_page_text = test_page.read()
        test_page.close()

        def decision_func(score):
            return score >= 100

        results = parse_query_page(
            test_page_text, 'http://konachan.net', decision_func)

        expected_result = (
            'http://konachan.net/post/show/230189/animal_ears-bed-bell-blonde_hair-blush-catgirl-col',
            'http://konachan.net/post/show/230187/5_nenme_no_houkago-animal-animal_ears-bikini-blush',
            'http://konachan.net/post/show/230181/aqua_eyes-bikini-blonde_hair-breasts-car-gun-hamad',
            'http://konachan.net/post/show/230175/breasts-cherry-cleavage-collar-demon-drink-flowers'
        )
        self.assertEqual(set(results), set(expected_result))

    def test_parse_detail_page_with_png(self):
        """
        Parse a detail page with PNG download link.
        """
        test_page = open(r'test/crawler/png_download.html', encoding='utf-8')
        test_page_text = test_page.read()
        test_page.close()

        result = parse_detail_page(test_page_text)

        self.assertEqual(result,
                         {
                             'pid': 230187,
                             'url': 'http://konachan.net/image/507cc0ad7ced2572b81c0aa5372ec309/Konachan.com%20-%20230187%20animal%20animal_ears%20bikini%20blush%20breasts%20cat%20catgirl%20cleavage%20fang%20kantoku%20kurumi_%28kantoku%29%20long_hair%20original%20photoshop%20scan%20skirt%20swimsuit%20tail%20white.png',
                             'ptype': 'png'
                         }
        )

    def test_parse_detail_page_with_jpg(self):
        """
        Parse a detail page with JPG download link.
        """
        test_page = open(r'test/crawler/jpg_download.html', encoding='utf-8')
        test_page_text = test_page.read()
        test_page.close()

        result = parse_detail_page(test_page_text)

        self.assertEqual(result, {
            'pid': 230198,
            'url': 'http://konachan.net/image/1db6a04b60041c2a5471d2e6a045d987/Konachan.com%20-%20230198%20bikini%20blonde_hair%20breasts%20cleavage%20collar%20gloves%20green_eyes%20headdress%20idolmaster%20maid%20navel%20short_hair%20swimsuit%20tagme_%28artist%29%20thighhighs%20water.jpg',
            'ptype': 'jpg'
        })

    def test_parse_detail_page_with_jpg_v1(self):
        """
        Parse a detail page with JPG download link in other vesion.
        """
        test_page = open(r'test/crawler/jpg_download_ver1.html', encoding='utf-8')
        test_page_text = test_page.read()
        test_page.close()

        result = parse_detail_page(test_page_text)

        self.assertEqual(result, {
            'pid': 230180,
            'url': 'http://konachan.net/image/369c10e69e6b59da2345d4f077f7b006/Konachan.com%20-%20230180%20ass%20blue_eyes%20blue_hair%20boots%20car%20gedou_%28shigure_seishin%29%20kantai_collection%20pantyhose%20phone%20shade%20shorts%20sunglasses%20tree%20urakaze_%28kancolle%29%20wristwear.jpg',
            'ptype': 'jpg'
        })
