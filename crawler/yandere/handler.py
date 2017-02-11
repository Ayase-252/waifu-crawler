"""
Konachan Cralwer Handlers

This module contains handlers to process pages.
"""

from crawler.konachan.parser import parse_query_page

class PostPageHandler:
    """
    Handlers for post page
    """
    def __init__(self, selector):
        """
        Initial function

        selector    Selector object to pick up pictures from the whole.
        """
        self._selector = selector

    def __call__(self, result_html):
        """
        Real procedure to deal with post page

        params:
        result_html     HTML text of post page
        """
        candidates = parse_query_page(result_html)
        qualified_pictures = selector.select(candidates)

        for qualified_picture in qualified_pictures:
            RequestScheduler.request(qualified_picture['link'], )
