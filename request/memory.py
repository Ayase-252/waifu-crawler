"""
Request Memory

This module contains a class to manage all about requests such as request detail,
probably response.
"""
from threading import Lock


class RequestMemory:
    """
    Request Memory
    """

    def __init__(self):
        """
        Constructor
        """
        self.next_memory_id = 0
        self.request_memory = []
        self.memory_lock = Lock()

    def _acquire_memory_lock(self):
        """
        Acquires the memory lock
        """
        self.memory_lock.acquire()

    def _release_memory_lock(self):
        """
        Releases the memory lock
        """
        self.memory_lock.release()

    def create(self, initial_dic=None):
        """
        Create an empty slot in memory

        params:
        initial_dic         Initial data except id

        returns:
        ID donating the new allocated slot in memory
        """
        self._acquire_memory_lock()
        new_memory_id = self.next_memory_id
        empty_slot = {
            'id': new_memory_id,
        }
        if initial_dic is not None:
            empty_slot.update(initial_dic)
        self.next_memory_id += 1
        self.request_memory.append(empty_slot)
        self._release_memory_lock()
        return new_memory_id

    def update(self, memory_id, update_dic):
        """
        Update a memory

        params:
        memory_id
        update_dic              Dict contains fields to update
        """
        self._acquire_memory_lock()
        index = self._get_memory_index(memory_id)
        self.request_memory[index].update(update_dic)
        self._release_memory_lock()

    def retrieve(self, memory_id):
        """
        Retrieve memory donated by memory_id

        paramas:
        memory_id

        returns:
        Dict donated by memory_id
        """
        memory = None
        self._acquire_memory_lock()
        index = self._get_memory_index(memory_id)
        memory = self.request_memory[index]
        self._release_memory_lock()
        return memory


    def _get_memory_index(self, request_id):
        """
        Query result by request id

        result:
        Subindex of result if found, otherwise -1
        """
        index = -1
        for result_tuple in enumerate(self.request_memory):
            if result_tuple[1]['id'] == request_id:
                index = result_tuple[0]
        return index
