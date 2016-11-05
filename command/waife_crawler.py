"""
Command for
waife-crawler
waife-crawler --page-limit <number>
waife-crawler --score-threshold <number>
"""
from request.scheduler import RequestScheduler
from crawler.parser import parse_query_page, parse_detail_page


def decision_function_factory(score_threshold=60):
    """
    """
    def decision_func(score):
        return score >= 60

    return decision_func


def run(page_limit=10, score_threshold=None):
    """
    """
    base_url = 'http://konachan.net'
    decision_func = decision_function_factory(score_threshold)
    RequestScheduler.initialize()

    def download_handler(response, pid, ptype):
        """
        """
        file_path = str(pid) + '.' + ptype
        print('Writing to' + file_path)
        picture = open(file_path, mode='wb')
        picture.write(response.content)
        picture.close()
        print('Picture', pid, 'has been saved at', file_path)

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
        to_download = parse_query_page(response.text, base_url, decision_func)
        for picture_url in to_download:
            print('Request to ', picture_url, 'is scheduled.')
            RequestScheduler.request(picture_url, detail_page_handler)

    for i in range(0, page_limit - 1):
        RequestScheduler.request(base_url + '/post', params={
            'page': i
        }, response_handler=query_page_handler)

    while RequestScheduler.is_working():
        pass

    print('Waife-crawler finished.')
