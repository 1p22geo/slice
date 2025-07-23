from typing import Callable
import fnmatch
import os


def dirwalk(path: str, callback: Callable[[str, str], None], followlinks=True):
    for root, dirnames, filenames in os.walk(path, followlinks=followlinks):
        for filename in fnmatch.filter(filenames, "*.wav"):
            file = str(os.path.join(root, filename))
            callback(file, filename)
