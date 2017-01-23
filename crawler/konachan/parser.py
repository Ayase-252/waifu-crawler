"""
Utility functions to parse web page on konachan.com
"""
import re

from bs4 import BeautifulSoup

def parse_query_page(text):
    """
    Parses query page.

    It will parse all pictures on the page, and return their info in a dict. It
    is a alternative method compatible with new design of crawler.
    """
    parsed_text = BeautifulSoup(text, 'html5lib')
    posts = parsed_text.find(id='post-list-posts').find_all('li')
    parsed_posts = []
    for post in posts:
        parsed_post = {}

        # Parse ID and detail url
        detail_url = post.find(class_='plid').text[4:]  # Remove (#pl )
        id_parttern = re.compile(r'http://konachan.net/post/show/(?P<id>\d+)')
        id_ = id_parttern.search(detail_url).group('id')
        parsed_post['link'] = detail_url
        parsed_post['id'] = int(id_)

        # Parse score, tags and rating
        title_parttern = re.compile(
            r'Rating: (?P<rating>\w+) Score: (?P<score>\d+) '
            'Tags: (?P<tags>[a-zA-z0-9_ ]+) User:'
        )
        title = post.find('a', class_='thumb').find('img')['title']
        matched_text = title_parttern.search(title)
        parsed_post['score'] = int(matched_text.group('score'))
        parsed_post['rating'] = matched_text.group('rating')
        parsed_post['tags'] = [
            tag.replace('_', ' ')
            for tag in matched_text.group('tags').split(' ')
        ]
        parsed_posts.append(parsed_post)

    return parsed_posts


def parse_detail_page(detail_page_text):
    """
    Parses detail page of picture.


    """
    parsed_text = BeautifulSoup(detail_page_text, 'html5lib')
    download_links = []

    # Try to find png link
    png_parttern = re.compile(r'Download PNG')
    png_anchor = parsed_text.find('a', text=png_parttern)
    if png_anchor is not None:
        download_links.append({
            'type': 'png',
            'link': png_anchor['href']
        })

    # Try to find jpeg link
    jpeg_parttern = re.compile(r'Download larger version')
    jpeg_anchor = parsed_text.find('a', text=jpeg_parttern)
    if jpeg_anchor is not None:
        download_links.append({
            'type': 'jpeg',
            'link': jpeg_anchor['href']
        })

    return download_links
