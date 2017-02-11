from unittest import TestCase
from datetime import datetime

from requests_mock import Mocker

from request.request_async import AsyncRequestScheduler


class TestGetMethod(TestCase):
    @Mocker()
    def test_get_method(self, mocker):
        mocker.get('mock://test.com', text='right text')

        request_scheduler = AsyncRequestScheduler(100)
        res = request_scheduler.get('mock://test.com')

        self.assertEqual(res.text, 'right text')


class TestIntervalControl(TestCase):
    @Mocker()
    def test_interval_control(self, mocker):
        mocker.get('mock://test.com')

        request_scheduler = AsyncRequestScheduler(100)
        time_start = datetime.now()
        request_1 = request_scheduler.get('mock://test.com')
        request_2 = request_scheduler.get('mock://test.com')
        time_end = datetime.now()
        time_delta = (time_end - time_start).microseconds

        self.assertGreater(time_delta, 100)
