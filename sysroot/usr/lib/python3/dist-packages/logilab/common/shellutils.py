# copyright 2003-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option) any
# later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""shell/term utilities, useful to write some python scripts instead of shell
scripts.
"""

from __future__ import print_function

__docformat__ = "restructuredtext en"

import os
import glob
import shutil
import sys
import tempfile
import fnmatch
import string
import random
import subprocess
import warnings
from os.path import exists, isdir, islink, basename, join
from _io import StringIO
from typing import Any, Callable, Optional, List, Union, Iterator, Tuple

from logilab.common import STD_BLACKLIST, _handle_blacklist
from logilab.common.deprecation import callable_deprecated


class tempdir(object):
    def __enter__(self):
        self.path = tempfile.mkdtemp()
        return self.path

    def __exit__(self, exctype, value, traceback):
        # rmtree in all cases
        shutil.rmtree(self.path)
        return traceback is None


class pushd(object):
    def __init__(self, directory):
        self.directory = directory

    def __enter__(self):
        self.cwd = os.getcwd()
        os.chdir(self.directory)
        return self.directory

    def __exit__(self, exctype, value, traceback):
        os.chdir(self.cwd)


def chown(path, login=None, group=None):
    """Same as `os.chown` function but accepting user login or group name as
    argument. If login or group is omitted, it's left unchanged.

    Note: you must own the file to chown it (or be root). Otherwise OSError is raised.
    """
    if login is None:
        uid = -1
    else:
        try:
            uid = int(login)
        except ValueError:
            import pwd  # Platforms: Unix

            uid = pwd.getpwnam(login).pw_uid
    if group is None:
        gid = -1
    else:
        try:
            gid = int(group)
        except ValueError:
            import grp

            gid = grp.getgrnam(group).gr_gid
    os.chown(path, uid, gid)


def mv(source, destination, _action=shutil.move):
    """A shell-like mv, supporting wildcards."""
    sources = glob.glob(source)
    if len(sources) > 1:
        assert isdir(destination)
        for filename in sources:
            _action(filename, join(destination, basename(filename)))
    else:
        try:
            source = sources[0]
        except IndexError:
            raise OSError("No file matching %s" % source)
        if isdir(destination) and exists(destination):
            destination = join(destination, basename(source))
        try:
            _action(source, destination)
        except OSError as ex:
            raise OSError("Unable to move %r to %r (%s)" % (source, destination, ex))


def rm(*files):
    """A shell-like rm, supporting wildcards."""
    for wfile in files:
        for filename in glob.glob(wfile):
            if islink(filename):
                os.remove(filename)
            elif isdir(filename):
                shutil.rmtree(filename)
            else:
                os.remove(filename)


def cp(source, destination):
    """A shell-like cp, supporting wildcards."""
    mv(source, destination, _action=shutil.copy)


def find(
    directory: str,
    exts: Union[Tuple[str, ...], str],
    exclude: bool = False,
    blacklist: Tuple[str, ...] = STD_BLACKLIST,
) -> List[str]:
    """Recursively find files ending with the given extensions from the directory.

    :type directory: str
    :param directory:
      directory where the search should start

    :type exts: basestring or list or tuple
    :param exts:
      extensions or lists or extensions to search

    :type exclude: boolean
    :param exts:
      if this argument is True, returning files NOT ending with the given
      extensions

    :type blacklist: list or tuple
    :param blacklist:
      optional list of files or directory to ignore, default to the value of
      `logilab.common.STD_BLACKLIST`

    :rtype: list
    :return:
      the list of all matching files
    """
    if isinstance(exts, str):
        exts = (exts,)
    if exclude:

        def match(filename: str, exts: Tuple[str, ...]) -> bool:
            for ext in exts:
                if filename.endswith(ext):
                    return False
            return True

    else:

        def match(filename: str, exts: Tuple[str, ...]) -> bool:
            for ext in exts:
                if filename.endswith(ext):
                    return True
            return False

    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        _handle_blacklist(blacklist, dirnames, filenames)
        # don't append files if the directory is blacklisted
        dirname = basename(dirpath)
        if dirname in blacklist:
            continue
        files.extend([join(dirpath, f) for f in filenames if match(f, exts)])
    return files


def globfind(
    directory: str,
    pattern: str,
    blacklist: Tuple[str, str, str, str, str, str, str, str] = STD_BLACKLIST,
) -> Iterator[str]:
    """Recursively finds files matching glob `pattern` under `directory`.

    This is an alternative to `logilab.common.shellutils.find`.

    :type directory: str
    :param directory:
      directory where the search should start

    :type pattern: basestring
    :param pattern:
      the glob pattern (e.g *.py, foo*.py, etc.)

    :type blacklist: list or tuple
    :param blacklist:
      optional list of files or directory to ignore, default to the value of
      `logilab.common.STD_BLACKLIST`

    :rtype: iterator
    :return:
      iterator over the list of all matching files
    """
    for curdir, dirnames, filenames in os.walk(directory):
        _handle_blacklist(blacklist, dirnames, filenames)
        for fname in fnmatch.filter(filenames, pattern):
            yield join(curdir, fname)


def unzip(archive, destdir):
    import zipfile

    if not exists(destdir):
        os.mkdir(destdir)
    zfobj = zipfile.ZipFile(archive)
    for name in zfobj.namelist():
        if name.endswith("/"):
            os.mkdir(join(destdir, name))
        else:
            outfile = open(join(destdir, name), "wb")
            outfile.write(zfobj.read(name))
            outfile.close()


@callable_deprecated("Use subprocess.Popen instead")
class Execute:
    """This is a deadlock safe version of popen2 (no stdin), that returns
    an object with errorlevel, out and err.
    """

    def __init__(self, command):
        cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.out, self.err = cmd.communicate()
        self.status = os.WEXITSTATUS(cmd.returncode)


class ProgressBar(object):
    """A simple text progression bar."""

    def __init__(
        self, nbops: int, size: int = 20, stream: StringIO = sys.stdout, title: str = ""
    ) -> None:
        if title:
            self._fstr = "\r%s [%%-%ss]" % (title, int(size))
        else:
            self._fstr = "\r[%%-%ss]" % int(size)
        self._stream = stream
        self._total = nbops
        self._size = size
        self._current = 0
        self._progress = 0
        self._current_text = None
        self._last_text_write_size = 0

    def _get_text(self):
        return self._current_text

    def _set_text(self, text=None):
        if text != self._current_text:
            self._current_text = text
            self.refresh()

    def _del_text(self):
        self.text = None

    text = property(_get_text, _set_text, _del_text)

    def update(self, offset: int = 1, exact: bool = False) -> None:
        """Move FORWARD to new cursor position (cursor will never go backward).

        :offset: fraction of ``size``

        :exact:

          - False: offset relative to current cursor position if True
          - True: offset as an asbsolute position

        """
        if exact:
            self._current = offset
        else:
            self._current += offset

        progress = int((float(self._current) / float(self._total)) * self._size)
        if progress > self._progress:
            self._progress = progress
            self.refresh()

    def refresh(self) -> None:
        """Refresh the progression bar display."""
        self._stream.write(self._fstr % ("=" * min(self._progress, self._size)))
        if self._last_text_write_size or self._current_text:
            template = " %%-%is" % (self._last_text_write_size)
            text = self._current_text
            if text is None:
                text = ""
            self._stream.write(template % text)
            self._last_text_write_size = len(text.rstrip())
        self._stream.flush()

    def finish(self):
        self._stream.write("\n")
        self._stream.flush()


class DummyProgressBar(object):
    __slots__ = ("text",)

    def refresh(self):
        pass

    def update(self):
        pass

    def finish(self):
        pass


_MARKER = object()


class progress(object):
    def __init__(self, nbops=_MARKER, size=_MARKER, stream=_MARKER, title=_MARKER, enabled=True):
        self.nbops = nbops
        self.size = size
        self.stream = stream
        self.title = title
        self.enabled = enabled

    def __enter__(self):
        if self.enabled:
            kwargs = {}
            for attr in ("nbops", "size", "stream", "title"):
                value = getattr(self, attr)
                if value is not _MARKER:
                    kwargs[attr] = value
            self.pb = ProgressBar(**kwargs)
        else:
            self.pb = DummyProgressBar()
        return self.pb

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pb.finish()


class RawInput(object):
    def __init__(
        self,
        input_function: Optional[Callable] = None,
        printer: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:
        if "input" in kwargs:
            input_function = kwargs.pop("input")
            warnings.warn(
                "'input' argument is deprecated," "use 'input_function' instead",
                DeprecationWarning,
            )
        self._input = input_function or input
        self._print = printer

    def ask(self, question: str, options: Tuple[str, ...], default: str) -> str:
        assert default in options
        choices = []
        for option in options:
            if option == default:
                label = option[0].upper()
            else:
                label = option[0].lower()
            if len(option) > 1:
                label += "(%s)" % option[1:].lower()
            choices.append((option, label))
        prompt = "%s [%s]: " % (question, "/".join([opt[1] for opt in choices]))
        tries = 3
        while tries > 0:
            answer = self._input(prompt).strip().lower()
            if not answer:
                return default
            possible = [option for option, label in choices if option.lower().startswith(answer)]
            if len(possible) == 1:
                return possible[0]
            elif len(possible) == 0:
                msg = "%s is not an option." % answer
            else:
                msg = "%s is an ambiguous answer, do you mean %s ?" % (
                    answer,
                    " or ".join(possible),
                )
            if self._print:
                self._print(msg)
            else:
                print(msg)
            tries -= 1
        raise Exception("unable to get a sensible answer")

    def confirm(self, question: str, default_is_yes: bool = True) -> bool:
        default = default_is_yes and "y" or "n"
        answer = self.ask(question, ("y", "n"), default)
        return answer == "y"


ASK = RawInput()


def getlogin():
    """avoid using os.getlogin() because of strange tty / stdin problems
    (man 3 getlogin)
    Another solution would be to use $LOGNAME, $USER or $USERNAME
    """
    if sys.platform != "win32":
        import pwd  # Platforms: Unix

        return pwd.getpwuid(os.getuid())[0]
    else:
        return os.environ["USERNAME"]


def generate_password(length=8, vocab=string.ascii_letters + string.digits):
    """dumb password generation function"""
    pwd = ""
    for i in range(length):
        pwd += random.choice(vocab)
    return pwd
