"""
File logger

This module manage a logger to maintain these lists of downloaded files.

"""


class FileLogger:
    """
    File logger
    """
    def __init__(self, log_path):
        self.log_file = open(log_path, 'a+')
        self.log_memory = self.log_file.readlines()

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

    def finalize(self):
        """
        Close the file in file logger. IT MUST BE CALLED WHEN THE OBJECT IS
        GOING TO BE INVALID.
        """
        self.log_file.close()
