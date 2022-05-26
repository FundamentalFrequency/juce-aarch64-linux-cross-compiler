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
"""Base class to represent a tree structure.




"""
__docformat__ = "restructuredtext en"

import sys

from logilab.common.visitor import VisitedMixIn, FilteredIterator, no_filter
from typing import Optional, Any, List, Callable

# Exceptions #################################################################


class NodeNotFound(Exception):
    """raised when a node has not been found"""


EX_SIBLING_NOT_FOUND: str = "No such sibling as '%s'"
EX_CHILD_NOT_FOUND: str = "No such child as '%s'"
EX_NODE_NOT_FOUND: str = "No such node as '%s'"


# Base node ###################################################################

# describe node of current class
NodeType = Any


class Node(object):
    """a basic tree node, characterized by an id"""

    def __init__(self, nid: Optional[str] = None) -> None:
        self.id = nid
        # navigation
        # should be something like Optional[type(self)] for subclasses but that's not possible?
        self.parent: Optional[NodeType] = None
        # should be something like List[type(self)] for subclasses but that's not possible?
        self.children: List[NodeType] = []

    def __iter__(self):
        return iter(self.children)

    def __str__(self, indent=0):
        s = ["%s%s %s" % (" " * indent, self.__class__.__name__, self.id)]
        indent += 2
        for child in self.children:
            try:
                s.append(child.__str__(indent))
            except TypeError:
                s.append(child.__str__())
        return "\n".join(s)

    def is_leaf(self):
        return not self.children

    def append(self, child: NodeType) -> None:
        # should be child: type(self) but that's not possible
        """add a node to children"""
        self.children.append(child)
        child.parent = self

    def remove(self, child: NodeType) -> None:
        # should be child: type(self) but that's not possible
        """remove a child node"""
        self.children.remove(child)
        child.parent = None

    def insert(self, index: int, child: NodeType) -> None:
        # should be child: type(self) but that's not possible
        """insert a child node"""
        self.children.insert(index, child)
        child.parent = self

    def replace(self, old_child: NodeType, new_child: NodeType) -> None:
        """replace a child node with another"""
        i = self.children.index(old_child)
        self.children.pop(i)
        self.children.insert(i, new_child)
        new_child.parent = self

    def get_sibling(self, nid: str) -> NodeType:
        """return the sibling node that has given id"""
        try:
            assert self.parent is not None
            return self.parent.get_child_by_id(nid)
        except NodeNotFound:
            raise NodeNotFound(EX_SIBLING_NOT_FOUND % nid)

    def next_sibling(self):
        """
        return the next sibling for this node if any
        """
        parent = self.parent
        if parent is None:
            # root node has no sibling
            return None
        index = parent.children.index(self)
        try:
            return parent.children[index + 1]
        except IndexError:
            return None

    def previous_sibling(self):
        """
        return the previous sibling for this node if any
        """
        parent = self.parent
        if parent is None:
            # root node has no sibling
            return None
        index = parent.children.index(self)
        if index > 0:
            return parent.children[index - 1]
        return None

    def get_node_by_id(self, nid: str) -> NodeType:
        """
        return node in whole hierarchy that has given id
        """
        root = self.root()
        try:
            return root.get_child_by_id(nid, 1)
        except NodeNotFound:
            raise NodeNotFound(EX_NODE_NOT_FOUND % nid)

    def get_child_by_id(self, nid: str, recurse: Optional[bool] = None) -> NodeType:
        """
        return child of given id
        """
        if self.id == nid:
            return self
        for c in self.children:
            if recurse:
                try:
                    return c.get_child_by_id(nid, 1)
                except NodeNotFound:
                    continue
            if c.id == nid:
                return c
        raise NodeNotFound(EX_CHILD_NOT_FOUND % nid)

    def get_child_by_path(self, path: List[str]) -> NodeType:
        """
        return child of given path (path is a list of ids)
        """
        if len(path) > 0 and path[0] == self.id:
            if len(path) == 1:
                return self
            else:
                for c in self.children:
                    try:
                        return c.get_child_by_path(path[1:])
                    except NodeNotFound:
                        pass
        raise NodeNotFound(EX_CHILD_NOT_FOUND % path)

    def depth(self) -> int:
        """
        return depth of this node in the tree
        """
        if self.parent is not None:
            return 1 + self.parent.depth()
        else:
            return 0

    def depth_down(self) -> int:
        """
        return depth of the tree from this node
        """
        if self.children:
            return 1 + max([c.depth_down() for c in self.children])
        return 1

    def width(self) -> int:
        """
        return the width of the tree from this node
        """
        return len(self.leaves())

    def root(self) -> NodeType:
        """
        return the root node of the tree
        """
        if self.parent is not None:
            return self.parent.root()
        return self

    def leaves(self) -> List[NodeType]:
        """
        return a list with all the leaves nodes descendant from this node
        """
        leaves = []
        if self.children:
            for child in self.children:
                leaves += child.leaves()
            return leaves
        else:
            return [self]

    def flatten(self, _list: Optional[List[NodeType]] = None) -> List[NodeType]:
        """
        return a list with all the nodes descendant from this node
        """
        if _list is None:
            _list = []
        _list.append(self)
        for c in self.children:
            c.flatten(_list)
        return _list

    def lineage(self) -> List[NodeType]:
        """
        return list of parents up to root node
        """
        lst = [self]
        if self.parent is not None:
            lst.extend(self.parent.lineage())
        return lst


class VNode(Node, VisitedMixIn):
    # we should probably merge this VisitedMixIn here because it's only used here
    """a visitable node"""


class BinaryNode(VNode):
    """a binary node (i.e. only two children"""

    def __init__(self, lhs=None, rhs=None):
        VNode.__init__(self)
        if lhs is not None or rhs is not None:
            assert lhs and rhs
            self.append(lhs)
            self.append(rhs)

    def remove(self, child):
        """remove the child and replace this node with the other child"""
        self.children.remove(child)
        self.parent.replace(self, self.children[0])

    def get_parts(self):
        """
        return the left hand side and the right hand side of this node
        """
        return self.children[0], self.children[1]


if sys.version_info[0:2] >= (2, 2):
    list_class = list
else:
    from UserList import UserList

    list_class = UserList


class ListNode(VNode, list_class):
    """Used to manipulate Nodes as Lists"""

    def __init__(self):
        list_class.__init__(self)
        VNode.__init__(self)
        self.children = self

    def __str__(self, indent=0):
        return "%s%s %s" % (
            indent * " ",
            self.__class__.__name__,
            ", ".join([str(v) for v in self]),
        )

    def append(self, child):
        """add a node to children"""
        list_class.append(self, child)
        child.parent = self

    def insert(self, index, child):
        """add a node to children"""
        list_class.insert(self, index, child)
        child.parent = self

    def remove(self, child):
        """add a node to children"""
        list_class.remove(self, child)
        child.parent = None

    def pop(self, index):
        """add a node to children"""
        child = list_class.pop(self, index)
        child.parent = None

    def __iter__(self):
        return list_class.__iter__(self)


# construct list from tree ####################################################


def post_order_list(node: Optional[Node], filter_func: Callable = no_filter) -> List[Node]:
    """
    create a list with tree nodes for which the <filter> function returned true
    in a post order fashion
    """
    l, stack = [], []
    poped, index = 0, 0
    while node:
        if filter_func(node):
            if node.children and not poped:
                stack.append((node, index))
                index = 0
                node = node.children[0]
            else:
                l.append(node)
                index += 1
                try:
                    node = stack[-1][0].children[index]
                except IndexError:
                    node = None
        else:
            node = None
        poped = 0
        if node is None and stack:
            node, index = stack.pop()
            poped = 1
    return l


def pre_order_list(node: Optional[Node], filter_func: Callable = no_filter) -> List[Node]:
    """
    create a list with tree nodes for which the <filter> function returned true
    in a pre order fashion
    """
    l, stack = [], []
    poped, index = 0, 0
    while node:
        if filter_func(node):
            if not poped:
                l.append(node)
            if node.children and not poped:
                stack.append((node, index))
                index = 0
                node = node.children[0]
            else:
                index += 1
                try:
                    node = stack[-1][0].children[index]
                except IndexError:
                    node = None
        else:
            node = None
        poped = 0
        if node is None and len(stack) > 1:
            node, index = stack.pop()
            poped = 1
    return l


class PostfixedDepthFirstIterator(FilteredIterator):
    """a postfixed depth first iterator, designed to be used with visitors"""

    def __init__(self, node: Node, filter_func: Optional[Any] = None) -> None:
        FilteredIterator.__init__(self, node, post_order_list, filter_func)


class PrefixedDepthFirstIterator(FilteredIterator):
    """a prefixed depth first iterator, designed to be used with visitors"""

    def __init__(self, node: Node, filter_func: Optional[Any] = None) -> None:
        FilteredIterator.__init__(self, node, pre_order_list, filter_func)
