"""
Request scheduler

This module handles requests to hosts in regulated way. e.g constant request
rate. Request in this library will behave in asynchonous way.
"""
from datetime import datetime, timedelta
from threading import Lock
import warnings

import requests
from thread_manager.thread_manager import ThreadManager
from .memory import RequestMemory
from logger import getLogger

logger = getLogger('waife-crawler.scheduler')


class RequestScheduler:
    """
    Request Scheduler
    """
    @classmethod
    def initialize(cls, request_interval=500):
        """
        Initializes a request scehduler

        params:
        request_interval    Minimal interval between two consecutive requests
        """

        cls.request_interval = request_interval
        cls.request_memory = RequestMemory()
        cls.latest_request_time = None
        cls.pending_requests = 0
        logger.debug('Counter lock is initialized.')
        cls._counter_lock = Lock()

    @classmethod
    def request(cls, url, response_handler=None, *, params=None, headers=None,
                save_response=False, handler_kwargs=None):
        """
        Makes a request to resource donated by url. Request will be delegated to
        a worker thread and may get delayed in the restrict of interval. In
        other words, the method is asynchonous.

        params:
        url                         URL
        response_handler            Callback function when response is avaliable
        params                      Parameters of the request
        headers                     Headers of the request
        save_response               Whether the response should be saved

        returns:
        ID of request for later use.
        """
        warnings.warn('Deprecated. Use schedule_get() and schedule_get_binary() instead.',
                      DeprecationWarning)
        can_be_sent_immediately = False
        if cls._is_ready_for_send_request_now():
            can_be_sent_immediately = True
            request_time = datetime.now()
        else:
            interval = cls._remaining_waiting_time()
            request_time = datetime.now() + timedelta(milliseconds=interval)
        request_id = cls.request_memory.create()
        request_kwargs = {
            'url': url,
            'request_id': request_id,
            'response_handler': response_handler,
            'params': params,
            'headers': headers,
            'save_response': save_response,
            'handler_kwargs': handler_kwargs
        }
        cls._pend_request(request_id, request_time)
        if can_be_sent_immediately:
            ThreadManager.run(function=cls._request, kwargs=request_kwargs,
                              success_handler=cls._decrease_pending_counter,
                              fail_handler=cls._decrease_pending_counter)
        else:
            ThreadManager.run_after(interval / 1000, function=cls._request,
                                    kwargs=request_kwargs,
                                    success_handler=cls._decrease_pending_counter,
                                    fail_handler=cls._decrease_pending_counter)
        return request_id

    @classmethod
    def is_completed(cls, request_id):
        """
        Checks request has completed
        """
        warnings.warn('Deprecated due to high posibility to cause dead lock',
                      DeprecationWarning)
        result = cls.request_memory.retrieve(request_id)
        return result['status'] in ['Success', 'Failed']

    @classmethod
    def is_failed(cls, request_id):
        """
        Checks request has been failed
        """
        warnings.warn('Deprecated due to high posibility to cause dead lock',
                      DeprecationWarning)
        result = cls.request_memory.retrieve(request_id)
        return result['status'] == 'Failed'

    @classmethod
    def is_success(cls, request_id):
        """
        Checks request has been success
        """
        warnings.warn('Deprecated due to high posibility to cause dead lock',
                      DeprecationWarning)
        result = cls.request_memory.retrieve(request_id)
        return result['status'] == 'Success'

    @classmethod
    def get_response(cls, request_id):
        """
        Get response of request donated by request_id

        returns:
        response objects if request succeeded and save_response is True,
        otherwise None
        """
        warnings.warn('Deprecated due to high posibility to cause dead lock',
                      DeprecationWarning)
        result = cls.request_memory.retrieve(request_id)
        if result is not None:
            return result['response']
        else:
            return None

    @classmethod
    def get_sent_time(cls, request_id):
        """
        Gets the time when the request sent
        """
        warnings.warn('Deprecated. Support to get sent time will be terminated.',
                      DeprecationWarning)
        request = cls.request_memory.retrieve(request_id)
        if 'sent time' in request:
            return request['sent time']
        else:
            return None

    @classmethod
    def is_working(cls):
        """
        """
        return cls.pending_requests != 0

    @classmethod
    def wait(cls):
        """
        """
        while cls.is_working():
            pass

    @classmethod
    def _request(cls, url, request_id, response_handler=None, *, params=None,
                 headers=None, save_response, handler_kwargs):
        """
        Function delegated to a worker thread to do actual request.

        params:
        refers to requst
        """
        user_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.'
                          '36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        if headers is not None:
            user_headers.update(headers)
        cls._send_request(request_id)
        response = requests.get(url, params=params, headers=user_headers)
        if response.status_code != 200:
            cls._fail_request(request_id)
            raise RuntimeError(
                'Response with status_code %d', response.status.code)
        else:
            if response_handler is not None:
                if handler_kwargs is not None:
                    response_handler(response, **handler_kwargs)
                else:
                    response_handler(response)
            if not save_response:
                response = None
            cls._succeed_request(request_id, response)

    @classmethod
    def _is_ready_for_send_request_now(cls):
        """
        Test whether a request can be sent immediately
        """
        return cls.latest_request_time is None or \
            (datetime.now() - cls.latest_request_time).microseconds / \
            1000 >= cls.request_interval

    @classmethod
    def _set_latest_request_time(cls, time_delayed=0):
        """
        Set latest request time based on now and time delayed
        """
        cls.latest_request_time = datetime.now() + \
            timedelta(milliseconds=time_delayed)

    @classmethod
    def _remaining_waiting_time(cls):
        """
        Remaining waiting time for next request

        Returns time in milliseconds
        """
        if cls.latest_request_time is not None:
            remaining_time = cls.request_interval - \
                ((datetime.now() - cls.latest_request_time).total_seconds() * 1000)
        else:
            remaining_time = 0
        return max(remaining_time, 0)

    @classmethod
    def _pend_request(cls, request_id, request_time):
        """
        Set request donated by request_id in pending status
        """
        cls._increase_pending_counter()
        cls.latest_request_time = request_time
        cls.request_memory.update(request_id, {
            'status': 'Pending',
            'request time': request_time
        })

    @classmethod
    def _send_request(cls, request_id):
        """
        Set request has been sent
        """
        cls.request_memory.update(request_id, {
            'status': 'Sent',
            'sent time': datetime.now()
        })

    @classmethod
    def _succeed_request(cls, request_id, response=None):
        """
        Set request has succeeded
        """
        # cls._decrease_pending_counter()
        cls.request_memory.update(request_id, {
            'status': 'Success',
            'response': response
        })

    @classmethod
    def _fail_request(cls, request_id):
        """
        Set request has failed
        """
        # cls._decrease_pending_counter()
        cls.request_memory.update(request_id, {
            'status': 'Failed'
        })

    @classmethod
    def _increase_pending_counter(cls, *args):
        """
        """
        cls._acquire_counter_lock()
        cls.pending_requests += 1
        logger.info('Pending thread counter increases to %d.',
                    cls.pending_requests)
        cls._release_counter_lock()

    @classmethod
    def _decrease_pending_counter(cls, *args):
        """
        """
        cls._acquire_counter_lock()
        cls.pending_requests -= 1
        logger.info('Pending thread counter decreases to %d.',
                    cls.pending_requests)
        cls._release_counter_lock()

    @classmethod
    def schedule_get(cls, url, *, params=None, headers=None, pre_request_handler=None,
                     success_handler=None, fail_handler=None):
        """
        Schedules a GET request to donated URL.

        Args:
        url                     URL of web resource requested
        *   (Below arguments are keyword arguments)
        params                  Parameters of request
        headers                 Headers of HTTP request
        pre_request_handler     Function being called right before request.
                                No argument is allowed.
                                It can be used to display a prompt to user.
        success_handler         Function being called after request returned
                                successfully.
                                The text of response will be the first
                                positional argument.
        failed_handler          Function being called after occurence of
                                exception.
                                Exception object will be the first positional
                                argument.
        """
        remaining_time_ms = cls._remaining_waiting_time()
        kwargs = {
            'url': url,
            'params': params,
            'headers': headers,
            'pre_request_handler': pre_request_handler
        }
        cls._increase_pending_counter()
        cls._set_latest_request_time(remaining_time_ms)
        if remaining_time_ms == 0:
            ThreadManager.run(function=cls._general_get,
                              kwargs=kwargs,
                              success_handler=success_handler,
                              fail_handler=fail_handler,
                              final_handler=cls._decrease_pending_counter)
        else:
            ThreadManager.run_after(remaining_time_ms / 1000,
                                    function=cls._general_get,
                                    kwargs=kwargs,
                                    success_handler=success_handler,
                                    fail_handler=fail_handler,
                                    final_handler=cls._decrease_pending_counter)

    @classmethod
    def _general_get(cls, url, *, params=None, headers=None, pre_request_handler=None):
        """
        Performs a GET request
        """
        pre_request_handler()
        request_headers = _generate_complete_header(headers)
        response = requests.get(url, params=params, headers=request_headers)
        if response.status_code != 200:
            raise RuntimeError(
                'Response failed, status code %d', response.status_code)
        return response.text

    @classmethod
    def _acquire_counter_lock(cls):
        logger.debug('Counter lock is acquired')
        cls._counter_lock.acquire()

    @classmethod
    def _release_counter_lock(cls):
        cls._counter_lock.release()
        logger.debug('Counter lock is released.')

    @classmethod
    def scheduler_get_js_ver(cls, url, *,
                             params=None, headers=None, callback=None):
        """
        This version uses callback convention of JavaScript. The first
        positional argument will be passed a error object if error arised in
        process. The second argument will be passed the result of request if
        request succeeds.
        """
        remaining_time_ms = cls._remaining_waiting_time()
        kwargs = {
            'url': url,
            'params': params,
            'headers': headers,
            'callback': callback
        }
        cls._increase_pending_counter()
        cls._set_latest_request_time(remaining_time_ms)
        if remaining_time_ms == 0:
            ThreadManager.simple_run(
                function=cls._scheduler_get_js_ver,
                **kwargs
            )
        else:
            ThreadManager.simple_run_after(
                remaining_time_ms / 1000,
                function=cls._scheduler_get_js_ver,
                **kwargs
            )

    @classmethod
    def _scheduler_get_js_ver(cls,
                              url, params=None, headers=None, callback=None):
        """
        Actual process of schduler_get_js_ver
        """
        request_headers = _generate_complete_header(headers)
        try:
            response = requests.get(url, params=params, headers=headers)
            if response.status_code != 200:
                raise RuntimeError('Request failed. Status code: %d',
                                   response.status_code)
            if callback is not None:
                callback(None, response)
        except AssertionError as assert_error:
            raise assert_error
        except Exception as general_error:
            if callback is not None:
                callback(general_error, None)
        finally:
            cls._decrease_pending_counter()


def _generate_complete_header(headers=None):
    ua_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.'
                      '36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    if headers is not None:
        return headers.update(ua_header)
    else:
        return ua_header
