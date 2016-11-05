"""
Unit tests of Request Memory
"""
import unittest
from threading import Thread, active_count

from request.memory import RequestMemory


class RequestMemoryTest(unittest.TestCase):
    """
    Unit tests of Request Memory
    """

    def test_allocate_new_slots_in_diff_threads(self):
        """
        Allocate some new slots in different threads. id should not be
        duplicated.
        """
        request_memory = RequestMemory()
        Thread(target=request_memory.create).run()
        Thread(target=request_memory.create).run()

        while active_count() != 1:
            pass
        ids = [request['id'] for request in request_memory.request_memory]
        #   No duplicated id
        self.assertEqual(len(ids), len(set(ids)))

    def test_update_memory(self):
        """
        Update a request in memory.
        """
        request_memory = RequestMemory()
        memory_id = request_memory.create({
            'old': 'hello world'
        })
        request_memory.update(memory_id, {
            'old': 'hello another world',
            'new': 'hello world'
        })
        new_memory = request_memory.retrieve(memory_id)

        self.assertEqual(new_memory['old'], 'hello another world')
        self.assertEqual(new_memory['new'], 'hello world')

    # def test_set_request_sent(self):
    #     """
    #     Set request has sent
    #     """
    #     request_memory = RequestMemory()
    #     request_id = request_memory.allocate_empty_slot(
    #         url='', request_time=datetime.now())
    #     request_memory.set_request_sent(request_id)
    #
    #     self.assertTrue(request_memory.is_request_sent(request_id))
    #
    # def test_set_request_broken(self):
    #     """
    #     Set request has broken
    #     """
    #     request_memory = RequestMemory()
    #     request_id = request_memory.allocate_empty_slot(
    #         url='', request_time=datetime.now())
    #     request_memory.set_request_broken(request_id)
    #
    #     self.assertTrue(request_memory.is_request_sent(request_id))
    #     self.assertTrue(request_memory.is_request_broken(request_id))
    #
    # def test_set_request_success(self):
    #     """
    #     Set request has succeeded
    #     """
    #     request_memory = RequestMemory()
    #     request_id = request_memory.allocate_empty_slot(
    #         url='', request_time=datetime.now())
    #     request_memory.set_request_success(request_id)
    #
    #     self.assertTrue(request_memory.is_request_sent(request_id))
    #     self.assertTrue(request_memory.is_request_success(request_id))
