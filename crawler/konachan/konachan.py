"""
Konachan Cralwer

It crawls konachan.net searching pictures. If picture passes these tests, it
will be downloaded.
"""

from crawler.crawler import Crawler


class KonachanCralwer(Crawler):
    """
    Konachan Cralwer
    """

    def __init__(self, **kwargs):
        """
        Initial cralwer
        """
        pass

    def run(self):
        """
        Drives the cralwer ^_^.
        """
        raise NotImplementedError
