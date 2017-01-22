"""
Abstract class of all crawlers.

All crawlers should subclass Crawler class here in order to be compatible with
CrawlerManager used by main procedure.
"""

class Crawler:
    """
    Abstract class of all crawler.

    All methods defined here should be implemented by subclasses. It's purely a
    virtual class.
    """
    def __init__(self, **kwargs):
        """
        Constrcutor of class.
        """
        raise NotImplementedError('__init__ of ' + self.__name__ + 'has not '
                                  'been implemented.')

    def run(self, **kwargs):
        """
        Runs crawler.

        Parsed command line will be passed in as keyword arguments. It should
        handle these command properly.
        """
        raise NotImplementedError('run of ' + self.__name__ + 'has not '
                                  'been implemented.')
