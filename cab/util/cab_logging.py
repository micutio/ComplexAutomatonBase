"""
Logging module of the Complex Automaton Base.
Controls console output and enables output at different logging levels.
"""

import sys

from enum import Enum


class LogLevel(Enum):
    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5


current_log_lvl: LogLevel = 2


def trace(msg: str):
    if current_log_lvl >= LogLevel.TRACE:
        print('[trace  ]' + msg)


def debug(msg: str):
    if current_log_lvl >= LogLevel.DEBUG:
        print('[debug  ]' + msg)


def info(msg: str):
    if current_log_lvl >= LogLevel.INFO:
        print('[info   ]' + msg)


def warning(msg: str):
    if current_log_lvl >= LogLevel.WARNING:
        print('[warning]' + msg, file=sys.stderr)


def error(msg: str):
    if current_log_lvl >= LogLevel.ERROR:
        print('[error  ]' + msg, file=sys.stderr)


def fatal(msg: str):
    if current_log_lvl >= LogLevel.FATAL:
        print('[fatal  ]' + msg, file=sys.stderr)
