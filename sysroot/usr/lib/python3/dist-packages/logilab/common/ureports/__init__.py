# copyright 2003-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-common.
#
# logilab-common is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License,
# or (at your option) any later version.
#
# logilab-common is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with logilab-common.  If not, see <http://www.gnu.org/licenses/>.
"""Universal report objects and some formatting drivers.

A way to create simple reports using python objects, primarily designed to be
formatted as text and html.
"""
__docformat__ = "restructuredtext en"

import sys

from typing import Any, Optional, Union, List as ListType, Generator, Tuple, Callable, TextIO

from logilab.common.compat import StringIO
from logilab.common.textutils import linesep
from logilab.common.tree import VNode
from logilab.common.ureports.nodes import Table, Section, Link, Paragraph, Title, Text

from logilab.common.ureports.nodes import VerbatimText, Image, Span, List  # noqa


def get_nodes(node, klass):
    """return an iterator on all children node of the given klass"""
    for child in node.children:
        if isinstance(child, klass):
            yield child
        # recurse (FIXME: recursion controled by an option)
        for grandchild in get_nodes(child, klass):
            yield grandchild


def layout_title(layout):
    """try to return the layout's title as string, return None if not found"""
    for child in layout.children:
        if isinstance(child, Title):
            return " ".join([node.data for node in get_nodes(child, Text)])


def build_summary(layout, level=1):
    """make a summary for the report, including X level"""
    assert level > 0
    level -= 1
    summary = ListType(klass="summary")
    for child in layout.children:
        if not isinstance(child, Section):
            continue
        label = layout_title(child)
        if not label and not child.id:
            continue
        if not child.id:
            child.id = label.replace(" ", "-")
        node = Link("#" + child.id, label=label or child.id)
        # FIXME: Three following lines produce not very compliant
        # docbook: there are some useless <para><para>. They might be
        # replaced by the three commented lines but this then produces
        # a bug in html display...
        if level and [n for n in child.children if isinstance(n, Section)]:
            node = Paragraph([node, build_summary(child, level)])
        summary.append(node)
    #         summary.append(node)
    #         if level and [n for n in child.children if isinstance(n, Section)]:
    #             summary.append(build_summary(child, level))
    return summary


class BaseWriter(object):
    """base class for ureport writers"""

    def format(
        self,
        layout: Any,
        stream: Optional[Union[StringIO, TextIO]] = None,
        encoding: Optional[Any] = None,
    ) -> None:
        """format and write the given layout into the stream object

        unicode policy: unicode strings may be found in the layout;
        try to call stream.write with it, but give it back encoded using
        the given encoding if it fails
        """
        if stream is None:
            stream = sys.stdout
        if not encoding:
            encoding = getattr(stream, "encoding", "UTF-8")
        self.encoding = encoding or "UTF-8"
        self.__compute_funcs: ListType[Tuple[Callable[[str], Any], Callable[[str], Any]]] = []
        self.out = stream
        self.begin_format(layout)
        layout.accept(self)
        self.end_format(layout)

    def format_children(self, layout: Union["Paragraph", "Section", "Title"]) -> None:
        """recurse on the layout children and call their accept method
        (see the Visitor pattern)
        """
        for child in getattr(layout, "children", ()):
            child.accept(self)

    def writeln(self, string: str = "") -> None:
        """write a line in the output buffer"""
        self.write(string + linesep)

    def write(self, string: str) -> None:
        """write a string in the output buffer"""
        try:
            self.out.write(string)
        except UnicodeEncodeError:
            # mypy: Argument 1 to "write" of "IO" has incompatible type "bytes"; expected "str"
            # probably a python3 port issue?
            self.out.write(string.encode(self.encoding))  # type: ignore

    def begin_format(self, layout: Any) -> None:
        """begin to format a layout"""
        self.section = 0

    def end_format(self, layout: Any) -> None:
        """finished to format a layout"""

    def get_table_content(self, table: Table) -> ListType[ListType[str]]:
        """trick to get table content without actually writing it

        return an aligned list of lists containing table cells values as string
        """
        result: ListType[ListType[str]] = [[]]
        # mypy: "Table" has no attribute "cols"
        # dynamic attribute
        cols = table.cols  # type: ignore

        for cell in self.compute_content(table):
            if cols == 0:
                result.append([])
                # mypy: "Table" has no attribute "cols"
                # dynamic attribute
                cols = table.cols  # type: ignore

            cols -= 1
            result[-1].append(cell)

        # fill missing cells
        while len(result[-1]) < cols:
            result[-1].append("")

        return result

    def compute_content(self, layout: VNode) -> Generator[str, Any, None]:
        """trick to compute the formatting of children layout before actually
        writing it

        return an iterator on strings (one for each child element)
        """
        # use cells !
        def write(data: str) -> None:
            try:
                stream.write(data)
            except UnicodeEncodeError:
                # mypy: Argument 1 to "write" of "TextIOWrapper" has incompatible type "bytes";
                # mypy: expected "str"
                # error from porting to python3?
                stream.write(data.encode(self.encoding))  # type: ignore

        def writeln(data: str = "") -> None:
            try:
                stream.write(data + linesep)
            except UnicodeEncodeError:
                # mypy: Unsupported operand types for + ("bytes" and "str")
                # error from porting to python3?
                stream.write(data.encode(self.encoding) + linesep)  # type: ignore

        # mypy: Cannot assign to a method
        # this really looks like black dirty magic since self.write is reused elsewhere in the code
        # especially since self.write and self.writeln are conditionally
        # deleted at the end of this function
        self.write = write  # type: ignore
        self.writeln = writeln  # type: ignore

        self.__compute_funcs.append((write, writeln))

        # mypy: Item "Table" of "Union[ListType[Any], Table, Title]" has no attribute "children"
        # dynamic attribute?
        for child in layout.children:  # type: ignore
            stream = StringIO()

            child.accept(self)

            yield stream.getvalue()

        self.__compute_funcs.pop()

        try:
            # mypy: Cannot assign to a method
            # even more black dirty magic
            self.write, self.writeln = self.__compute_funcs[-1]  # type: ignore
        except IndexError:
            del self.write
            del self.writeln


from logilab.common.ureports.text_writer import TextWriter  # noqa
from logilab.common.ureports.html_writer import HTMLWriter  # noqa
