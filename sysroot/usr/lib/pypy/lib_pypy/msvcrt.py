"""
Python interface to the Microsoft Visual C Runtime
Library, providing access to those non-portable, but
still useful routines.
"""

# XXX incomplete: implemented only functions needed by subprocess.py
# PAC: 2010/08 added MS locking for Whoosh

# 07/2016: rewrote in CFFI

import sys
if sys.platform != 'win32':
    raise ImportError("The 'msvcrt' module is only available on Windows")

import _rawffi
from _pypy_winbase_cffi import ffi as _ffi
_lib = _ffi.dlopen(_rawffi.get_libc().name)

import errno

try: from __pypy__ import builtinify, validate_fd
except ImportError: builtinify = validate_fd = lambda f: f


def _ioerr():
    e = _ffi.errno
    raise IOError(e, errno.errorcode[e])


@builtinify
def open_osfhandle(fd, flags):
    """"open_osfhandle(handle, flags) -> file descriptor

    Create a C runtime file descriptor from the file handle handle. The
    flags parameter should be a bitwise OR of os.O_APPEND, os.O_RDONLY,
    and os.O_TEXT. The returned file descriptor may be used as a parameter
    to os.fdopen() to create a file object."""
    fd = _lib._open_osfhandle(fd, flags)
    if fd == -1:
        _ioerr()
    return fd

@builtinify
def get_osfhandle(fd):
    """"get_osfhandle(fd) -> file handle

    Return the file handle for the file descriptor fd. Raises IOError if
    fd is not recognized."""
    try:
        validate_fd(fd)
    except OSError as e:
        raise IOError(*e.args)
    result = _lib._get_osfhandle(fd)
    if result == -1:
        _ioerr()
    return result

@builtinify
def setmode(fd, flags):
    """setmode(fd, mode) -> Previous mode

    Set the line-end translation mode for the file descriptor fd. To set
    it to text mode, flags should be os.O_TEXT; for binary, it should be
    os.O_BINARY."""
    flags = _lib._setmode(fd, flags)
    if flags == -1:
        _ioerr()
    return flags

LK_UNLCK, LK_LOCK, LK_NBLCK, LK_RLCK, LK_NBRLCK = range(5)

@builtinify
def locking(fd, mode, nbytes):
    """"locking(fd, mode, nbytes) -> None

    Lock part of a file based on file descriptor fd from the C runtime.
    Raises IOError on failure. The locked region of the file extends from
    the current file position for nbytes bytes, and may continue beyond
    the end of the file. mode must be one of the LK_* constants listed
    below. Multiple regions in a file may be locked at the same time, but
    may not overlap. Adjacent regions are not merged; they must be unlocked
    individually."""
    rv = _lib._locking(fd, mode, nbytes)
    if rv != 0:
        _ioerr()

# Console I/O routines

kbhit = _lib._kbhit

@builtinify
def getch():
    return chr(_lib._getch())

@builtinify
def getwch():
    return unichr(_lib._getwch())

@builtinify
def getche():
    return chr(_lib._getche())

@builtinify
def getwche():
    return unichr(_lib._getwche())

@builtinify
def putch(ch):
    _lib._putch(ord(ch))

@builtinify
def putwch(ch):
    _lib._putwch(ord(ch))

@builtinify
def ungetch(ch):
    if _lib._ungetch(ord(ch)) == -1:   # EOF
        _ioerr()

@builtinify
def ungetwch(ch):
    if _lib._ungetwch(ord(ch)) == -1:   # EOF
        _ioerr()
