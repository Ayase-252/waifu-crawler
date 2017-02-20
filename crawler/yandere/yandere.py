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
        self.request_scheduler = AsyncRequestScheduler(2000)

    # TODO: refactor
    def run(self, **kwargs):
        """
        Runs the crawler
        """
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
                text = self.request_scheduler.get(base_url, params={
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
            id_ = qualified_picture['id']
            url = qualified_picture['detail url']
            try:
                if not file_logger.is_in(id_):
                    print('Requesting to page {}'.format(url))
                    text = self.request_scheduler.get(url).text
                    links = self._parse_detail_page(text, url)
                    print('Downloading picture {0}'.format(id_))
                    self._download(links, id_)
                    print('\nDownloaded.')
                    file_logger.add(id_)

            except ConnectTimeout:
                print('Connection timed out. '
                      'Please retry in stable network environmnent.')

    def _download(self, parsed_links, id_):
        """
        Download picture based on parsed_links
        """
        type_codes = ['png', 'jpg']
        type_suffix = {
            'png': '.png',
            'jpeg': '.jpg'
        }
        for type_ in type_codes:
            if type_ in parsed_links:
                self.request_scheduler.download(
                    parsed_links[type_],
                    'yandere-' + str(id_) + type_suffix[type_]
                )
                break

    def _parse_detail_page(self, text, url):
        """
        Wrapper of process to parsing detail page
        """
        try:

            links = parse_detail_page(text)
            return links
        except RuntimeError as e:
            print('=' * 25)
            print('Parsing Error: Please report an issue in '
                  'https://github.com/Ayase-252/waife-crawler/issues with '
                  'following message.')
            print('URL: {}'.format(url))
            print('=' * 25)
            raise RuntimeError('Parse Error: {}'.format(url))
