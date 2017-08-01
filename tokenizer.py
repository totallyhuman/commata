#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import re

import exceptions
import functions


def tokenize(code):
    """Splits the code into tokens.

    Positional arguments:
        code (str): the code to be tokenized

    Returns:
        tokens (list): a list of all the tokens in the code
    """
    Token = collections.namedtuple('Token', ['type', 'value'])

    token_specs = [
        ('char', r'\'([^\\]|\\[\s\S])'),
        ('string', r'"([^\\]|\\[\s\S])+"'),
        ('unclosed_string', r'"([^\\]|\\[\s\S])+$'),
        ('comment', r'###.*\n'),
        ('number', r'-?\d+(\.\d*)?'),
        ('noop', r'[ \t\n]+'),
        ('command', r'.')
    ]
    token_regex = '|'.join(r'(?P<{}>{})'.format(*i) for i in token_specs)
    tokens = []

    for token in re.finditer(token_regex, code):
        _type = token.lastgroup
        value = token.group(_type)

        if _type == 'noop' or _type == 'comment':
            pass
        elif _type == 'command':
            if value in functions.commands:
                tokens.append(Token(_type, value))
            else:
                raise exceptions.UnknownCommand(value)
        else:
            tokens.append(Token(_type, value))

    return tokens
