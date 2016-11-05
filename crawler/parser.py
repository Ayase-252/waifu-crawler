"""
Parser
"""
import re

from bs4 import BeautifulSoup


def parse_query_page(page_html, base_url, decision_func):
    """
    Parse query page, return url of detail page of picture which is determined
    to download by decision function
    """
    parsed_html = BeautifulSoup(page_html, 'html5lib')
    pictures = parsed_html.find(id='post-list-posts').find_all('li')
    to_downloaded_detail_page_urls = []
    for picture in pictures:
        regx = re.compile(r'Score: (?P<score>\d+)')
        img_alt = picture.find('img')['alt']
        score = int(regx.search(img_alt).group('score'))
        if decision_func(score=score):
            to_downloaded_detail_page_urls.append(base_url +
                                                  picture.find('a', class_='thumb')['href'])

    return to_downloaded_detail_page_urls

def parse_detail_page(page_html):
    """
    """
    parsed_html = BeautifulSoup(page_html, 'html5lib')

    stats = parsed_html.find(id='stats')
    id_regx = re.compile(r'Id: (?P<id>\d+)')
    picture_id_str = stats.find(text=id_regx)
    picture_id = int(id_regx.match(picture_id_str).group('id'))

    png_regx = re.compile(r'Download PNG')
    png_anchor = parsed_html.find('a', text=png_regx)
    #TODO: This code snappet works but is extremely ugly.
    if png_anchor is not None:
        return {
            'pid': picture_id,
            'url': png_anchor['href'],
            'ptype': 'png'
        }
    else:
        jpg_regx = re.compile(r'Download larger version')
        jpg_anchor = parsed_html.find('a', text=jpg_regx)
        if jpg_anchor is not None:
            return {
                'pid': picture_id,
                'url': jpg_anchor['href'],
                'ptype': 'jpg'
            }
        else:
            jpg_v1_regx = re.compile(r'View larger version')
            jpg_v1_anchor = parsed_html.find('a', text=jpg_v1_regx)
            return {
                'pid': picture_id,
                'url': jpg_v1_anchor['href'],
                'ptype': 'jpg'
            }
