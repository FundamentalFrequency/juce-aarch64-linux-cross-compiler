# pylint: disable=E0601,W0622,W0611
# copyright 2003-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""Wrappers around some builtins introduced in python 2.3, 2.4 and
2.5, making them available in for earlier versions of python.

See another compatibility snippets from other projects:

    :mod:`lib2to3.fixes`
    :mod:`coverage.backward`
    :mod:`unittest2.compatibility`
"""


__docformat__ = "restructuredtext en"

import sys
import types
from typing import Union

# not used here, but imported to preserve API
import builtins  # noqa


def str_to_bytes(string):
    return str.encode(string)


# we have to ignore the encoding in py3k to be able to write a string into a
# TextIOWrapper or like object (which expect an unicode string)
def str_encode(string: Union[int, str], encoding: str) -> str:
    return str(string)


# See also http://bugs.python.org/issue11776
if sys.version_info[0] == 3:

    def method_type(callable, instance, klass):
        # api change. klass is no more considered
        return types.MethodType(callable, instance)


else:
    # alias types otherwise
    method_type = types.MethodType

# Pythons 2 and 3 differ on where to get StringIO
if sys.version_info < (3, 0):
    from cStringIO import StringIO

    FileIO = file  # noqa
    BytesIO = StringIO
    reload = reload  # noqa
else:
    from io import StringIO, FileIO  # noqa
    from imp import reload  # noqa

from logilab.common.deprecation import callable_deprecated  # noqa

# Other projects import these from here, keep providing them for
# backwards compat
any = callable_deprecated('use builtin "any"')(any)
all = callable_deprecated('use builtin "all"')(all)
