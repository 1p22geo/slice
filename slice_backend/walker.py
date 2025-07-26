from typing import Callable
import fnmatch
import os


def countfiles(path: str, followlinks=True):
    count = 0
    for root, dirnames, filenames in os.walk(path, followlinks=followlinks):
        for filename in fnmatch.filter(filenames, "*.wav"):
            count += 1
    return count


def dirwalk(path: str, callback: Callable[[str, str], None], followlinks=True):
    for root, dirnames, filenames in os.walk(path, followlinks=followlinks):
        for filename in fnmatch.filter(filenames, "*.wav"):
            file = str(os.path.join(root, filename))
            callback(file, filename)
