"""
Parser for yande.re
"""
import re

from bs4 import BeautifulSoup


def parse_query_list(text):
    """
    Parse query list document
    """

    parsed_text = BeautifulSoup(text, 'html5lib')
    posts = parsed_text.find(id='post-list-posts').find_all('li')
    parsed_posts = []
    for post in posts:
        parsed_post = {}

        # Parse ID and detail url
        detail_url = post.find(class_='plid').text[4:]  # Remove (#pl )
        id_parttern = re.compile(r'https://yande.re/post/show/(?P<id>\d+)')
        id_ = id_parttern.search(detail_url).group('id')
        parsed_post['detail url'] = detail_url
        parsed_post['id'] = int(id_)

        # Parse score, tags and rating
        title = post.find('a', class_='thumb').find('img')['title']
        parsed_title_meta = parse_title(title)
        parsed_post.update(parsed_title_meta)
        parsed_posts.append(parsed_post)

    return parsed_posts


def parse_detail_page(detail_page_text):
    """
    Parse detail page of picture.

    returns:
    Download links of picture
    """
    parsed_text = BeautifulSoup(detail_page_text, 'html5lib')
    download_links = {}

    # Try to find png link
    png_parttern = re.compile(r'Download PNG')
    png_anchor = parsed_text.find('a', text=png_parttern)
    if png_anchor is not None:
        download_links['png'] = png_anchor['href']

    # Try to find jpeg link
    jpeg_parttern = re.compile(r'Download larger version')
    jpeg_anchor = parsed_text.find('a', text=jpeg_parttern)
    if jpeg_anchor is not None:
        download_links['jpeg'] = jpeg_anchor['href']

    jpeg_parttern_2 = re.compile(r'View larger version')
    jpeg_anchor_2 = parsed_text.find('a', text=jpeg_parttern_2)
    if jpeg_anchor_2 is not None:
        download_links['jpeg'] = jpeg_anchor_2['href']

    if download_links == {}:
        raise RuntimeError('Page cannot be parsed: Parsing result is empty.')

    return download_links


def parse_title(title_text):
    """
    Parse title to fetch meta data of picture

    params:
    title_text      Title of picture

    returns:
    metadata of picture
    """
    meta = {}
    title_parttern = re.compile(
        r'Rating: (?P<rating>\w+) Score: (?P<score>\d+) Tags: (?P<tags>.+) User:'
    )
    matched_text = title_parttern.search(title_text)
    if matched_text is not None:
        meta['score'] = int(matched_text.group('score'))
        meta['rating'] = matched_text.group('rating')
        meta['tags'] = [
            tag.replace('_', ' ')
            for tag in matched_text.group('tags').split(' ')
        ]
    else:
        raise RuntimeError('Title cannot be parsed! \nFailed title: ' +
                           title_text)
    return meta
