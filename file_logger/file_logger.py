"""
File logger

This module manage a logger to maintain these lists of downloaded files.

"""

import os


def file_handler(function):
    """
    Wrapper of function that need to write or read something in file.

    Use as a decorator.
    """

    def function_wrapper(self, *args):
        self.log_file = open(self.log_path, 'a+')
        function(self, *args)
        self.log_file.close()
    return function_wrapper


class FileLogger:
    """
    File logger
    """

    def __init__(self, log_path):
        self.log_path = log_path
        if os.path.isfile(log_path):
            self.log_file = open(log_path, 'r')
            files = self.log_file.read()
            if files != '':
                self.log_memory = [int(file_id)
                                   for file_id in files.split('\n')
                                   if file_id != '']
            else:
                self.log_memory = []
            self.log_file.close()
        else:
            self.log_memory = []

    @file_handler
    def add(self, file_id):
        """
        Add ID of file into logger.
        """
        self.log_memory.append(file_id)
        self.log_file.write(str(file_id) + '\n')
        self.log_file.flush()

    def is_in(self, file_id):
        """
        Test whether given file_id is in the logger.
        """
        return file_id in self.log_memory
