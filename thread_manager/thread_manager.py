"""
Thread manager

This is a FACADE of bulit-in module threading. To ease the debug in multi-thread,
some loggers will be added.
"""
from threading import Thread, Timer

from logger import getLogger


class ThreadManager:
    """
    Thread manager
    """
    logger = getLogger('waife-crawl.ThreadManager')

    @classmethod
    def run(cls, function, kwargs=None, success_handler=None, fail_handler=None):
        """
        Start a thread to run the given function.
        If function is executed without exception, the return value will be passed
        to success_handler.Then Success handler will be executed.
        If exception is raised during function is executing, fail_handler which
        the exception will be passed to, will be executed., if it has.
        """
        Thread(target=cls._run, kwargs={
            'function': function,
            'kwargs': kwargs,
            'success_handler': success_handler,
            'fail_handler': fail_handler
        }).run()

    @classmethod
    def _run(cls, function, kwargs=None, success_handler=None, fail_handler=None):
        """
        Code that the new thread runs.
        """
        cls.logger.debug("Starts executing. Function %s with args %s will be"
                         " called.", function.__name__, kwargs)
        try:
            if kwargs is not None:
                result = function(**kwargs)
            else:
                result = function()
        except Exception as exception:
            cls.logger.error("Fail due to exception %s", exception)
            if fail_handler is not None:
                fail_handler(exception)
            cls.logger.debug('Exits')
            return
        cls.logger.debug('Success')
        if success_handler is not None:
            cls.logger.debug("Handles Success, Function %s with args %s will be"
                             " called.", success_handler.__name__, result)
            success_handler(result)
        cls.logger.debug('Exits')

    @classmethod
    def run_after(cls, sec_to_run, function, kwargs=None, success_handler=None,
                  fail_handler=None):
        """
        Run function after sec_to_run.
        Other arguments is same as those described in run.
        """
        cls.logger.debug("Will start in %fs.", sec_to_run)
        Timer(sec_to_run, cls._run, kwargs={
            'function': function,
            'kwargs': kwargs,
            'success_handler': success_handler,
            'fail_handler': fail_handler
        }).start()
