"""
Progress bar
"""
import sys


class ProgressBar:
    def __init__(self, total_size):
        self.progress = 0
        self.total_size = total_size

    def set_progress(self, progress):
        self.progress = progress
        self._update()

    def _update(self):
        progress_blocks = self.progress // 4
        blank_blocks = 25 - progress_blocks
        sys.stdout.write('\r')
        sys.stdout.write(
            '[' + '=' * progress_blocks + ' ' * blank_blocks + ']'
            + ' {}%  Total Size: {}Byte'.format(self.progress, self.total_size)
        )
        sys.stdout.flush()
