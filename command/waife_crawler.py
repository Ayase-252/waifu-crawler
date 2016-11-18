"""
Command for
waife-crawler
waife-crawler --page-limit <number>
waife-crawler --score-threshold <number>
"""
from datetime import date
import os

from request.scheduler import RequestScheduler
from crawler.parser import parse_query_page, parse_detail_page
from file_logger.file_logger import FileLogger
from conf import FILE_DESTINATION

base_url = 'http://konachan.net'
DECISION_FUNCTION = None
file_logger = FileLogger('file.log')


def make_destination_path():
    datestr = date.today().strftime('%Y-%m-%d')
    return FILE_DESTINATION + datestr


class DecisionFunctionFactory:
    """
    """

    def __init__(self, score_threshold):
        self.score_threshold = score_threshold

    def __call__(self, score):
        return score >= self.score_threshold


def download_handler(response, pid, ptype):
    """
    """
    if file_logger.is_in(pid):
        print('Picture', pid, 'has been downloaded.')
    else:
        file_path = make_destination_path() + '/'
        file_name = str(pid) + '.' + ptype
        file_full_path = file_path + file_name
        print('Writing to', file_full_path)
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        picture = open(file_full_path, mode='wb')
        picture.write(response.content)
        picture.close()
        file_logger.add(pid)
        print('Picture', pid, 'has been saved at', file_full_path)


def detail_page_handler(response):
    """
    """
    print('Parsing detail page:', response.url)
    download = parse_detail_page(response.text)
    print('Download of picture No.', download['pid'], 'is scheduled.')
    RequestScheduler.request(download['url'], download_handler,
                             handler_kwargs={
                                 'pid': download['pid'],
                                 'ptype': download['ptype']
    })


def query_page_handler(response):
    """
    """
    print('Parsing query page:', response.url)
    to_download = parse_query_page(response.text, base_url, DECISION_FUNCTION)
    for picture_url in to_download:
        print('Request to ', picture_url, 'is scheduled.')
        RequestScheduler.request(picture_url, detail_page_handler)


def run(page_limit=10, score_threshold=100):
    """
    """
    global DECISION_FUNCTION
    DECISION_FUNCTION = DecisionFunctionFactory(score_threshold)
    RequestScheduler.initialize(request_interval=2000)

    for i in range(1, page_limit + 1):
        RequestScheduler.request(base_url + '/post', params={
            'page': i
        }, response_handler=query_page_handler)

    while RequestScheduler.is_working():
        pass
    print('Waife-crawler finished.')
