from unittest import TestCase, skip
from os import path, remove

from requests_mock import Mocker

from crawler.yandere.yandere import YandereCrawler
from crawler.yandere.selector import *
from test.utility import read_file, read_as_binary


class RunTest(TestCase):

    def setUpTestCase(self, mocker):
        # Setup query page
        mocker.get('https://yande.re/post?page=1',
                   text=read_file('test/crawler/yandere/query_list_safe_test'))

        # Setup detail page
        mocker.get('https://yande.re/post/show/377505',
                   text=read_file('test/crawler/yandere/detail_page_377505'))

        # Setup target file
        mocker.get('https://files.yande.re/image/64c7aeade1c09807a1417cfe873b81e1/yande.re%20377505%20kimi_no_na_wa%20miyamizu_mitsuha%20seifuku.png',
                   content=read_as_binary('test/crawler/yandere/picture_target'))

    @Mocker()
    def test_run_with_default_set(self, mocker):
        """
        Enables safe selector
        """
        self.setUpTestCase(mocker)

        crawler = YandereCrawler(page_limit=1, score_filter=20)
        crawler.run()

        self.assertTrue(path.isfile('yandere-377505.png'))
        self.assertEqual(read_file('yandere-377505.png'),
                         'If you read this, it is right!\n')
        remove('yandere-377505.png')
        remove('yandere.log')


class DetailPageParsingFailTest(TestCase):
    def test_detail_page_parsing_failed(self):
        crawler = YandereCrawler()

        with self.assertRaisesRegex(RuntimeError, 'https://not.exist.com'):
            crawler._parse_detail_page('<p></p>', 'https://not.exist.com')


class DownloaderTest(TestCase):
    @Mocker()
    def test_jpeg_only_picture_test(self, mocker):
        mocker.get('mock://test.com', content=b'hello world')
        links = {
            'jpeg': 'mock://test.com'
        }
        id_ = 112233

        crawler = YandereCrawler()
        crawler._download(links, id_)

        self.assertTrue(path.isfile('yandere-112233.jpg'))
        self.assertEqual(read_as_binary('yandere-112233.jpg'),
                         b'hello world')
        remove('yandere-112233.jpg')
