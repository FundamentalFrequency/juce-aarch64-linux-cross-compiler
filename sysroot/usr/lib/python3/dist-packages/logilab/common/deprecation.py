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
"""Deprecation utilities."""

__docformat__ = "restructuredtext en"

import os
import sys
from enum import Enum
from warnings import warn
from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES
from typing import Any, Callable, Dict, Optional, Type
from typing_extensions import Protocol


def get_real__name__(some_callable: Callable) -> str:
    """
    This is another super edge magic case which is needed because we uses
    lazy_wraps because of logilab.common.modutils.LazyObject and because
    __name__ has special behavior and doesn't work like a normal attribute and
    that __getattribute__ of lazy_wraps is bypassed.

    Therefor, to get the real callable name when several lazy_wrapped
    decorator are used we need to travers the __wrapped__ attributes chain.
    """

    targeted_callable = some_callable
    while hasattr(targeted_callable, "__wrapped__"):
        targeted_callable = targeted_callable.__wrapped__  # type: ignore

    return targeted_callable.__name__


def lazy_wraps(wrapped: Callable) -> Callable:
    """
    This is the equivalent of the @wraps decorator of functools except it won't
    try to grabs attributes of the targeted function on decoration but on access.

    This is needed because of logilab.common.modutils.LazyObject.

    Indeed: if you try to decorate a LazyObject with @wraps, wraps will try to
    access attributes of LazyObject and this will trigger the attempt to import
    the module decorated by LazyObject which you don't want to do when you just
    want to mark this LazyObject has been a deprecated objet that you only
    wants to trigger if the user try to use it.

    Usage: like @wraps()

    >>> @lazy_wraps(function)
    >>> def wrapper(*args, **kwargs): ...
    """

    def update_wrapper_attributes(wrapper: Callable) -> Callable:
        def __getattribute__(self, attribute: str) -> Any:
            if attribute in WRAPPER_ASSIGNMENTS:
                return getattr(wrapped, attribute)

            return super(self.__class__, self).__getattribute__(attribute)

        wrapper.__getattribute__ = __getattribute__  # type: ignore

        for attribute in WRAPPER_UPDATES:
            getattr(wrapper, attribute).update(getattr(wrapped, attribute, {}))

        wrapper.__wrapped__ = wrapped  # type: ignore

        return wrapper

    return update_wrapper_attributes


class DeprecationWrapper(object):
    """proxy to print a warning on access to any attribute of the wrapped object"""

    def __init__(
        self, proxied: Any, msg: Optional[str] = None, version: Optional[str] = None
    ) -> None:
        self._proxied: Any = proxied
        self._msg: str = msg if msg else ""
        self.version: Optional[str] = version

    def __getattr__(self, attr: str) -> Any:
        send_warning(
            self._msg,
            deprecation_class=DeprecationWarning,
            deprecation_class_kwargs={},
            stacklevel=3,
            version=self.version,
        )
        return getattr(self._proxied, attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        if attr in ("_proxied", "_msg"):
            self.__dict__[attr] = value
        else:
            send_warning(
                self._msg,
                deprecation_class=DeprecationWarning,
                deprecation_class_kwargs={},
                stacklevel=3,
                version=self.version,
            )
            setattr(self._proxied, attr, value)


def _get_module_name(number: int = 1) -> str:
    """
    automagically try to determine the package name from which the warning has
    been triggered by loop other calling frames.

    If it fails to do so, return an empty string.
    """

    frame = sys._getframe()

    for i in range(number + 1):
        if frame.f_back is None:
            break

        frame = frame.f_back

    if frame.f_globals["__package__"]:
        return frame.f_globals["__package__"]

    file_name = os.path.split(frame.f_globals["__file__"])[1]

    if file_name.endswith(".py"):
        file_name = file_name[: -len(".py")]

    return file_name


def send_warning(
    reason: str,
    deprecation_class: Type[DeprecationWarning],
    deprecation_class_kwargs: Dict[str, Any],
    version: Optional[str] = None,
    stacklevel: int = 2,
    module_name: Optional[str] = None,
) -> None:
    """Display a deprecation message only if the version is older than the
    compatible version.
    """
    if module_name and version:
        reason = "[%s %s] %s" % (module_name, version, reason)
    elif module_name:
        reason = "[%s] %s" % (module_name, reason)
    elif version:
        reason = "[%s] %s" % (version, reason)

    warn(
        deprecation_class(reason, **deprecation_class_kwargs), stacklevel=stacklevel  # type: ignore
    )


class DeprecationWarningKind(Enum):
    ARGUMENT = "argument"
    ATTRIBUTE = "attribute"
    CALLABLE = "callable"
    CLASS = "class"
    MODULE = "module"


class DeprecationWarningOperation(Enum):
    DEPRECATED = "deprecated"
    MOVED = "moved"
    REMOVED = "removed"
    RENAMED = "renamed"


class StructuredDeprecationWarning(DeprecationWarning):
    """
    Base class for all structured DeprecationWarning
    Mostly used with isinstance
    """

    def __init__(self, reason: str):
        self.reason: str = reason

    def __str__(self) -> str:
        return self.reason


class TargetRenamedDeprecationWarning(StructuredDeprecationWarning):
    def __init__(self, reason: str, kind: DeprecationWarningKind, old_name: str, new_name: str):
        super().__init__(reason)
        self.operation = DeprecationWarningOperation.RENAMED
        self.kind: DeprecationWarningKind = kind  # callable, class, module, argument, attribute
        self.old_name: str = old_name
        self.new_name: str = new_name


class TargetDeprecatedDeprecationWarning(StructuredDeprecationWarning):
    def __init__(self, reason: str, kind: DeprecationWarningKind):
        super().__init__(reason)
        self.operation = DeprecationWarningOperation.DEPRECATED
        self.kind: DeprecationWarningKind = kind  # callable, class, module, argument, attribute


class TargetRemovedDeprecationWarning(StructuredDeprecationWarning):
    def __init__(self, reason: str, kind: DeprecationWarningKind, name: str):
        super().__init__(reason)
        self.operation = DeprecationWarningOperation.REMOVED
        self.kind: DeprecationWarningKind = kind  # callable, class, module, argument, attribute
        self.name: str = name


class TargetMovedDeprecationWarning(StructuredDeprecationWarning):
    def __init__(
        self,
        reason: str,
        kind: DeprecationWarningKind,
        old_name: str,
        new_name: str,
        old_module: str,
        new_module: str,
    ):
        super().__init__(reason)
        self.operation = DeprecationWarningOperation.MOVED
        self.kind: DeprecationWarningKind = kind  # callable, class, module, argument, attribute
        self.old_name: str = old_name
        self.new_name: str = new_name
        self.old_module: str = old_module
        self.new_module: str = new_module


def callable_renamed(
    old_name: str, new_function: Callable, version: Optional[str] = None
) -> Callable:
    """use to tell that a callable has been renamed.

    It returns a callable wrapper, so that when its called a warning is printed
    telling what is the object new name.

    >>> old_function = renamed('old_function', new_function)
    >>> old_function()
    sample.py:57: DeprecationWarning: old_function has been renamed and is deprecated, uses
    new_function instead old_function()
    >>>
    """

    @lazy_wraps(new_function)
    def wrapped(*args, **kwargs):
        send_warning(
            (
                f"{old_name} has been renamed and is deprecated, uses "
                f"{get_real__name__(new_function)} instead"
            ),
            TargetRenamedDeprecationWarning,
            deprecation_class_kwargs={
                "kind": DeprecationWarningKind.CALLABLE,
                "old_name": old_name,
                "new_name": get_real__name__(new_function),
            },
            stacklevel=3,
            version=version,
            module_name=new_function.__module__,
        )
        return new_function(*args, **kwargs)

    return wrapped


renamed: Callable[[str, Callable, Optional[str]], Callable] = callable_renamed(
    old_name="renamed", new_function=callable_renamed
)


def argument_removed(old_argument_name: str, version: Optional[str] = None) -> Callable:
    """
    callable decorator to allow getting backward compatibility for renamed keyword arguments.

    >>> @argument_removed("old")
    ... def some_function(new):
    ...     return new
    >>> some_function(old=42)
    sample.py:15: DeprecationWarning: argument old of callable some_function has been renamed and
    is deprecated, use keyword argument new instead some_function(old=42)
    42
    """

    def _wrap(func: Callable) -> Callable:
        @lazy_wraps(func)
        def check_kwargs(*args, **kwargs):
            if old_argument_name in kwargs:
                send_warning(
                    f"argument {old_argument_name} of callable {get_real__name__(func)} has been "
                    f"removed and is deprecated",
                    deprecation_class=TargetRemovedDeprecationWarning,
                    deprecation_class_kwargs={
                        "kind": DeprecationWarningKind.ARGUMENT,
                        "name": old_argument_name,
                    },
                    stacklevel=3,
                    version=version,
                    module_name=func.__module__,
                )
                del kwargs[old_argument_name]

            return func(*args, **kwargs)

        return check_kwargs

    return _wrap


@argument_removed("name")
@argument_removed("doc")
def callable_deprecated(
    reason: Optional[str] = None, version: Optional[str] = None, stacklevel: int = 2
) -> Callable:
    """Display a deprecation message only if the version is older than the
    compatible version.
    """

    def decorator(func: Callable) -> Callable:
        @lazy_wraps(func)
        def wrapped(*args, **kwargs) -> Callable:
            message: str = reason or 'The function "%s" is deprecated'
            if "%s" in message:
                message %= get_real__name__(func)

            send_warning(
                message,
                TargetDeprecatedDeprecationWarning,
                {"kind": DeprecationWarningKind.CALLABLE},
                version,
                stacklevel + 1,
                module_name=func.__module__,
            )
            return func(*args, **kwargs)

        return wrapped

    return decorator


class CallableDeprecatedCallable(Protocol):
    def __call__(
        self, reason: Optional[str] = None, version: Optional[str] = None, stacklevel: int = 2
    ) -> Callable:
        ...


deprecated: CallableDeprecatedCallable = callable_renamed(
    old_name="deprecated", new_function=callable_deprecated
)


def _generate_class_deprecated():
    class _class_deprecated(type):
        """metaclass to print a warning on instantiation of a deprecated class"""

        def __call__(cls, *args, **kwargs):
            message = getattr(cls, "__deprecation_warning__", "%(cls)s is deprecated") % {
                "cls": cls.__name__
            }
            send_warning(
                message,
                deprecation_class=getattr(
                    cls, "__deprecation_warning_class__", TargetDeprecatedDeprecationWarning
                ),
                deprecation_class_kwargs=getattr(
                    cls,
                    "__deprecation_warning_class_kwargs__",
                    {"kind": DeprecationWarningKind.CLASS},
                ),
                module_name=getattr(
                    cls, "__deprecation_warning_module_name__", _get_module_name(1)
                ),
                stacklevel=getattr(cls, "__deprecation_warning_stacklevel__", 3),
                version=getattr(cls, "__deprecation_warning_version__", None),
            )
            return type.__call__(cls, *args, **kwargs)

    return _class_deprecated


class_deprecated = _generate_class_deprecated()


def attribute_renamed(old_name: str, new_name: str, version: Optional[str] = None) -> Callable:
    """
    class decorator to allow getting backward compatibility for renamed attributes.

    >>> @attribute_renamed(old_name="old", new_name="new")
    ... class SomeClass:
    ...     def __init__(self):
    ...         self.new = 42

    >>> some_class = SomeClass()
    >>> print(some_class.old)
    sample.py:15: DeprecationWarning: SomeClass.old has been renamed and is deprecated, use
    SomeClass.new instead
      print(some_class.old)
    42
    >>> some_class.old = 43
    sample.py:16: DeprecationWarning: SomeClass.old has been renamed and is deprecated, use
    SomeClass.new instead
      some_class.old = 43
    >>> some_class.old == some_class.new
    True
    """

    def _class_wrap(klass: type) -> type:
        reason = (
            f"{klass.__name__}.{old_name} has been renamed and is deprecated, use "
            f"{klass.__name__}.{new_name} instead"
        )

        def _get_old(self) -> Any:
            send_warning(
                reason,
                deprecation_class=TargetRenamedDeprecationWarning,
                deprecation_class_kwargs={
                    "kind": DeprecationWarningKind.ATTRIBUTE,
                    "old_name": old_name,
                    "new_name": new_name,
                },
                stacklevel=3,
                version=version,
                module_name=klass.__module__,
            )
            return getattr(self, new_name)

        def _set_old(self, value) -> None:
            send_warning(
                reason,
                deprecation_class=TargetRenamedDeprecationWarning,
                deprecation_class_kwargs={
                    "kind": DeprecationWarningKind.ATTRIBUTE,
                    "old_name": old_name,
                    "new_name": new_name,
                },
                stacklevel=3,
                version=version,
                module_name=klass.__module__,
            )
            setattr(self, new_name, value)

        def _del_old(self):
            send_warning(
                reason,
                deprecation_class=TargetRenamedDeprecationWarning,
                deprecation_class_kwargs={
                    "kind": DeprecationWarningKind.ATTRIBUTE,
                    "old_name": old_name,
                    "new_name": new_name,
                },
                stacklevel=3,
                version=version,
                module_name=klass.__module__,
            )
            delattr(self, new_name)

        setattr(klass, old_name, property(_get_old, _set_old, _del_old))

        return klass

    return _class_wrap


def argument_renamed(old_name: str, new_name: str, version: Optional[str] = None) -> Callable:
    """
    callable decorator to allow getting backward compatibility for renamed keyword arguments.

    >>> @argument_renamed(old_name="old", new_name="new")
    ... def some_function(new):
    ...     return new
    >>> some_function(old=42)
    sample.py:15: DeprecationWarning: argument old of callable some_function has been renamed and
    is deprecated, use keyword argument new instead
      some_function(old=42)
    42
    """

    def _wrap(func: Callable) -> Callable:
        @lazy_wraps(func)
        def check_kwargs(*args, **kwargs) -> Callable:
            if old_name in kwargs and new_name in kwargs:
                raise ValueError(
                    f"argument {old_name} of callable {get_real__name__(func)} has been "
                    f"renamed to {new_name} but you are both using {old_name} and "
                    f"{new_name} has keyword arguments, only uses {new_name}"
                )

            if old_name in kwargs:
                send_warning(
                    f"argument {old_name} of callable {get_real__name__(func)} has been renamed "
                    f"and is deprecated, use keyword argument {new_name} instead",
                    deprecation_class=TargetRenamedDeprecationWarning,
                    deprecation_class_kwargs={
                        "kind": DeprecationWarningKind.ARGUMENT,
                        "old_name": old_name,
                        "new_name": new_name,
                    },
                    stacklevel=3,
                    version=version,
                    module_name=func.__module__,
                )
                kwargs[new_name] = kwargs[old_name]
                del kwargs[old_name]

            return func(*args, **kwargs)

        return check_kwargs

    return _wrap


@argument_renamed(old_name="modpath", new_name="module_path")
@argument_renamed(old_name="objname", new_name="object_name")
def callable_moved(
    module_name: str,
    object_name: str,
    version: Optional[str] = None,
    stacklevel: int = 2,
    new_name: Optional[str] = None,
) -> Callable:
    """use to tell that a callable has been moved to a new module.

    It returns a callable wrapper, so that when its called a warning is printed
    telling where the object can be found, import is done (and not before) and
    the actual object is called.

    NOTE: the usage is somewhat limited on classes since it will fail if the
    wrapper is use in a class ancestors list, use the `class_moved` function
    instead (which has no lazy import feature though).
    """
    # in case the callable has been renamed
    new_name = new_name if new_name is not None else object_name
    old_module = _get_module_name(3)

    message = "object %s.%s has been moved to %s.%s" % (
        old_module,
        object_name,
        module_name,
        object_name,
    )

    def callnew(*args, **kwargs):
        from logilab.common.modutils import load_module_from_name

        send_warning(
            message,
            deprecation_class=TargetMovedDeprecationWarning,
            deprecation_class_kwargs={
                "kind": DeprecationWarningKind.CALLABLE,
                "old_name": object_name,
                "new_name": new_name,
                "old_module": old_module,
                "new_module": module_name,
            },
            version=version,
            stacklevel=stacklevel + 1,
            module_name=old_module,
        )

        m = load_module_from_name(module_name)
        return getattr(m, object_name)(*args, **kwargs)

    return callnew


moved: Callable[[Optional[str], Optional[str], int], Callable] = callable_renamed(
    old_name="moved", new_function=callable_moved
)


def class_renamed(
    old_name: str,
    new_class: type,
    message: Optional[str] = None,
    version: Optional[str] = None,
    module_name: Optional[str] = None,
    deprecated_warning_class=TargetRenamedDeprecationWarning,
    deprecated_warning_kwargs=None,
) -> type:
    """automatically creates a class which fires a DeprecationWarning
    when instantiated.

    >>> Set = class_renamed('Set', set, 'Set is now replaced by set')
    >>> s = Set()
    sample.py:57: DeprecationWarning: Set is now replaced by set
    s = Set()
    >>>
    """
    class_dict: Dict[str, Any] = {}
    if message is None:
        message = "%s is deprecated, use %s instead" % (old_name, new_class.__name__)

    class_dict["__deprecation_warning__"] = message
    class_dict["__deprecation_warning_class__"] = deprecated_warning_class
    if deprecated_warning_kwargs is None:
        class_dict["__deprecation_warning_class_kwargs__"] = {
            "kind": DeprecationWarningKind.CLASS,
            "old_name": old_name,
            "new_name": new_class.__name__,
        }
    else:
        class_dict["__deprecation_warning_class_kwargs__"] = deprecated_warning_kwargs
    class_dict["__deprecation_warning_version__"] = version
    class_dict["__deprecation_warning_stacklevel__"] = 3

    if module_name:
        class_dict["__deprecation_warning_module_name__"] = module_name
    else:
        class_dict["__deprecation_warning_module_name__"] = _get_module_name(1)

    try:
        return class_deprecated(old_name, (new_class,), class_dict)
    except (NameError, TypeError):
        # in case of conflicting metaclass situation
        # mypy can't handle dynamic base classes https://github.com/python/mypy/issues/2477
        class DeprecatedClass(new_class):  # type: ignore
            def __init__(self, *args, **kwargs):
                msg = class_dict.get(
                    "__deprecation_warning__",
                    f"{old_name} is deprecated, use {new_class.__name__} instead",
                )
                send_warning(
                    msg,
                    deprecation_class=TargetRenamedDeprecationWarning,
                    deprecation_class_kwargs={
                        "kind": DeprecationWarningKind.CLASS,
                        "old_name": old_name,
                        "new_name": new_class.__name__,
                    },
                    stacklevel=class_dict.get("__deprecation_warning_stacklevel__", 3),
                    version=class_dict.get("__deprecation_warning_version__", None),
                )
                super(DeprecatedClass, self).__init__(*args, **kwargs)

        return DeprecatedClass


def class_moved(
    new_class: type,
    old_name: Optional[str] = None,
    message: Optional[str] = None,
    version: Optional[str] = None,
) -> type:
    """nice wrapper around class_renamed when a class has been moved into
    another module
    """
    if old_name is None:
        old_name = new_class.__name__

    old_module = _get_module_name(1)

    if message is None:
        message = "class %s.%s is now available as %s.%s" % (
            old_module,
            old_name,
            new_class.__module__,
            new_class.__name__,
        )

    module_name = _get_module_name(1)

    return class_renamed(
        old_name,
        new_class,
        message=message,
        module_name=module_name,
        deprecated_warning_class=TargetMovedDeprecationWarning,
        deprecated_warning_kwargs={
            "kind": DeprecationWarningKind.CLASS,
            "old_module": old_module,
            "new_module": new_class.__module__,
            "old_name": old_name,
            "new_name": new_class.__name__,
        },
    )
