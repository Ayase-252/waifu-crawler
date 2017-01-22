"""
Utility functions to parse web page on konachan.com
"""
import re

from bs4 import BeautifulSoup

def parse_query_page_new(text):
    """
    Parses query page.

    It will parse all pictures on the page, and return their info in a dict. It
    is a alternative method compatible with new design of crawler.
    """
