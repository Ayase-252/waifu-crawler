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
