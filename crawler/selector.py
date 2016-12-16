"""
Selector

Selector decides whether a picture should be download.
"""
import copy


class Selector:
    """
    Selector middleware implements a queue of selector functions. Candidates
    go through a series of functions and are flitered.
    """

    def __init__(self):
        self._selector_queue = []
        self._decisive_selector_queue = []

    def add_normal_selector(self, selector_function):
        """
        Add selector into queue. The selector who first is added will be the
        first to take effective.
        """
        self._selector_queue.append(selector_function)

    def select(self, candidates):
        """
        Select eligible picture from candidates.
        """
        candidates_copy = copy.deepcopy(candidates)
        eligible_pictures = []
        for decisive_selector in self._decisive_selector_queue:
            for candidate in candidates_copy:
                if decisive_selector(candidate):
                    eligible_pictures.append(candidate)
                    candidates_copy.remove(candidate)

        for selector in self._selector_queue:
            for candidate in candidates_copy:
                if not selector(candidate):
                    candidates_copy.remove(candidate)
        return candidates_copy + eligible_pictures

    def add_decisive_selector(self, decisive_selector):
        """
        Add decisive selector into queue.
        Picture passing test of any decisive selector will be selected.
        """
        self._decisive_selector_queue.append(decisive_selector)
