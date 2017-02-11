from unittest import TestCase

from crawler.yandere import selector


class SafeSelectorTest(TestCase):

    def test_safe_picture(self):
        picture_info = {
            'id': 123456,
            'rating': 'Safe'
        }
        self.assertTrue(selector.safe_selector(picture_info))

    def test_questionable_picture(self):
        picture_info = {
            'id': 124235,
            'rating': 'Questionable'
        }
        self.assertFalse(selector.safe_selector(picture_info))


class ScoreSelectorFactoryTest(TestCase):
    def test_positive_case(self):
        picture_info = {
            'id': 728378,
            'score': 30
        }

        score_selector = selector.score_selector_factory(20)
        self.assertTrue(score_selector(picture_info))

    def test_false_case(self):
        picture_info = {
            'id': 793012,
            'score': 10
        }
        score_selector = selector.score_selector_factory(20)
        self.assertFalse(score_selector(picture_info))
