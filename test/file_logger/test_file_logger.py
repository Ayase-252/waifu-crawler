#pylint: skip-file

from unittest import TestCase
import os

from file_logger.file_logger import FileLogger

class FileLoggerTest(TestCase):
    def setUp(self):
        self.file_logger = FileLogger('test_file.log')

    def tearDown(self):
        self.file_logger.finalize()
        if os.path.isfile('test_file.log'):
            os.remove('test_file.log')

    def test_file_log(self):
        self.file_logger.add('12345')
        self.file_logger.add('12453')
        self.assertTrue(self.file_logger.is_in('12345'))
        self.assertTrue(self.file_logger.is_in('12453'))
        self.assertFalse(self.file_logger.is_in('9999'))
