from unittest import TestCase
from os import path, remove

from requests_mock import Mocker

from yandere.command import *
from yandere.selector import *
from test.utility import read_file, read_as_binary

class RunTest(TestCase):

    def setUpTestCase(self, mocker):
        # Setup query page
        mocker.get('https://yande.re/post?page=1',
                   text=read_file('test/yandere/query_list_safe_test'))

        # Setup detail page
        mocker.get('https://yande.re/post/show/377505',
                   text=read_file('test/yandere/detail_page_377505'))

        # Setup target file
        mocker.get('https://files.yande.re/image/64c7aeade1c09807a1417cfe873b81e1/yande.re%20377505%20kimi_no_na_wa%20miyamizu_mitsuha%20seifuku.png',
                   content=read_as_binary('test/yandere/picture_target'))

    @Mocker()
    def test_run_with_safe_seletor(self, mocker):
        self.setUpTestCase(mocker)

        run(pages=1, selector=safe_selector)

        self.assertTrue(path.isfile('yandere-377505.png'))
        self.assertEqual(read_file('yandere-377505.png'),
                         'If you read this, it is right!')
        remove('yandere-377505.png')
