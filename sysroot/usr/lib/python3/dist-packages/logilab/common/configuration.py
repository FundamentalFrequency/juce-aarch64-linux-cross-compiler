# copyright 2003-2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""Classes to handle advanced configuration in simple to complex applications.

Allows to load the configuration from a file or from command line
options, to generate a sample configuration file or to display
program's usage. Fills the gap between optik/optparse and ConfigParser
by adding data types (which are also available as a standalone optik
extension in the `optik_ext` module).


Quick start: simplest usage
---------------------------

.. ::

  >>> import sys
  >>> from logilab.common.configuration import Configuration
  >>> options = [('dothis', {'type':'yn', 'default': True, 'metavar': '<y or n>'}),
  ...            ('value', {'type': 'string', 'metavar': '<string>'}),
  ...            ('multiple', {'type': 'csv', 'default': ('yop',),
  ...                          'metavar': '<comma separated values>',
  ...                          'help': 'you can also document the option'}),
  ...            ('number', {'type': 'int', 'default':2, 'metavar':'<int>'}),
  ...           ]
  >>> config = Configuration(options=options, name='My config')
  >>> print config['dothis']
  True
  >>> print config['value']
  None
  >>> print config['multiple']
  ('yop',)
  >>> print config['number']
  2
  >>> print config.help()
  Usage:  [options]

  Options:
    -h, --help            show this help message and exit
    --dothis=<y or n>
    --value=<string>
    --multiple=<comma separated values>
                          you can also document the option [current: none]
    --number=<int>

  >>> f = open('myconfig.ini', 'w')
  >>> f.write('''[MY CONFIG]
  ... number = 3
  ... dothis = no
  ... multiple = 1,2,3
  ... ''')
  >>> f.close()
  >>> config.load_file_configuration('myconfig.ini')
  >>> print config['dothis']
  False
  >>> print config['value']
  None
  >>> print config['multiple']
  ['1', '2', '3']
  >>> print config['number']
  3
  >>> sys.argv = ['mon prog', '--value', 'bacon', '--multiple', '4,5,6',
  ...             'nonoptionargument']
  >>> print config.load_command_line_configuration()
  ['nonoptionargument']
  >>> print config['value']
  bacon
  >>> config.generate_config()
  # class for simple configurations which don't need the
  # manager / providers model and prefer delegation to inheritance
  #
  # configuration values are accessible through a dict like interface
  #
  [MY CONFIG]

  dothis=no

  value=bacon

  # you can also document the option
  multiple=4,5,6

  number=3

  Note : starting with Python 2.7 ConfigParser is able to take into
  account the order of occurrences of the options into a file (by
  using an OrderedDict). If you have two options changing some common
  state, like a 'disable-all-stuff' and a 'enable-some-stuff-a', their
  order of appearance will be significant : the last specified in the
  file wins. For earlier version of python and logilab.common newer
  than 0.61 the behaviour is unspecified.

"""

from __future__ import print_function

__docformat__ = "restructuredtext en"

__all__ = (
    "OptionsManagerMixIn",
    "OptionsProviderMixIn",
    "ConfigurationMixIn",
    "Configuration",
    "OptionsManager2ConfigurationAdapter",
)

import os
import sys
import re
from os.path import exists, expanduser
from optparse import OptionGroup
from copy import copy
from _io import StringIO, TextIOWrapper
from typing import Any, Optional, Union, Dict, List, Tuple, Iterator, Callable
from warnings import warn

import configparser as cp

from logilab.common.types import OptionParser, Option, attrdict
from logilab.common.compat import str_encode as _encode
from logilab.common.deprecation import callable_deprecated
from logilab.common.textutils import normalize_text, unquote
from logilab.common import optik_ext


OptionError = optik_ext.OptionError

REQUIRED: List = []


class UnsupportedAction(Exception):
    """raised by set_option when it doesn't know what to do for an action"""


def _get_encoding(encoding: Optional[str], stream: Union[StringIO, TextIOWrapper]) -> str:
    encoding = encoding or getattr(stream, "encoding", None)
    if not encoding:
        import locale

        encoding = locale.getpreferredencoding()
    return encoding


_ValueType = Union[List[str], Tuple[str, ...], str]

# validation functions ########################################################

# validators will return the validated value or raise optparse.OptionValueError
# XXX add to documentation


def choice_validator(optdict: Dict[str, Any], name: str, value: str) -> str:
    """validate and return a converted value for option of type 'choice'"""
    if value not in optdict["choices"]:
        msg = "option %s: invalid value: %r, should be in %s"
        raise optik_ext.OptionValueError(msg % (name, value, optdict["choices"]))
    return value


def multiple_choice_validator(optdict: Dict[str, Any], name: str, value: _ValueType) -> _ValueType:
    """validate and return a converted value for option of type 'choice'"""
    choices = optdict["choices"]
    values = optik_ext.check_csv(None, name, value)
    for value in values:
        if value not in choices:
            msg = "option %s: invalid value: %r, should be in %s"
            raise optik_ext.OptionValueError(msg % (name, value, choices))
    return values


def csv_validator(optdict: Dict[str, Any], name: str, value: _ValueType) -> _ValueType:
    """validate and return a converted value for option of type 'csv'"""
    return optik_ext.check_csv(None, name, value)


def yn_validator(optdict: Dict[str, Any], name: str, value: Union[bool, str]) -> bool:
    """validate and return a converted value for option of type 'yn'"""
    return optik_ext.check_yn(None, name, value)


def named_validator(
    optdict: Dict[str, Any], name: str, value: Union[Dict[str, str], str]
) -> Dict[str, str]:
    """validate and return a converted value for option of type 'named'"""
    return optik_ext.check_named(None, name, value)


def file_validator(optdict, name, value):
    """validate and return a filepath for option of type 'file'"""
    return optik_ext.check_file(None, name, value)


def color_validator(optdict, name, value):
    """validate and return a valid color for option of type 'color'"""
    return optik_ext.check_color(None, name, value)


def password_validator(optdict, name, value):
    """validate and return a string for option of type 'password'"""
    return optik_ext.check_password(None, name, value)


def date_validator(optdict, name, value):
    """validate and return a mx DateTime object for option of type 'date'"""
    return optik_ext.check_date(None, name, value)


def time_validator(optdict, name, value):
    """validate and return a time object for option of type 'time'"""
    return optik_ext.check_time(None, name, value)


def bytes_validator(optdict: Dict[str, str], name: str, value: Union[int, str]) -> int:
    """validate and return an integer for option of type 'bytes'"""
    return optik_ext.check_bytes(None, name, value)


VALIDATORS: Dict[str, Callable] = {
    "string": unquote,
    "int": int,
    "float": float,
    "file": file_validator,
    "font": unquote,
    "color": color_validator,
    "regexp": re.compile,
    "csv": csv_validator,
    "yn": yn_validator,
    "bool": yn_validator,
    "named": named_validator,
    "password": password_validator,
    "date": date_validator,
    "time": time_validator,
    "bytes": bytes_validator,
    "choice": choice_validator,
    "multiple_choice": multiple_choice_validator,
}


def _call_validator(
    opttype: str, optdict: Dict[str, Any], option: str, value: Union[List[str], int, str]
) -> Union[List[str], int, str]:
    if opttype not in VALIDATORS:
        raise Exception('Unsupported type "%s"' % opttype)
    try:
        return VALIDATORS[opttype](optdict, option, value)
    except TypeError:
        try:
            return VALIDATORS[opttype](value)
        except optik_ext.OptionValueError:
            raise
        except Exception:
            raise optik_ext.OptionValueError(
                "%s value (%r) should be of type %s" % (option, value, opttype)
            )


# user input functions ########################################################

# user input functions will ask the user for input on stdin then validate
# the result and return the validated value or raise optparse.OptionValueError
# XXX add to documentation


def input_password(optdict, question="password:"):
    from getpass import getpass

    while True:
        value = getpass(question)
        value2 = getpass("confirm: ")
        if value == value2:
            return value
        print("password mismatch, try again")


def input_string(optdict, question):
    value = input(question).strip()
    return value or None


def _make_input_function(opttype):
    def input_validator(optdict, question):
        while True:
            value = input(question)
            if not value.strip():
                return None
            try:
                return _call_validator(opttype, optdict, None, value)
            except optik_ext.OptionValueError as ex:
                msg = str(ex).split(":", 1)[-1].strip()
                print("bad value: %s" % msg)

    return input_validator


INPUT_FUNCTIONS: Dict[str, Callable] = {
    "string": input_string,
    "password": input_password,
}

for opttype in VALIDATORS.keys():
    INPUT_FUNCTIONS.setdefault(opttype, _make_input_function(opttype))

# utility functions ############################################################


def expand_default(self, option):
    """monkey patch OptionParser.expand_default since we have a particular
    way to handle defaults to avoid overriding values in the configuration
    file
    """
    if self.parser is None or not self.default_tag:
        return option.help
    optname = option._long_opts[0][2:]
    try:
        provider = self.parser.options_manager._all_options[optname]
    except KeyError:
        value = None
    else:
        optdict = provider.get_option_def(optname)
        optname = provider.option_attrname(optname, optdict)
        value = getattr(provider.config, optname, optdict)
        value = format_option_value(optdict, value)
    if value is optik_ext.NO_DEFAULT or not value:
        value = self.NO_DEFAULT_VALUE
    return option.help.replace(self.default_tag, str(value))


def _validate(
    value: Union[List[str], int, str], optdict: Dict[str, Any], name: str = ""
) -> Union[List[str], int, str]:
    """return a validated value for an option according to its type

    optional argument name is only used for error message formatting
    """
    try:
        _type = optdict["type"]
    except KeyError:
        # FIXME
        return value
    return _call_validator(_type, optdict, name, value)


convert = callable_deprecated("[0.60] convert() was renamed _validate()")(_validate)

# format and output functions ##################################################


def comment(string):
    """return string as a comment"""
    lines = [line.strip() for line in string.splitlines()]
    return "# " + ("%s# " % os.linesep).join(lines)


def format_time(value):
    if not value:
        return "0"
    if value != int(value):
        return "%.2fs" % value
    value = int(value)
    nbmin, nbsec = divmod(value, 60)
    if nbsec:
        return "%ss" % value
    nbhour, nbmin_ = divmod(nbmin, 60)
    if nbmin_:
        return "%smin" % nbmin
    nbday, nbhour_ = divmod(nbhour, 24)
    if nbhour_:
        return "%sh" % nbhour
    return "%sd" % nbday


def format_bytes(value: int) -> str:
    if not value:
        return "0"
    if value != int(value):
        return "%.2fB" % value
    value = int(value)
    prevunit = "B"
    for unit in ("KB", "MB", "GB", "TB"):
        next, remain = divmod(value, 1024)
        if remain:
            return "%s%s" % (value, prevunit)
        prevunit = unit
        value = next
    return "%s%s" % (value, unit)


def format_option_value(optdict: Dict[str, Any], value: Any) -> Union[None, int, str]:
    """return the user input's value from a 'compiled' value"""
    if isinstance(value, (list, tuple)):
        value = ",".join(value)
    elif isinstance(value, dict):
        value = ",".join(["%s:%s" % (k, v) for k, v in value.items()])
    elif hasattr(value, "match"):  # optdict.get('type') == 'regexp'
        # compiled regexp
        value = value.pattern
    elif optdict.get("type") == "yn":
        value = value and "yes" or "no"
    elif isinstance(value, str) and value.isspace():
        value = "'%s'" % value
    elif optdict.get("type") == "time" and isinstance(value, (float, int)):
        value = format_time(value)
    elif optdict.get("type") == "bytes" and hasattr(value, "__int__"):
        value = format_bytes(value)
    return value


def ini_format_section(
    stream: Union[StringIO, TextIOWrapper],
    section: str,
    options: Any,
    encoding: str = None,
    doc: Optional[Any] = None,
) -> None:
    """format an options section using the INI format"""
    encoding = _get_encoding(encoding, stream)
    if doc:
        print(_encode(comment(doc), encoding), file=stream)
    print("[%s]" % section, file=stream)
    ini_format(stream, options, encoding)


def ini_format(stream: Union[StringIO, TextIOWrapper], options: Any, encoding: str) -> None:
    """format options using the INI format"""
    for optname, optdict, value in options:
        value = format_option_value(optdict, value)
        help = optdict.get("help")
        if help:
            help = normalize_text(help, line_len=79, indent="# ")
            print(file=stream)
            print(_encode(help, encoding), file=stream)
        else:
            print(file=stream)
        if value is None:
            print("#%s=" % optname, file=stream)
        else:
            value = _encode(value, encoding).strip()
            if optdict.get("type") == "string" and "\n" in value:
                prefix = "\n    "
                value = prefix + prefix.join(value.split("\n"))
            print("%s=%s" % (optname, value), file=stream)


format_section = ini_format_section


def rest_format_section(stream, section, options, encoding=None, doc=None):
    """format an options section using as ReST formatted output"""
    encoding = _get_encoding(encoding, stream)
    if section:
        print("%s\n%s" % (section, "'" * len(section)), file=stream)
    if doc:
        print(_encode(normalize_text(doc, line_len=79, indent=""), encoding), file=stream)
        print(file=stream)
    for optname, optdict, value in options:
        help = optdict.get("help")
        print(":%s:" % optname, file=stream)
        if help:
            help = normalize_text(help, line_len=79, indent="  ")
            print(_encode(help, encoding), file=stream)
        if value:
            value = _encode(format_option_value(optdict, value), encoding)
            print(file=stream)
            print("  Default: ``%s``" % value.replace("`` ", "```` ``"), file=stream)


# Options Manager ##############################################################


class OptionsManagerMixIn(object):
    """MixIn to handle a configuration from both a configuration file and
    command line options
    """

    def __init__(
        self,
        usage: Optional[str],
        config_file: Optional[Any] = None,
        version: Optional[Any] = None,
        quiet: int = 0,
    ) -> None:
        self.config_file = config_file
        self.reset_parsers(usage, version=version)
        # list of registered options providers
        self.options_providers: List[ConfigurationMixIn] = []
        # dictionary associating option name to checker
        self._all_options: Dict[str, ConfigurationMixIn] = {}
        self._short_options: Dict[str, str] = {}
        self._nocallback_options: Dict[ConfigurationMixIn, str] = {}
        self._mygroups: Dict[str, optik_ext.OptionGroup] = {}
        # verbosity
        self.quiet = quiet
        self._maxlevel = 0

    def reset_parsers(self, usage: Optional[str] = "", version: Optional[Any] = None) -> None:
        # configuration file parser
        self.cfgfile_parser = cp.ConfigParser()
        # command line parser
        self.cmdline_parser = optik_ext.OptionParser(usage=usage, version=version)
        # mypy: "OptionParser" has no attribute "options_manager"
        # dynamic attribute?
        self.cmdline_parser.options_manager = self  # type: ignore
        self._optik_option_attrs = set(self.cmdline_parser.option_class.ATTRS)

    def register_options_provider(
        self, provider: "ConfigurationMixIn", own_group: bool = True
    ) -> None:
        """register an options provider"""
        assert provider.priority <= 0, "provider's priority can't be >= 0"
        for i in range(len(self.options_providers)):
            if provider.priority > self.options_providers[i].priority:
                self.options_providers.insert(i, provider)
                break
        else:
            self.options_providers.append(provider)

        # mypy: Need type annotation for 'option'
        # you can't type variable of a list comprehension, right?
        non_group_spec_options: List = [
            option for option in provider.options if "group" not in option[1]  # type: ignore
        ]  # type: ignore

        groups = getattr(provider, "option_groups", ())
        if own_group and non_group_spec_options:
            self.add_option_group(
                provider.name.upper(), provider.__doc__, non_group_spec_options, provider
            )
        else:
            for opt, optdict in non_group_spec_options:
                self.add_optik_option(provider, self.cmdline_parser, opt, optdict)
        for gname, gdoc in groups:
            gname = gname.upper()

            # mypy: Need type annotation for 'option'
            # you can't type variable of a list comprehension, right?
            goptions: List = [
                option
                for option in provider.options  # type: ignore
                if option[1].get("group", "").upper() == gname
            ]  # type: ignore
            self.add_option_group(gname, gdoc, goptions, provider)

    def add_option_group(
        self,
        group_name: str,
        doc: Optional[str],
        options: Union[List[Tuple[str, Dict[str, Any]]], List[Tuple[str, Dict[str, str]]]],
        provider: "ConfigurationMixIn",
    ) -> None:
        """add an option group including the listed options"""
        assert options
        # add option group to the command line parser
        if group_name in self._mygroups:
            group = self._mygroups[group_name]
        else:
            group = optik_ext.OptionGroup(self.cmdline_parser, title=group_name.capitalize())
            self.cmdline_parser.add_option_group(group)
            # mypy: "OptionGroup" has no attribute "level"
            # dynamic attribute
            group.level = provider.level  # type: ignore
            self._mygroups[group_name] = group
            # add section to the config file
            if group_name != "DEFAULT":
                self.cfgfile_parser.add_section(group_name)
        # add provider's specific options
        for opt, optdict in options:
            self.add_optik_option(provider, group, opt, optdict)

    def add_optik_option(
        self,
        provider: "ConfigurationMixIn",
        optikcontainer: Union[OptionParser, OptionGroup],
        opt: str,
        optdict: Dict[str, Any],
    ) -> None:
        if "inputlevel" in optdict:
            warn(
                '[0.50] "inputlevel" in option dictionary for %s is deprecated,'
                ' use "level"' % opt,
                DeprecationWarning,
            )
            optdict["level"] = optdict.pop("inputlevel")
        args, optdict = self.optik_option(provider, opt, optdict)
        option = optikcontainer.add_option(*args, **optdict)
        self._all_options[opt] = provider
        self._maxlevel = max(self._maxlevel, option.level or 0)

    def optik_option(
        self, provider: "ConfigurationMixIn", opt: str, optdict: Dict[str, Any]
    ) -> Tuple[List[str], Dict[str, Any]]:
        """get our personal option definition and return a suitable form for
        use with optik/optparse
        """
        optdict = copy(optdict)
        if "action" in optdict:
            self._nocallback_options[provider] = opt
        else:
            optdict["action"] = "callback"
            optdict["callback"] = self.cb_set_provider_option
        # default is handled here and *must not* be given to optik if you
        # want the whole machinery to work
        if "default" in optdict:
            if (
                "help" in optdict
                and optdict.get("default") is not None
                and not optdict["action"] in ("store_true", "store_false")
            ):
                optdict["help"] += " [current: %default]"
            del optdict["default"]
        args = ["--" + str(opt)]
        if "short" in optdict:
            self._short_options[optdict["short"]] = opt
            args.append("-" + optdict["short"])
            del optdict["short"]
        # cleanup option definition dict before giving it to optik
        for key in list(optdict.keys()):
            if key not in self._optik_option_attrs:
                optdict.pop(key)
        return args, optdict

    def cb_set_provider_option(
        self, option: "Option", opt: str, value: Union[List[str], int, str], parser: "OptionParser"
    ) -> None:
        """optik callback for option setting"""
        if opt.startswith("--"):
            # remove -- on long option
            opt = opt[2:]
        else:
            # short option, get its long equivalent
            opt = self._short_options[opt[1:]]
        # trick since we can't set action='store_true' on options
        if value is None:
            value = 1
        self.global_set_option(opt, value)

    def global_set_option(self, opt: str, value: Union[List[str], int, str]) -> None:
        """set option on the correct option provider"""
        self._all_options[opt].set_option(opt, value)

    def generate_config(
        self,
        stream: Union[StringIO, TextIOWrapper] = None,
        skipsections: Tuple[()] = (),
        encoding: Optional[Any] = None,
    ) -> None:
        """write a configuration file according to the current configuration
        into the given stream or stdout
        """
        options_by_section: Dict[Any, List] = {}
        sections = []

        for provider in self.options_providers:
            for section, options in provider.options_by_section():
                if section is None:
                    section = provider.name
                if section in skipsections:
                    continue
                options = [(n, d, v) for (n, d, v) in options if d.get("type") is not None]
                if not options:
                    continue
                if section not in sections:
                    sections.append(section)
                alloptions = options_by_section.setdefault(section, [])
                alloptions += options
        stream = stream or sys.stdout
        encoding = _get_encoding(encoding, stream)
        printed = False
        for section in sections:
            if printed:
                print("\n", file=stream)
            format_section(stream, section.upper(), options_by_section[section], encoding)
            printed = True

    def generate_manpage(
        self, pkginfo: attrdict, section: int = 1, stream: StringIO = None
    ) -> None:
        """write a man page for the current configuration into the given
        stream or stdout
        """
        self._monkeypatch_expand_default()
        try:
            optik_ext.generate_manpage(
                self.cmdline_parser,
                pkginfo,
                section,
                stream=stream or sys.stdout,
                level=self._maxlevel,
            )
        finally:
            self._unmonkeypatch_expand_default()

    # initialization methods ##################################################

    def load_provider_defaults(self) -> None:
        """initialize configuration using default values"""
        for provider in self.options_providers:
            provider.load_defaults()

    def load_file_configuration(self, config_file: str = None) -> None:
        """load the configuration from file"""
        self.read_config_file(config_file)
        self.load_config_file()

    def read_config_file(self, config_file: str = None) -> None:
        """read the configuration file but do not load it (i.e. dispatching
        values to each options provider)
        """
        helplevel = 1
        while helplevel <= self._maxlevel:
            opt = "-".join(["long"] * helplevel) + "-help"
            if opt in self._all_options:
                break  # already processed

            def helpfunc(option, opt, val, p, level=helplevel):
                print(self.help(level))
                sys.exit(0)

            helpmsg = "%s verbose help." % " ".join(["more"] * helplevel)
            optdict = {"action": "callback", "callback": helpfunc, "help": helpmsg}
            provider = self.options_providers[0]
            self.add_optik_option(provider, self.cmdline_parser, opt, optdict)
            provider.options += ((opt, optdict),)
            helplevel += 1
        if config_file is None:
            config_file = self.config_file
        if config_file is not None:
            config_file = expanduser(config_file)
        if config_file and exists(config_file):
            parser = self.cfgfile_parser
            parser.read([config_file])
            # normalize sections'title
            # mypy: "ConfigParser" has no attribute "_sections"
            # dynamic attribute?
            for sect, values in list(parser._sections.items()):  # type: ignore
                if not sect.isupper() and values:
                    parser._sections[sect.upper()] = values  # type: ignore
        elif not self.quiet:
            msg = "No config file found, using default configuration"
            print(msg, file=sys.stderr)
            return

    def input_config(self, onlysection=None, inputlevel=0, stream=None):
        """interactively get configuration values by asking to the user and generate
        a configuration file
        """
        if onlysection is not None:
            onlysection = onlysection.upper()
        for provider in self.options_providers:
            for section, option, optdict in provider.all_options():
                if onlysection is not None and section != onlysection:
                    continue
                if "type" not in optdict:
                    # ignore action without type (callback, store_true...)
                    continue
                provider.input_option(option, optdict, inputlevel)
        # now we can generate the configuration file
        if stream is not None:
            self.generate_config(stream)

    def load_config_file(self) -> None:
        """dispatch values previously read from a configuration file to each
        options provider)
        """
        parser = self.cfgfile_parser
        for section in parser.sections():
            for option, value in parser.items(section):
                try:
                    self.global_set_option(option, value)
                except (KeyError, OptionError):
                    # TODO handle here undeclared options appearing in the config file
                    continue

    def load_configuration(self, **kwargs: Any) -> None:
        """override configuration according to given parameters"""
        for opt, opt_value in kwargs.items():
            opt = opt.replace("_", "-")
            provider = self._all_options[opt]
            provider.set_option(opt, opt_value)

    def load_command_line_configuration(self, args: List[str] = None) -> List[str]:
        """override configuration according to command line parameters

        return additional arguments
        """
        self._monkeypatch_expand_default()

        try:
            if args is None:
                args = sys.argv[1:]
            else:
                args = list(args)
            (options, args) = self.cmdline_parser.parse_args(args=args)
            for provider in self._nocallback_options.keys():
                config = provider.config
                for attr in config.__dict__.keys():
                    value = getattr(options, attr, None)
                    if value is None:
                        continue
                    setattr(config, attr, value)
            return args
        finally:
            self._unmonkeypatch_expand_default()

    # help methods ############################################################

    def add_help_section(self, title: str, description: str, level: int = 0) -> None:
        """add a dummy option section for help purpose """
        group = optik_ext.OptionGroup(
            self.cmdline_parser, title=title.capitalize(), description=description
        )
        # mypy: "OptionGroup" has no attribute "level"
        # it does, it is set in the optik_ext module
        group.level = level  # type: ignore
        self._maxlevel = max(self._maxlevel, level)
        self.cmdline_parser.add_option_group(group)

    def _monkeypatch_expand_default(self) -> None:
        # monkey patch optik_ext to deal with our default values
        try:
            self.__expand_default_backup = optik_ext.HelpFormatter.expand_default
            # mypy: Cannot assign to a method
            # it's dirty but you can
            optik_ext.HelpFormatter.expand_default = expand_default  # type: ignore
        except AttributeError:
            # python < 2.4: nothing to be done
            pass

    def _unmonkeypatch_expand_default(self) -> None:
        # remove monkey patch
        if hasattr(optik_ext.HelpFormatter, "expand_default"):
            # mypy: Cannot assign to a method
            # it's dirty but you can

            # unpatch optik_ext to avoid side effects
            optik_ext.HelpFormatter.expand_default = self.__expand_default_backup  # type: ignore

    def help(self, level: int = 0) -> str:
        """return the usage string for available options """
        # mypy: "HelpFormatter" has no attribute "output_level"
        # set in optik_ext
        self.cmdline_parser.formatter.output_level = level  # type: ignore
        self._monkeypatch_expand_default()
        try:
            return self.cmdline_parser.format_help()
        finally:
            self._unmonkeypatch_expand_default()


class Method(object):
    """used to ease late binding of default method (so you can define options
    on the class using default methods on the configuration instance)
    """

    def __init__(self, methname):
        self.method = methname
        self._inst = None

    def bind(self, instance: "Configuration") -> None:
        """bind the method to its instance"""
        if self._inst is None:
            self._inst = instance

    def __call__(self, *args: Any, **kwargs: Any) -> Dict[str, str]:
        assert self._inst, "unbound method"
        return getattr(self._inst, self.method)(*args, **kwargs)


# Options Provider #############################################################


class OptionsProviderMixIn(object):
    """Mixin to provide options to an OptionsManager"""

    # those attributes should be overridden
    priority = -1
    name = "default"
    options: Tuple = ()
    level = 0

    def __init__(self) -> None:
        self.config = optik_ext.Values()
        for option_tuple in self.options:
            try:
                option, optdict = option_tuple
            except ValueError:
                raise Exception("Bad option: %s" % str(option_tuple))
            if isinstance(optdict.get("default"), Method):
                optdict["default"].bind(self)
            elif isinstance(optdict.get("callback"), Method):
                optdict["callback"].bind(self)
        self.load_defaults()

    def load_defaults(self) -> None:
        """initialize the provider using default values"""
        for opt, optdict in self.options:
            action = optdict.get("action")
            if action != "callback":
                # callback action have no default
                default = self.option_default(opt, optdict)
                if default is REQUIRED:
                    continue
                self.set_option(opt, default, action, optdict)

    def option_default(self, opt, optdict=None):
        """return the default value for an option"""
        if optdict is None:
            optdict = self.get_option_def(opt)
        default = optdict.get("default")
        if callable(default):
            default = default()
        return default

    def option_attrname(self, opt, optdict=None):
        """get the config attribute corresponding to opt"""
        if optdict is None:
            optdict = self.get_option_def(opt)
        return optdict.get("dest", opt.replace("-", "_"))

    option_name = callable_deprecated(
        "[0.60] OptionsProviderMixIn.option_name() was renamed to option_attrname()"
    )(option_attrname)

    def option_value(self, opt):
        """get the current value for the given option"""
        return getattr(self.config, self.option_attrname(opt), None)

    def set_option(self, opt, value, action=None, optdict=None):
        """method called to set an option (registered in the options list)"""
        if optdict is None:
            optdict = self.get_option_def(opt)
        if value is not None:
            value = _validate(value, optdict, opt)
        if action is None:
            action = optdict.get("action", "store")
        if optdict.get("type") == "named":  # XXX need specific handling
            optname = self.option_attrname(opt, optdict)
            currentvalue = getattr(self.config, optname, None)
            if currentvalue:
                currentvalue.update(value)
                value = currentvalue
        if action == "store":
            setattr(self.config, self.option_attrname(opt, optdict), value)
        elif action in ("store_true", "count"):
            setattr(self.config, self.option_attrname(opt, optdict), 0)
        elif action == "store_false":
            setattr(self.config, self.option_attrname(opt, optdict), 1)
        elif action == "append":
            opt = self.option_attrname(opt, optdict)
            _list = getattr(self.config, opt, None)
            if _list is None:
                if isinstance(value, (list, tuple)):
                    _list = value
                elif value is not None:
                    _list = []
                    _list.append(value)
                setattr(self.config, opt, _list)
            elif isinstance(_list, tuple):
                setattr(self.config, opt, _list + (value,))
            else:
                _list.append(value)
        elif action == "callback":
            optdict["callback"](None, opt, value, None)
        else:
            raise UnsupportedAction(action)

    def input_option(self, option, optdict, inputlevel=99):
        default = self.option_default(option, optdict)
        if default is REQUIRED:
            defaultstr = "(required): "
        elif optdict.get("level", 0) > inputlevel:
            return
        elif optdict["type"] == "password" or default is None:
            defaultstr = ": "
        else:
            defaultstr = "(default: %s): " % format_option_value(optdict, default)
        print(":%s:" % option)
        print(optdict.get("help") or option)
        inputfunc = INPUT_FUNCTIONS[optdict["type"]]
        value = inputfunc(optdict, defaultstr)
        while default is REQUIRED and not value:
            print("please specify a value")
            value = inputfunc(optdict, "%s: " % option)
        if value is None and default is not None:
            value = default
        self.set_option(option, value, optdict=optdict)

    def get_option_def(self, opt):
        """return the dictionary defining an option given it's name"""
        assert self.options
        for option in self.options:
            if option[0] == opt:
                return option[1]
        # mypy: Argument 2 to "OptionError" has incompatible type "str"; expected "Option"
        # seems to be working?
        raise OptionError("no such option %s in section %r" % (opt, self.name), opt)  # type: ignore

    def all_options(self):
        """return an iterator on available options for this provider
        option are actually described by a 3-uple:
        (section, option name, option dictionary)
        """
        for section, options in self.options_by_section():
            if section is None:
                if self.name is None:
                    continue
                section = self.name.upper()
            for option, optiondict, value in options:
                yield section, option, optiondict

    def options_by_section(self) -> Iterator[Any]:
        """return an iterator on options grouped by section

        (section, [list of (optname, optdict, optvalue)])
        """
        sections: Dict[str, List[Tuple[str, Dict[str, Any], Any]]] = {}
        for optname, optdict in self.options:
            sections.setdefault(optdict.get("group"), []).append(
                (optname, optdict, self.option_value(optname))
            )
        if None in sections:
            # mypy: No overload variant of "pop" of "MutableMapping" matches argument type "None"
            # it actually works
            yield None, sections.pop(None)  # type: ignore
        for section, options in sorted(sections.items()):
            yield section.upper(), options

    def options_and_values(self, options=None):
        if options is None:
            options = self.options
        for optname, optdict in options:
            yield (optname, optdict, self.option_value(optname))


# configuration ################################################################


class ConfigurationMixIn(OptionsManagerMixIn, OptionsProviderMixIn):
    """basic mixin for simple configurations which don't need the
    manager / providers model
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not args:
            kwargs.setdefault("usage", "")
        kwargs.setdefault("quiet", 1)
        OptionsManagerMixIn.__init__(self, *args, **kwargs)
        OptionsProviderMixIn.__init__(self)
        if not getattr(self, "option_groups", None):
            self.option_groups: List[Tuple[Any, str]] = []
            for option, optdict in self.options:
                try:
                    gdef = (optdict["group"].upper(), "")
                except KeyError:
                    continue
                if gdef not in self.option_groups:
                    self.option_groups.append(gdef)
        self.register_options_provider(self, own_group=False)

    def register_options(self, options):
        """add some options to the configuration"""
        options_by_group = {}
        for optname, optdict in options:
            options_by_group.setdefault(optdict.get("group", self.name.upper()), []).append(
                (optname, optdict)
            )
        for group, group_options in options_by_group.items():
            self.add_option_group(group, None, group_options, self)
        self.options += tuple(options)

    def load_defaults(self):
        OptionsProviderMixIn.load_defaults(self)

    def __iter__(self):
        return iter(self.config.__dict__.items())

    def __getitem__(self, key):
        try:
            return getattr(self.config, self.option_attrname(key))
        except (optik_ext.OptionValueError, AttributeError):
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.set_option(key, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except (OptionError, KeyError):
            return default


class Configuration(ConfigurationMixIn):
    """class for simple configurations which don't need the
    manager / providers model and prefer delegation to inheritance

    configuration values are accessible through a dict like interface
    """

    def __init__(
        self, config_file=None, options=None, name=None, usage=None, doc=None, version=None
    ):
        if options is not None:
            self.options = options
        if name is not None:
            self.name = name
        if doc is not None:
            self.__doc__ = doc
        super(Configuration, self).__init__(config_file=config_file, usage=usage, version=version)


class OptionsManager2ConfigurationAdapter(object):
    """Adapt an option manager to behave like a
    `logilab.common.configuration.Configuration` instance
    """

    def __init__(self, provider):
        self.config = provider

    def __getattr__(self, key):
        return getattr(self.config, key)

    def __getitem__(self, key):
        provider = self.config._all_options[key]
        try:
            return getattr(provider.config, provider.option_attrname(key))
        except AttributeError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        self.config.global_set_option(self.config.option_attrname(key), value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


# other functions ##############################################################


def read_old_config(newconfig, changes, configfile):
    """initialize newconfig from a deprecated configuration file

    possible changes:
    * ('renamed', oldname, newname)
    * ('moved', option, oldgroup, newgroup)
    * ('typechanged', option, oldtype, newvalue)
    """
    # build an index of changes
    changesindex = {}
    for action in changes:
        if action[0] == "moved":
            option, oldgroup, newgroup = action[1:]
            changesindex.setdefault(option, []).append((action[0], oldgroup, newgroup))
            continue
        if action[0] == "renamed":
            oldname, newname = action[1:]
            changesindex.setdefault(newname, []).append((action[0], oldname))
            continue
        if action[0] == "typechanged":
            option, oldtype, newvalue = action[1:]
            changesindex.setdefault(option, []).append((action[0], oldtype, newvalue))
            continue
        if action[0] in ("added", "removed"):
            continue  # nothing to do here
        raise Exception("unknown change %s" % action[0])
    # build a config object able to read the old config
    options = []
    for optname, optdef in newconfig.options:
        for action in changesindex.pop(optname, ()):
            if action[0] == "moved":
                oldgroup, newgroup = action[1:]
                optdef = optdef.copy()
                optdef["group"] = oldgroup
            elif action[0] == "renamed":
                optname = action[1]
            elif action[0] == "typechanged":
                oldtype = action[1]
                optdef = optdef.copy()
                optdef["type"] = oldtype
        options.append((optname, optdef))
    if changesindex:
        raise Exception("unapplied changes: %s" % changesindex)
    oldconfig = Configuration(options=options, name=newconfig.name)
    # read the old config
    oldconfig.load_file_configuration(configfile)
    # apply values reverting changes
    changes.reverse()
    done = set()
    for action in changes:
        if action[0] == "renamed":
            oldname, newname = action[1:]
            newconfig[newname] = oldconfig[oldname]
            done.add(newname)
        elif action[0] == "typechanged":
            optname, oldtype, newvalue = action[1:]
            newconfig[optname] = newvalue
            done.add(optname)
    for optname, optdef in newconfig.options:
        if optdef.get("type") and optname not in done:
            newconfig.set_option(optname, oldconfig[optname], optdict=optdef)


def merge_options(options, optgroup=None):
    """preprocess a list of options and remove duplicates, returning a new list
    (tuple actually) of options.

    Options dictionaries are copied to avoid later side-effect. Also, if
    `otpgroup` argument is specified, ensure all options are in the given group.
    """
    alloptions = {}
    options = list(options)
    for i in range(len(options) - 1, -1, -1):
        optname, optdict = options[i]
        if optname in alloptions:
            options.pop(i)
            alloptions[optname].update(optdict)
        else:
            optdict = optdict.copy()
            options[i] = (optname, optdict)
            alloptions[optname] = optdict
        if optgroup is not None:
            alloptions[optname]["group"] = optgroup
    return tuple(options)
