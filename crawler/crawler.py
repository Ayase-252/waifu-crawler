"""
Abstract class of all crawlers.

All crawlers should subclass Crawler class here in order to be compatible with
CrawlerManager used by main procedure.
"""

from abc import ABCMeta, abstractmethod


class Crawler(metaclass=ABCMeta):
    """
    Abstract class of all crawler.

    All methods defined here should be implemented by subclasses. It's purely a
    virtual class.
    """
    @abstractmethod
    def __init__(self, **kwargs):
        """
        Constrcutor of class.
        """
        pass

    @abstractmethod
    def run(self, **kwargs):
        """
        Runs crawler.

        Parsed command line will be passed in as keyword arguments. It should
        handle these command properly.
        """
        pass
