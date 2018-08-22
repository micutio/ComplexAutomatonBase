"""
Logging module of the Complex Automaton Base.
Controls console output and enables output at different logging levels.
"""

import sys

from enum import Enum
from functools import total_ordering
from typing import Dict


@total_ordering
class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


log_db: Dict[str, LogLevel] = dict()
log_db['current'] = LogLevel.INFO


def set_log_trace():
    log_db['current'] = LogLevel.TRACE


def set_log_debug():
    log_db['current'] = LogLevel.DEBUG


def set_log_info():
    log_db['current'] = LogLevel.INFO


def set_log_warning():
    log_db['current'] = LogLevel.WARNING


def set_log_error():
    log_db['current'] = LogLevel.ERROR


def set_log_fatal():
    log_db['current'] = LogLevel.FATAL


def trace(msg: str):
    if log_db['current'] <= LogLevel.TRACE:
        print('[trace  ]' + msg)


def debug(msg: str):
    if log_db['current'] <= LogLevel.DEBUG:
        print('[debug  ]' + msg)


def info(msg: str):
    if log_db['current'] <= LogLevel.INFO:
        print('[info   ]' + msg)


def warning(msg: str):
    if log_db['current'] <= LogLevel.WARNING:
        print('[warning]' + msg, file=sys.stderr)


def error(msg: str):
    if log_db['current'] <= LogLevel.ERROR:
        print('[error  ]' + msg, file=sys.stderr)


def fatal(msg: str):
    if log_db['current'] <= LogLevel.FATAL:
        print('[fatal  ]' + msg, file=sys.stderr)
