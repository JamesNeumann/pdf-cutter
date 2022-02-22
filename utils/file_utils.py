import os
from time import sleep


def is_file_locked(file_path):
    """
    Checks to see if a file is locked. Performs three checks
        1. Checks if the file even exists
        2. Attempts to open the file for reading. This will determine if the file has a write lock.
            Write locks occur when the file is being edited or copied to, e.g. a file copy destination
        3. Attempts to rename the file. If this fails the file is open by some other process for reading. The
            file can be read, but not written to or deleted.
    """
    if not (os.path.exists(file_path)):
        return False
    try:
        f = open(file_path, 'r')
        f.close()
    except IOError:
        return True

    lock_file = file_path + ".lckchk"
    if os.path.exists(lock_file):
        os.remove(lock_file)
    try:
        os.rename(file_path, lock_file)
        sleep(1)
        os.rename(lock_file, file_path)
        return False
    except WindowsError:
        return True


def wait_until_file_is_unlocked(file_path):
    while is_file_locked(file_path):
        pass
