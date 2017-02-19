"""
Konachan Cralwer Handlers

This module contains handlers to process pages.
"""

from crawler.yandere.parser import parse_query_list


class QueryPageHandler:
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
        candidates = parse_query_list(result_html)
        return self._selector.select(candidates)
