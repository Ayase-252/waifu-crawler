"""
Yandere Crawler
"""
from requests import ConnectTimeout, get

from file_logger.file_logger import FileLogger
from crawler.crawler import Crawler
from crawler.selector import Selector
from request.request_async import AsyncRequestScheduler
from crawler.yandere.handler import QueryPageHandler
from crawler.yandere.parser import parse_detail_page
from crawler.yandere.selector import safe_selector, score_selector_factory


class YandereCrawler(Crawler):
    """
    Yandere Crawler

    Configuration can be done by passing object carrying configuration to
    constructor.
    """

    def __init__(self, **kwargs):
        """
        Acceptable parameters:
        page_limit          The max amount of pages being crawled
        """
        if 'page_limit' in kwargs:
            self._page_limit = kwargs['page_limit']
        else:
            self._page_limit = 10
        if 'score_filter' in kwargs:
            self._score_filter = kwargs['score_filter']
        else:
            self._score_filter = 70

    # TODO: refactor
    def run(self, **kwargs):
        """
        Runs the crawler
        """
        request_scheduler = AsyncRequestScheduler(2000)
        base_url = r'https://yande.re/post'
        qualified_pictures = []

        file_logger = FileLogger('yandere.log')

        # Prepare Selector
        selector = Selector()
        selector.add_normal_selector(safe_selector)
        selector.add_normal_selector(
            score_selector_factory(self._score_filter)
        )
        query_page_handler = QueryPageHandler(selector)

        # Parse Query Page
        for page_no in range(1, self._page_limit + 1):
            try:
                print('Requesting to page ' + str(page_no))
                text = request_scheduler.get(base_url, params={
                    'page': page_no
                }).text
                new_qualified = query_page_handler(text)
                print(str(len(new_qualified)) + ' pictures are added to '
                      'pending queue.')
                qualified_pictures += new_qualified
            except ConnectTimeout:
                print('Connection to page ' + str(page_no) + ' timed out. '
                      'Please retry in stable network environmnent.')

        # Parse download link and download it
        for qualified_picture in qualified_pictures:
            try:
                if not file_logger.is_in(qualified_picture['id']):
                    print('Requesting to page ' + qualified_picture['detail url'])
                    text = request_scheduler.get(
                        qualified_picture['detail url']).text
                    links = parse_detail_page(text)['download links']
                    png_link = list(filter(lambda elem: elem[
                                      'type'] == 'png', links))
                    if len(png_link) == 1:
                        print('Downloading picture {0}. Type {1}'.format(
                            qualified_picture['id'], 'png'
                        ))
                        request_scheduler.download(
                            png_link[0]['link'],
                            'yandere-' + str(qualified_picture['id']) + '.png'
                        )
                        file_logger.add(qualified_picture['id'])

                    else:
                        print('Downloading picture {0}. Type {1}'.format(
                            qualified_picture['id'], 'jpg'
                        ))
                        request_scheduler.download(
                            link[0]['link'],
                            'yandere-' + str(qualified_picture['id']) + '.jpg'
                        )
                        content = get(links[0]['link']).content
                        file_logger.add(qualified_picture['id'])
            except ConnectTimeout:
                print('Connection timed out. '
                      'Please retry in stable network environmnent.')
