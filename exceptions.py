#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class UnknownCommand(Exception):
    """An Exception that is raised on an invalid command."""

    def __init__(self, command):
        super(UnknownCommand,
              self).__init__('Unknown command: {!r}'.format(command))
