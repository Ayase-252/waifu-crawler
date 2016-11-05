"""
Request scheduler

This module handles requests to hosts in regulated way. e.g constant request
rate. Request in this library will behave in asynchonous way.
"""
from datetime import datetime, timedelta
from threading import Thread, Timer, Lock, current_thread
import warnings

import requests
from .memory import RequestMemory


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
            Thread(target=cls._request, kwargs=request_kwargs).run()
        else:
            Timer(interval/1000, function=cls._request, kwargs=request_kwargs).start()
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
            (datetime.now() - cls.latest_request_time).microseconds / 1000 >= cls.request_interval

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
        cls._decrease_pending_counter()
        cls.request_memory.update(request_id, {
            'status': 'Success',
            'response': response
        })

    @classmethod
    def _fail_request(cls, request_id):
        """
        Set request has failed
        """
        cls._decrease_pending_counter()
        cls.request_memory.update(request_id, {
            'status': 'Failed'
        })

    @classmethod
    def _increase_pending_counter(cls):
        """
        """
        cls._counter_lock.acquire()
        cls.pending_requests += 1
        cls._counter_lock.release()

    @classmethod
    def _decrease_pending_counter(cls):
        """
        """
        cls._counter_lock.acquire()
        cls.pending_requests -= 1
        cls._counter_lock.release()
