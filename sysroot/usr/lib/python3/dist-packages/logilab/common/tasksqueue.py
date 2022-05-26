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
"""Prioritized tasks queue"""

__docformat__ = "restructuredtext en"


from typing import Iterator, List
from bisect import insort_left
import queue

LOW = 0
MEDIUM = 10
HIGH = 100

PRIORITY = {
    "LOW": LOW,
    "MEDIUM": MEDIUM,
    "HIGH": HIGH,
}
REVERSE_PRIORITY = dict((values, key) for key, values in PRIORITY.items())


class PrioritizedTasksQueue(queue.Queue):
    def _init(self, maxsize: int) -> None:
        """Initialize the queue representation"""
        self.maxsize = maxsize
        # ordered list of task, from the lowest to the highest priority
        self.queue: List["Task"] = []  # type: ignore

    def _put(self, item: "Task") -> None:
        """Put a new item in the queue"""
        for i, task in enumerate(self.queue):
            # equivalent task
            if task == item:
                # if new task has a higher priority, remove the one already
                # queued so the new priority will be considered
                if task < item:
                    item.merge(task)
                    del self.queue[i]
                    break
                # else keep it so current order is kept
                task.merge(item)
                return
        insort_left(self.queue, item)

    def _get(self) -> "Task":
        """Get an item from the queue"""
        return self.queue.pop()

    def __iter__(self) -> Iterator["Task"]:
        return iter(self.queue)

    def remove(self, tid: str) -> None:
        """remove a specific task from the queue"""
        # XXX acquire lock
        for i, task in enumerate(self):
            if task.id == tid:
                self.queue.pop(i)
                return
        raise ValueError("not task of id %s in queue" % tid)


class Task:
    def __init__(self, tid: str, priority: int = LOW) -> None:
        # task id
        self.id = tid
        # task priority
        self.priority = priority

    def __repr__(self) -> str:
        return "<Task %s @%#x>" % (self.id, id(self))

    def __lt__(self, other: "Task") -> bool:
        return self.priority < other.priority

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and self.id == other.id

    __hash__ = object.__hash__

    def merge(self, other: "Task") -> None:
        pass
