#!/usr/bin/python3
import argparse
import sys

from crawler import YandereCrawler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web crawler for pictures of '
                                     'adorable waifes. :)')
    parser.add_argument('-t', '--threshold', type=int, dest='threshold',
                        default=100, help='Score threshold, Picture scoring '
                        'higher than threshold will be downloaded. '
                        '(Default 100)')
    sys_args = parser.parse_args(sys.argv[1:])

    yandere_crawler = YandereCrawler(score_filter=sys_args.threshold)
    yandere_crawler.run()
