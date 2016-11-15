from unittest import TestCase

from thread_manager.thread_manager import ThreadManager


class ThreadManagerTest(TestCase):

    def test_run(self):
        ThreadManager.run(function=lambda x: x + 1, kwargs={'x': 1},
                          success_handler=lambda x: self.assertEqual(x, 2)
                          )

    def test_when_exception_raises(self):
        def raise_error():
            raise ValueError('you wrong')
        ThreadManager.run(
            function=raise_error,
            fail_handler=lambda e: self.assertIsInstance(e, ValueError)
        )

    def test_run_after(self):
        ThreadManager.run_after(1, function=lambda x: x + 1, kwargs={'x': 1},
                                success_handler=lambda x: self.assertEqual(
                                    x, 2)
                                )

    def test_simple_run(self):
        ThreadManager.simple_run(function=lambda x: x + 1, x=1,
                                 callback=lambda result: self.assertEqual(result, 2))

    def test_simple_run_without_argument(self):
        ThreadManager.simple_run(function=lambda: 1,
                                 callback=lambda result: self.assertEqual(result, 1))

    def test__simple_run_after(self):
        ThreadManager.simple_run_after(1, function=lambda x: x + 1, x=1,
                                       callback=lambda x: self.assertEqual(
                                           x, 2)
                                       )
