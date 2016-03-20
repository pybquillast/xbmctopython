'''
Created on 9/05/2014

@author: pybquillast

This module has been ported from xbmcstubs:

__author__ = 'Team XBMC <http://xbmc.org>'
__credits__ = 'Team XBMC'


'''
"""
xbmcvfs Namespace Reference
Classes and functions to work with files and folders.

Classes
class      File
class      Stat

Functions
def     copy
def     delete
def     rename
def     mkdir
def     mkdirs
def     rmdir
def     exists
def     listdir
"""

import os
import shutil

#
# Detailed Description
#
# Classes and functions to work with files and folders.
#
#
# Function Documentation
#

def copy(source, destination):
    """
    Copy file to destination, returns true/false.

    source: string - file to copy.
    destination: string - destination file

    Example:
        success = xbmcvfs.copy(source, destination)
    """
    try:
        shutil.copy(source, destination)
        return True
    except:
        return False

def delete(fileName):
    """
    Deletes a file.

    fileName: string - file to delete

    Example:
        xbmcvfs.delete(file)
    """
    try:
        os.remove(fileName)
        return True
    except:
        return False


def exists(path):
    """
    Checks for a file or folder existance, mimics Pythons os.path.exists()

    path: string - file or folder

    Example:
        success = xbmcvfs.exists(path)
    """
    return os.path.exists(path)

def listdir(path):
    """
    listdir(path) -- lists content of a folder.

    path        : folder

    example:
     - dirs, files = xbmcvfs.listdir(path)
    """
    return os.walk(path).next()[1:]

def mkdir(path):
    """
    Create a folder.

    path: folder

    Example:
        success = xbmcfvs.mkdir(path)
    """
    os.mkdir(path)
    return os.path.exists(path)

def mkdirs(path):
    """
    mkdirs(path)--Create folder(s) - it will create all folders in the path.

    path : folder

    example:

    - success = xbmcvfs.mkdirs(path)
    Create folder(s) - it will create all folders in the path.

    path: folder

    Example:
        success = xbmcfvs.mkdirs(path)
    """
    os.makedirs(path)
    return os.path.exists(path)


def rename(fileName, newFileName):
    """
    Renames a file, returns true/false.

    fileName: string - file to rename
    newFileName: string - new filename, including the full path

    Example:
        success = xbmcvfs.rename(file,newFileName)
    """
    try:
        os.rename(fileName, newFileName)
        return True
    except:
        return False

def rmdir(path):
    """
    Remove a folder.

    path: folder

    Example:
        success = xbmcfvs.rmdir(path)
    """
    try:
        os.rmdir(path)
        return True
    except:
        return False

#
# CLASSES
#

class File(object):
    """
    xbmcvfs.File Class Reference

    Public Member Functions
    def     __init__
    def     close
    def     read
    def     readBytes
    def     seek
    def     size
    def     write
    """

# Constructor & Destructor Documentation

    def __init__(self, filename, optype = None):
        """
        'w' - opt open for write
        example:
         f = xbmcvfs.File(file, ['w'])
        """
        self._file = open(filename, *optype)
        pass

#    Member Function Documentation

    def close(self):
        """
        example:
         f = xbmcvfs.File(file)
         f.close()
        """
        self._file.close()
        pass

    def read(self, bytesToRead = None):
        """
        bytes : how many bytes to read [opt]- if not set it will read the whole file
        example:
        f = xbmcvfs.File(file)
        b = f.read()
        f.close()
        """
        return self._file.read(bytesToRead)

    def readBytes(self, numbytes):
        """
        readBytes(numbytes)

        numbytes : how many bytes to read [opt]- if not set it will read the whole file

        returns: bytearray

        example:
        f = xbmcvfs.File(file)
        b = f.read()
        f.close()
        """
        return self._file.read(numbytes)

    def seek(self, offset, whence):
        """
        FilePosition : position in the file
        Whence : where in a file to seek from[0 begining, 1 current , 2 end possition]
        example:
         f = xbmcvfs.File(file)
         result = f.seek(8129, 0)
         f.close()
        """
        return self._file.seek(offset, whence)

    def size(self):
        """
        example:
         f = xbmcvfs.File(file)
         s = f.size()
         f.close()
        """
        return self._file.__sizeof__()
        pass

    def write(self, bufferToWrite):
        """
        buffer : buffer to write to file
        example:
         f = xbmcvfs.File(file, 'w', True)
         result = f.write(buffer)
         f.close()
        """
        return self._file.write(bufferToWrite)
        pass

class Stat(object):
    def __init__(self, path):
        """
        Stat(path) -- get file or file system status.

        path        : file or folder

        example:
        - print xbmcvfs.Stat(path).st_mtime()
    """
        self._stat = os.stat(path)
        pass

#
# Member Function Documentation
#

    def st_atime(self): return self._stat.st_atime
    def st_ctime(self): return self._stat.st_ctime
    def st_gid(self): return self._stat.st_gid
    def st_ino(self): return self._stat.st_ino
    def st_mode(self): return self._stat.st_mode
    def st_mtime(self): return self._stat.st_mtime
    def st_nlink(self): return self._stat.st_nlink
    def st_size(self): return self._stat.st_size
    def st_uid(self): return self._stat.st_uid
