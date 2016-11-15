"""
Request Scheduler Unit Tests
"""
import unittest

from requests_mock import Mocker

from request.scheduler import RequestScheduler


class RequestSchedulerTest(unittest.TestCase):
    """
    Request Scheduler Unit Tests
    """
    @staticmethod
    def request_interval_test(asserter, mocker, expected_interval):
        """
        Test whether requests are sent in given interval.
        """
        mocker.get(r'http://test.com')
        RequestScheduler.initialize(request_interval=expected_interval)
        request_id_1 = RequestScheduler.request(r'http://test.com')
        request_id_2 = RequestScheduler.request(r'http://test.com')
        RequestScheduler.wait()
        request_time_1 = RequestScheduler.get_sent_time(request_id_1)
        request_time_2 = RequestScheduler.get_sent_time(request_id_2)
        actual_interval = (request_time_2 - request_time_1).microseconds
        asserter.assertGreaterEqual(
            actual_interval, expected_interval,
            msg='Actual interval {0} is less than expected {1}'.format(
                actual_interval, expected_interval
            )
        )
        RequestScheduler.wait()

    @Mocker()
    def test_request_one_page(self, mocker):
        """
        Test request a page via request scheduler
        """
        mocker.get(r'http://test.com', text='hello world')
        RequestScheduler.initialize()
        request_id = RequestScheduler.request(r'http://test.com',
                                              save_response=True)
        RequestScheduler.wait()
        response = RequestScheduler.get_response(request_id)
        self.assertEqual(response.url, r'http://test.com/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'hello world')

    @Mocker()
    def test_consecutive_requests(self, mocker):
        """
        Test consecutive requests
        """
        interval_to_test = [500, 1000, 2000]
        for interval in interval_to_test:
            self.request_interval_test(self, mocker, interval)

    @Mocker()
    def test_failed_request(self, mocker):
        """
        Request is failed.
        """
        mocker.get(r'http://test.com', status_code=404)
        RequestScheduler.initialize()
        request_id = RequestScheduler.request(r'http://test.com')
        while RequestScheduler.is_working():
            pass

        self.assertTrue(RequestScheduler.is_failed(request_id))
        self.assertFalse(RequestScheduler.is_success(request_id))

    @Mocker()
    def test_check_is_working(self, mocker):
        """
        Checks whether task is scheduled.
        """
        mocker.get(r'http://test.com', text='hello world')
        #   Long interval make sure some requests will not be executed in
        #   this test.
        RequestScheduler.initialize(request_interval=2000)
        RequestScheduler.request(r'http://test.com')
        RequestScheduler.request(r'http://test.com')

        self.assertTrue(RequestScheduler.is_working())
        RequestScheduler.wait()

    @Mocker()
    def test_new_web_page_request_method(self, mocker):
        """
        Check new web page request method
        """
        mocker.get(r'http://test.com', text='hello world')

        RequestScheduler.initialize()
        RequestScheduler.schedule_get(
            url='http://test.com',
            pre_request_handler=lambda: print('pre request handler'),
            success_handler=lambda response: self.assertEqual(response, 'hello world'),
            fail_handler=lambda ex: self.assertIsNone(ex))
