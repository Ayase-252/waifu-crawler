"""
Configuration Reader
"""
import conf


class Configuration:
    """
    Configuration of waife crawler
    """

    @classmethod
    def get_file_destination(cls):
        return conf.FILE_DESTINATION
