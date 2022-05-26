# copyright 2019 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of yams.
#
# yams is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# yams is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with yams. If not, see <https://www.gnu.org/licenses/>.

"""Types declarations for types annotations"""

from typing import TYPE_CHECKING, TypeVar


# to avoid circular imports
if TYPE_CHECKING:
    from logilab.common.tree import Node
    from logilab.common.ureports.html_writer import HTMLWriter
    from logilab.common.ureports.text_writer import TextWriter
    from logilab.common.ureports.nodes import Paragraph
    from logilab.common.ureports.nodes import Title
    from logilab.common.table import Table
    from logilab.common.optik_ext import OptionParser
    from logilab.common.optik_ext import Option
    from logilab.common import attrdict
else:
    Node = TypeVar("Node")
    HTMLWriter = TypeVar("HTMLWriter")
    TextWriter = TypeVar("TextWriter")
    Table = TypeVar("Table")
    OptionParser = TypeVar("OptionParser")
    Option = TypeVar("Option")
    attrdict = TypeVar("attrdict")
    Paragraph = TypeVar("Paragraph")
    Title = TypeVar("Title")
