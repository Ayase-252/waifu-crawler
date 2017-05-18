from unittest import TestCase
from datetime import datetime
from os import path, remove, removedirs

from requests_mock import Mocker
from requests.exceptions import ConnectTimeout

from request import AsyncRequestScheduler
from test.utility import read_as_binary


class TestGetMethod(TestCase):
    @Mocker()
    def test_get_method(self, mocker):
        mocker.get('mock://test.com', text='right text')

        request_scheduler = AsyncRequestScheduler(100)
        res = request_scheduler.get('mock://test.com')

        self.assertEqual(res.text, 'right text')

    @Mocker()
    def test_resume_from_failed_request(self, mocker):
        mocker.get('mocker://test.com', exc=ConnectTimeout)

        request_scheduler = AsyncRequestScheduler(100)
        with self.assertRaises(ConnectTimeout):
            request_scheduler.get('mocker://test.com')

        mocker.get('mocker://test.com', text='right text')
        res = request_scheduler.get('mocker://test.com')
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


class TestDownloader(TestCase):
    @Mocker()
    def test_download_without_specified_path(self, mocker):
        mocker.get('mocker://test.com', content=b'that it is.')

        request_scheduler = AsyncRequestScheduler(100)
        request_scheduler.download('mocker://test.com', 'test.file')

        self.assertTrue(path.isfile('test.file'))
        self.assertEqual(read_as_binary('test.file'), b'that it is.')

        remove('test.file')

    @Mocker()
    def test_download_with_specified_path(self, mocker):
        mocker.get('mocker://test.com', content=b'that it is.')

        request_scheduler = AsyncRequestScheduler(100)
        request_scheduler.download('mocker://test.com', 'test.file',
                                   'testdir')

        target_path = path.abspath('./testdir')
        target_file_path = path.join(target_path, 'test.file')
        self.assertTrue(path.isfile(target_file_path))
        with open(target_file_path, encoding='utf-8') as f:
            result = f.read().encode('utf-8')
        self.assertEqual(result, b'that it is.')

        remove(target_file_path)
        removedirs(target_path)
