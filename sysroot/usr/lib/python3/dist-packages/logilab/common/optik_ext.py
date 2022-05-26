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
"""Add an abstraction level to transparently import optik classes from optparse
(python >= 2.3) or the optik package.

It also defines three new types for optik/optparse command line parser :

  * regexp
    argument of this type will be converted using re.compile
  * csv
    argument of this type will be converted using split(',')
  * yn
    argument of this type will be true if 'y' or 'yes', false if 'n' or 'no'
  * named
    argument of this type are in the form <NAME>=<VALUE> or <NAME>:<VALUE>
  * password
    argument of this type wont be converted but this is used by other tools
    such as interactive prompt for configuration to double check value and
    use an invisible field
  * multiple_choice
    same as default "choice" type but multiple choices allowed
  * file
    argument of this type wont be converted but checked that the given file exists
  * color
    argument of this type wont be converted but checked its either a
    named color or a color specified using hexadecimal notation (preceded by a #)
  * time
    argument of this type will be converted to a float value in seconds
    according to time units (ms, s, min, h, d)
  * bytes
    argument of this type will be converted to a float value in bytes
    according to byte units (b, kb, mb, gb, tb)
"""
from __future__ import print_function

__docformat__ = "restructuredtext en"

import re
import sys
import time
from copy import copy
from os.path import exists
from logilab.common import attrdict

from typing import Any, Union, List, Optional, Tuple, Dict
from _io import StringIO

# python >= 2.3
from optparse import (  # noqa
    OptionParser as BaseParser,
    Option as BaseOption,
    OptionGroup,
    OptionContainer,
    OptionValueError,
    OptionError,
    Values,
    HelpFormatter,
    SUPPRESS_HELP,
    NO_DEFAULT,
)

try:
    from mx import DateTime

    HAS_MX_DATETIME = True
except ImportError:
    HAS_MX_DATETIME = False

from logilab.common.textutils import splitstrip, TIME_UNITS, BYTE_UNITS, apply_units


def check_regexp(option, opt, value):
    """check a regexp value by trying to compile it
    return the compiled regexp
    """
    if hasattr(value, "pattern"):
        return value
    try:
        return re.compile(value)
    except ValueError:
        raise OptionValueError("option %s: invalid regexp value: %r" % (opt, value))


def check_csv(
    option: Optional["Option"], opt: str, value: Union[List[str], Tuple[str, ...], str]
) -> Union[List[str], Tuple[str, ...]]:
    """check a csv value by trying to split it
    return the list of separated values
    """
    if isinstance(value, (list, tuple)):
        return value
    try:
        return splitstrip(value)
    except ValueError:
        raise OptionValueError("option %s: invalid csv value: %r" % (opt, value))


def check_yn(option: Optional["Option"], opt: str, value: Union[bool, str]) -> bool:
    """check a yn value
    return true for yes and false for no
    """
    if isinstance(value, int):
        return bool(value)
    if value in ("y", "yes"):
        return True
    if value in ("n", "no"):
        return False
    msg = "option %s: invalid yn value %r, should be in (y, yes, n, no)"
    raise OptionValueError(msg % (opt, value))


def check_named(
    option: Optional[Any], opt: str, value: Union[Dict[str, str], str]
) -> Dict[str, str]:
    """check a named value
    return a dictionary containing (name, value) associations
    """
    if isinstance(value, dict):
        return value
    values: List[Tuple[str, str]] = []
    for value in check_csv(option, opt, value):
        # mypy: Argument 1 to "append" of "list" has incompatible type "List[str]";
        # mypy: expected "Tuple[str, str]"
        # we know that the split will give a 2 items list
        if value.find("=") != -1:
            values.append(value.split("=", 1))  # type: ignore
        elif value.find(":") != -1:
            values.append(value.split(":", 1))  # type: ignore
    if values:
        return dict(values)
    msg = "option %s: invalid named value %r, should be <NAME>=<VALUE> or \
<NAME>:<VALUE>"
    raise OptionValueError(msg % (opt, value))


def check_password(option, opt, value):
    """check a password value (can't be empty)"""
    # no actual checking, monkey patch if you want more
    return value


def check_file(option, opt, value):
    """check a file value
    return the filepath
    """
    if exists(value):
        return value
    msg = "option %s: file %r does not exist"
    raise OptionValueError(msg % (opt, value))


# XXX use python datetime
def check_date(option, opt, value):
    """check a file value
    return the filepath
    """
    try:
        return DateTime.strptime(value, "%Y/%m/%d")
    except DateTime.Error:
        raise OptionValueError("expected format of %s is yyyy/mm/dd" % opt)


def check_color(option, opt, value):
    """check a color value and returns it
    /!\\ does *not* check color labels (like 'red', 'green'), only
    checks hexadecimal forms
    """
    # Case (1) : color label, we trust the end-user
    if re.match("[a-z0-9 ]+$", value, re.I):
        return value
    # Case (2) : only accepts hexadecimal forms
    if re.match("#[a-f0-9]{6}", value, re.I):
        return value
    # Else : not a color label neither a valid hexadecimal form => error
    msg = "option %s: invalid color : %r, should be either hexadecimal \
    value or predefined color"
    raise OptionValueError(msg % (opt, value))


def check_time(option, opt, value):
    if isinstance(value, (int, float)):
        return value
    return apply_units(value, TIME_UNITS)


def check_bytes(option: Optional["Option"], opt: str, value: Any) -> int:
    if hasattr(value, "__int__"):
        return value
    # mypy: Incompatible return value type (got "Union[float, int]", expected "int")
    # we force "int" using "final=int"
    return apply_units(value, BYTE_UNITS, final=int)  # type: ignore


class Option(BaseOption):
    """override optik.Option to add some new option types"""

    TYPES = BaseOption.TYPES + (
        "regexp",
        "csv",
        "yn",
        "named",
        "password",
        "multiple_choice",
        "file",
        "color",
        "time",
        "bytes",
    )
    ATTRS = BaseOption.ATTRS + ["hide", "level"]
    TYPE_CHECKER = copy(BaseOption.TYPE_CHECKER)
    TYPE_CHECKER["regexp"] = check_regexp
    TYPE_CHECKER["csv"] = check_csv
    TYPE_CHECKER["yn"] = check_yn
    TYPE_CHECKER["named"] = check_named
    TYPE_CHECKER["multiple_choice"] = check_csv
    TYPE_CHECKER["file"] = check_file
    TYPE_CHECKER["color"] = check_color
    TYPE_CHECKER["password"] = check_password
    TYPE_CHECKER["time"] = check_time
    TYPE_CHECKER["bytes"] = check_bytes
    if HAS_MX_DATETIME:
        TYPES += ("date",)
        TYPE_CHECKER["date"] = check_date

    def __init__(self, *opts: str, **attrs: Any) -> None:
        BaseOption.__init__(self, *opts, **attrs)
        # mypy: "Option" has no attribute "hide"
        # we test that in the if
        if hasattr(self, "hide") and self.hide:  # type: ignore
            self.help = SUPPRESS_HELP

    def _check_choice(self) -> None:
        """FIXME: need to override this due to optik misdesign"""
        if self.type in ("choice", "multiple_choice"):
            # mypy: "Option" has no attribute "choices"
            # we know that option of this type has this attribute
            if self.choices is None:  # type: ignore
                raise OptionError("must supply a list of choices for type 'choice'", self)
            elif not isinstance(self.choices, (tuple, list)):  # type: ignore
                raise OptionError(
                    "choices must be a list of strings ('%s' supplied)"
                    % str(type(self.choices)).split("'")[1],  # type: ignore
                    self,
                )
        elif self.choices is not None:  # type: ignore
            raise OptionError("must not supply choices for type %r" % self.type, self)

    # mypy: Unsupported target for indexed assignment
    # black magic?
    BaseOption.CHECK_METHODS[2] = _check_choice  # type: ignore

    def process(self, opt: str, value: str, values: Values, parser: BaseParser) -> int:
        # First, convert the value(s) to the right type.  Howl if any
        # value(s) are bogus.
        value = self.convert_value(opt, value)
        if self.type == "named":
            assert self.dest is not None
            existant = getattr(values, self.dest)
            if existant:
                existant.update(value)
                value = existant
        # And then take whatever action is expected of us.
        # This is a separate method to make life easier for
        # subclasses to add new actions.
        # mypy: Argument 2 to "take_action" of "Option" has incompatible type "Optional[str]";
        # mypy: expected "str"
        # is it ok?
        return self.take_action(self.action, self.dest, opt, value, values, parser)  # type: ignore


class OptionParser(BaseParser):
    """override optik.OptionParser to use our Option class"""

    def __init__(self, option_class: type = Option, *args: Any, **kwargs: Any) -> None:
        # mypy: Argument "option_class" to "__init__" of "OptionParser" has incompatible type
        # mypy: "type"; expected "Option"
        # mypy is doing really weird things with *args/**kwargs and looks buggy
        BaseParser.__init__(self, option_class=option_class, *args, **kwargs)  # type: ignore

    def format_option_help(self, formatter: Optional[HelpFormatter] = None) -> str:
        if formatter is None:
            formatter = self.formatter
        outputlevel = getattr(formatter, "output_level", 0)
        formatter.store_option_strings(self)
        result = []
        result.append(formatter.format_heading("Options"))
        formatter.indent()
        if self.option_list:
            result.append(OptionContainer.format_option_help(self, formatter))
            result.append("\n")
        for group in self.option_groups:
            # mypy: "OptionParser" has no attribute "level"
            # but it has one no?
            if group.level <= outputlevel and (  # type: ignore
                group.description or level_options(group, outputlevel)
            ):
                result.append(group.format_help(formatter))
                result.append("\n")
        formatter.dedent()
        # Drop the last "\n", or the header if no options or option groups:
        return "".join(result[:-1])


# mypy error: error: "Type[OptionGroup]" has no attribute "level"
# monkeypatching
OptionGroup.level = 0  # type: ignore


def level_options(group: BaseParser, outputlevel: int) -> List[BaseOption]:
    # mypy: "Option" has no attribute "help"
    # but it does
    return [
        option
        for option in group.option_list
        if (getattr(option, "level", 0) or 0) <= outputlevel and option.help is not SUPPRESS_HELP  # type: ignore  # noqa
    ]


def format_option_help(self, formatter):
    result = []
    outputlevel = getattr(formatter, "output_level", 0) or 0
    for option in level_options(self, outputlevel):
        result.append(formatter.format_option(option))
    return "".join(result)


# mypy error: Cannot assign to a method
# but we still do it because magic
OptionContainer.format_option_help = format_option_help  # type: ignore


class ManHelpFormatter(HelpFormatter):
    """Format help using man pages ROFF format"""

    def __init__(
        self,
        indent_increment: int = 0,
        max_help_position: int = 24,
        width: int = 79,
        short_first: int = 0,
    ) -> None:
        HelpFormatter.__init__(self, indent_increment, max_help_position, width, short_first)

    def format_heading(self, heading: str) -> str:
        return ".SH %s\n" % heading.upper()

    def format_description(self, description):
        return description

    def format_option(self, option: BaseParser) -> str:
        try:
            # mypy: "Option" has no attribute "option_strings"
            # we handle if it doesn't
            optstring = option.option_strings  # type: ignore
        except AttributeError:
            optstring = self.format_option_strings(option)
        # mypy: "OptionParser" has no attribute "help"
        # it does
        if option.help:  # type: ignore
            # mypy: Argument 1 to "expand_default" of "HelpFormatter" has incompatible type
            # mypy: "OptionParser"; expected "Option"
            # it still works?
            help_text = self.expand_default(option)  # type: ignore
            help = " ".join([line.strip() for line in help_text.splitlines()])
        else:
            help = ""
        return """.IP "%s"
%s
""" % (
            optstring,
            help,
        )

    def format_head(self, optparser: OptionParser, pkginfo: attrdict, section: int = 1) -> str:
        long_desc = ""
        pgm = optparser.get_prog_name()
        short_desc = self.format_short_description(pgm, pkginfo.description)
        if hasattr(pkginfo, "long_desc"):
            long_desc = self.format_long_description(pgm, pkginfo.long_desc)
        return "%s\n%s\n%s\n%s" % (
            self.format_title(pgm, section),
            short_desc,
            self.format_synopsis(pgm),
            long_desc,
        )

    def format_title(self, pgm: str, section: int) -> str:
        date = "-".join([str(num) for num in time.localtime()[:3]])
        return '.TH %s %s "%s" %s' % (pgm, section, date, pgm)

    def format_short_description(self, pgm: str, short_desc: str) -> str:
        return r""".SH NAME
.B %s
\- %s
""" % (
            pgm,
            short_desc.strip(),
        )

    def format_synopsis(self, pgm: str) -> str:
        return (
            """.SH SYNOPSIS
.B  %s
[
.I OPTIONS
] [
.I <arguments>
]
"""
            % pgm
        )

    def format_long_description(self, pgm, long_desc):
        long_desc = "\n".join([line.lstrip() for line in long_desc.splitlines()])
        long_desc = long_desc.replace("\n.\n", "\n\n")
        if long_desc.lower().startswith(pgm):
            long_desc = long_desc[len(pgm) :]
        return """.SH DESCRIPTION
.B %s
%s
""" % (
            pgm,
            long_desc.strip(),
        )

    def format_tail(self, pkginfo: attrdict) -> str:
        tail = """.SH SEE ALSO
/usr/share/doc/pythonX.Y-%s/

.SH BUGS
Please report bugs on the project\'s mailing list:
%s

.SH AUTHOR
%s <%s>
""" % (
            getattr(pkginfo, "debian_name", pkginfo.modname),
            pkginfo.mailinglist,
            pkginfo.author,
            pkginfo.author_email,
        )

        if hasattr(pkginfo, "copyright"):
            tail += (
                """
.SH COPYRIGHT
%s
"""
                % pkginfo.copyright
            )

        return tail


def generate_manpage(
    optparser: OptionParser,
    pkginfo: attrdict,
    section: int = 1,
    stream: StringIO = sys.stdout,
    level: int = 0,
) -> None:
    """generate a man page from an optik parser"""
    formatter = ManHelpFormatter()
    # mypy: "ManHelpFormatter" has no attribute "output_level"
    # dynamic attribute?
    formatter.output_level = level  # type: ignore
    formatter.parser = optparser
    print(formatter.format_head(optparser, pkginfo, section), file=stream)
    print(optparser.format_option_help(formatter), file=stream)
    print(formatter.format_tail(pkginfo), file=stream)


__all__ = ("OptionParser", "Option", "OptionGroup", "OptionValueError", "Values")
