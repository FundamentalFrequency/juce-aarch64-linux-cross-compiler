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
"""A generic visitor abstract implementation.




"""
from typing import Any, Callable, Optional, Union
from logilab.common.types import Node, HTMLWriter, TextWriter

__docformat__ = "restructuredtext en"


def no_filter(_: Node) -> int:
    return 1


# Iterators ###################################################################
class FilteredIterator(object):
    def __init__(self, node: Node, list_func: Callable, filter_func: Optional[Any] = None) -> None:
        self._next = [(node, 0)]
        if filter_func is None:
            filter_func = no_filter
        self._list = list_func(node, filter_func)

    def __next__(self) -> Optional[Node]:
        try:
            return self._list.pop(0)
        except Exception:
            return None

    next = __next__


# Base Visitor ################################################################
class Visitor(object):
    def __init__(self, iterator_class, filter_func=None):
        self._iter_class = iterator_class
        self.filter = filter_func

    def visit(self, node, *args, **kargs):
        """
        launch the visit on a given node

        call 'open_visit' before the beginning of the visit, with extra args
        given
        when all nodes have been visited, call the 'close_visit' method
        """
        self.open_visit(node, *args, **kargs)
        return self.close_visit(self._visit(node))

    def _visit(self, node):
        iterator = self._get_iterator(node)
        n = next(iterator)
        while n:
            result = n.accept(self)
            n = next(iterator)
        return result

    def _get_iterator(self, node):
        return self._iter_class(node, self.filter)

    def open_visit(self, *args, **kargs):
        """
        method called at the beginning of the visit
        """

    def close_visit(self, result):
        """
        method called at the end of the visit
        """
        return result


# standard visited mixin ######################################################
class VisitedMixIn(object):
    """
    Visited interface allow node visitors to use the node
    """

    def get_visit_name(self) -> str:
        """
        return the visit name for the mixed class. When calling 'accept', the
        method <'visit_' + name returned by this method> will be called on the
        visitor
        """
        try:
            # mypy: "VisitedMixIn" has no attribute "TYPE"
            # dynamic attribute
            return self.TYPE.replace("-", "_")  # type: ignore
        except Exception:
            return self.__class__.__name__.lower()

    def accept(
        self, visitor: Union[HTMLWriter, TextWriter], *args: Any, **kwargs: Any
    ) -> Optional[Any]:
        func = getattr(visitor, "visit_%s" % self.get_visit_name())
        return func(self, *args, **kwargs)

    def leave(self, visitor, *args, **kwargs):
        func = getattr(visitor, "leave_%s" % self.get_visit_name())
        return func(self, *args, **kwargs)
