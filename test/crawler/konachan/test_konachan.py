from unittest import TestCase, skip
from os import remove

from requests_mock import Mocker

from crawler.selector import Selector
from test.utility import read_file, read_as_binary
from crawler.konachan.konachan import KonachanCralwer

TEST_FIXTURE_ROOT = r'test/crawler/konachan/'


def setup_fixture(mocker):
    mocker.get('http://konachan.net/post?page=1',
               text=read_file(TEST_FIXTURE_ROOT + 'konachanrun_qp_1'))
    mocker.get('http://konachan.net/post?page=2',
               text=read_file(TEST_FIXTURE_ROOT + 'konachanrun_qp_2'))
    mocker.get('http://konachan.net/post/show/235050/flower_knight_girl-'
               'houzuki_michiru-waifu2x',
               text=read_file(TEST_FIXTURE_ROOT + 'konachanrun_dp_235050'))
    mocker.get('http://konachan.net/post/show/235057/animal_ears-arukesah-'
               'ass-barefoot-catgirl-fang-gra',
               text=read_file(TEST_FIXTURE_ROOT + 'konachanrun_dp_235057'))
    mocker.get('http://konachan.nethttp://konachan.net/post/show/235044/'
               'aliasing-animal-barefoot-black_hair-cropped-dress-',
               text=read_file(TEST_FIXTURE_ROOT + 'konachanrun_dp_235044'))
    mocker.get('http://konachan.net/post/show/235031/breasts-dress-fate-grand'
               '_order-fate_-series-glasse',
               text=read_file(TEST_FIXTURE_ROOT + 'konachanrun_dp_235031'))
    mocker.get('http://konachan.net/image/37c6cf9a53b4eec64ca409e236add764/Konachan.com%20-%20235050%20flower_knight_girl%20houzuki_michiru%20waifu2x.png',
               content=b'235050')
    mocker.get('http://konachan.net/image/91606173f47d94c0bc861180aebfacf6/Konachan.com%20-%20235057%20animal_ears%20arukesah%20ass%20barefoot%20catgirl%20fang%20gray_hair%20green_eyes%20original%20short_hair%20tail.jpg',
               content=b'235057')
    mocker.get('http://konachan.net/image/e571a2395730046075bf88abf2c13f34/Konachan.com%20-%20235044%20aliasing%20animal%20barefoot%20black_hair%20cropped%20dress%20fish%20flowers%20instrument%20original%20piano%20short_hair%20summer_dress%20watermark%20wenqing_yan_%28yuumei_art%29.png',
               content=b'235044')
    mocker.get('http://konachan.net/image/f998caea4a94aa642183f794d9b336b2/Konachan.com%20-%20235031%20breasts%20dress%20fate_grand_order%20fate_%28series%29%20glasses%20matthew_kyrielite%20pantyhose%20purple_eyes%20purple_hair%20rong_yi_tan%20short_hair%20tie.png',
               content=b'235031')


@skip('unimplemented')
class TestKonachanRun(TestCase):

    @Mocker()
    def test_normal_run(self, mocker):
        """
        Tests run of Konachan cralwer.

        Test fixture contains two query pages. Test supplies a
        selector filtering picture in score.
        """
        # Setup test fixtures
        setup_fixture(mocker)

        konachan = KonachanCralwer()
        # run cralwer
        konachan.run(
            save_dir='.',
            no_sub_dir=True,
            pages=2
        )

        # Assert
        self.assertEqual(read_file('235057.jpg'), 235057)
        self.assertEqual(read_file('235050.png'), 235050)
        self.assertEqual(read_file('235044.png'), 235044)
        self.assertEqual(read_file('235031.png'), 235031)

    def tearDown(self):
        remove('235057.jpg')
        remove('235050.png')
        remove('235044.png')
        remove('235031.png')
