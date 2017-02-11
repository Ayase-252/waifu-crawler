"""
Konachan Cralwer

It crawls konachan.net searching pictures. If picture passes these tests, it
will be downloaded.
"""

from crawler.crawler import Crawler

from request.scheduler import RequestScheduler


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
        url_base = r'https://yande.re/'
        page_limit = 10
        if page_limit in self:
            page_limit = self.page_limit
        for page_no in range(page_limit):
            post_page_url = url_base + 'post?page=' + str(page_no)
            RequestScheduler.request(post_page_url, )
