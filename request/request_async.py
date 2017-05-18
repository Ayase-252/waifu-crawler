"""
Asynchronous Request Library

This module re-implemented previous `scheduler` which relys on callback.
Methods in this version are written with asynchronous support of Python
language.
"""

from datetime import datetime
from os import path, mkdir
from math import floor

import requests

from display import ProgressBar

# Connection Timeout set
# See http://docs.python-requests.org/en/master/user/advanced/
# Timeouts
_CONNECT_TIMEOUT = 15
_READ_TIMEOUT = 60


class AsyncRequestScheduler:
    """
    Scheduler of outcoming request
    """

    def __init__(self, request_interval):
        """
        Constructor

        params:
        request_interval        Time interval of requests(in ms)
        """
        self._request_interval = request_interval
        self._send_request_iter = self._send_request()
        next(self._send_request_iter)

    def _send_request(self):
        """
        Send request to remote server
        """
        last_request_time = None
        request_methods = {
            'GET': requests.get
        }
        ua = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/'
            '537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        next_request = yield
        url = next_request['url']
        method = next_request['method']
        params = next_request['params']
        stream = next_request['stream']
        while True:
            if last_request_time is not None:
                time_interval = (datetime.now() -
                                 last_request_time).microseconds
                if time_interval < self._request_interval:
                    continue
            last_request_time = datetime.now()
            next_request = yield request_methods[method](
                url, params,
                headers=ua,
                stream=stream,
                timeout=(_CONNECT_TIMEOUT, _READ_TIMEOUT)
            )
            url = next_request['url']
            method = next_request['method']
            params = next_request['params']
            stream = next_request['stream']

    def get(self, url, params=None, stream=False):
        """
        Wrapper of get method

        parmas:
        url         URL
        parmas      Parameters of the request
        """
        try:
            return self._send_request_iter.send({
                'url': url,
                'method': 'GET',
                'params': params,
                'stream': stream
            })
        except StopIteration:
            self._send_request_iter = self._send_request()
            next(self._send_request_iter)
            return self._send_request_iter.send({
                'url': url,
                'method': 'GET',
                'params': params,
                'stream': stream
            })

    def download(self, url, file_name, file_path=None):
        """
        Download file

        Download file from remote server and save it in specified path.

        params:
        url                         URL of file
        file_name
        file_path   default None    If not None, it is relative path to home
                                    directory.
        """
        response = self.get(url, stream=True)
        if file_path is not None:
            file_root = path.abspath(file_path)
            if not path.isdir(file_root):
                mkdir(file_root)
        else:
            file_root = path.abspath('.')

        total_length = response.headers.get('content-length')

        if total_length is None:
            print("Website doesn't provides content-length. Therefore progress"
                  " bar cannot work. Please wait..")
            file_content = response.content

        else:
            downloaded_size = 0
            total_length = int(total_length)
            progress_bar = ProgressBar(total_length)
            file_content = b''
            for data in response.iter_content(chunk_size=4096):
                file_content += data
                downloaded_size += len(data)
                progress = floor(downloaded_size / total_length * 100)
                progress_bar.set_progress(progress)
            if downloaded_size != total_length:
                raise RuntimeError('Connection is broken.')

        with open(path.join(file_root, file_name), 'wb') as f:
            f.write(file_content)
