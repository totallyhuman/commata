#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
,,, (Commata)

A language that probably hopefully does something.

Sumant Bhaskaruni
v0.2.0 (basically, don't use it)
"""

import argparse
import collections
import math
import re


def switch(stacks, stk_no, stack):
    a = stack.pop()
    b = stack.pop()

    stack.push(a)
    stack.push(b)


def sum_stack(stacks, stk_no, stack):
    if isinstance(stack.peek(), str):
        result = ''
        for i in range(len(stack)):
            result += str(stack.pop())
    else:
        result = 0
        for i in range(len(stack)):
            result += stack.pop()

    stack.push(result)

commands = {
    '+': # addition or concatenation
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) + stack.pop()),
    '-': # subtraction
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) - stack.pop()),
    '×': # multiplication or string multiplication
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) * stack.pop()),
    '÷': # division
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) / stack.pop()),
    '/': # integer division
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) // stack.pop()),
    '%': # modulo or string formatting
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) % stack.pop()),
    '*': # exponentiation
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) ** stack.pop()),
    '√': # square root
    lambda stacks, stk_no, stack: stack.push(math.sqrt(stack.pop())),
    '↓': # output
    lambda stacks, stk_no, stack: print(stack.pop(), end = ''),
    '↑': # pop
    lambda stacks, stk_no, stack: stack.pop(),
    '¬': # logical NOT
    lambda stacks, stk_no, stack: stack.push(int(not stack.pop())),
    '∧': # logical AND
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2) and stack.pop())),
    '∨': # logical OR
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2) or stack.pop())),
    'i': # convert to int
    lambda stacks, stk_no, stack: stack.push(int(stack.pop())),
    'f': # convert to float
    lambda stacks, stk_no, stack: stack.push(float(stack.pop())),
    's': # convert to string
    lambda stacks, stk_no, stack: stack.push(str(stack.pop())),
    'c': # convert number to its ASCII character
    lambda stacks, stk_no, stack: stack.push(chr(stack.pop())),
    'o': # convert character to its ASCII number
    lambda stacks, stk_no, stack: stack.push(ord(stack.pop())),
    '⊢': # slice start of string
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2)[stack.pop():]),
    '⊣': # slice end of string
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2)[:stack.pop()]),
    '⟛': # slice every nth character of string
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2)[::stack.pop()]),
    '&': # bitwise AND
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) & stack.pop()),
    '|': # bitwise OR
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) | stack.pop()),
    '^': # bitwise XOR
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) ^ stack.pop()),
    '~': # bitwise NOT
    lambda stacks, stk_no, stack: stack.push(~ stack.pop()),
    '«': # bit left shift
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) << stack.pop()),
    '»': # bit right shift
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) >> stack.pop()),
    ':': # duplicate
    lambda stacks, stk_no, stack: stack.push(stack.peek()),
    '<': # lesser than
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2) < stack.pop())),
    '>': # greater than
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2) > stack.pop())),
    '=': # equality
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2) == stack.pop())),
    '≤': # lesser than or equal to
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2) <= stack.pop())),
    '≥': # greater than or equal to
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2) >= stack.pop())),
    '±': # sign of number
    lambda stacks, stk_no, stack: stack.push(
        (stack.peek() > 0) - (stack.pop() < 0)),
    '•': # move nth item to the top
    lambda stacks, stk_no, stack: stack.push(stack.pop(stack.pop())),
    '⇆': # switch last two items
    switch,
    '↔': # reverse the stack
    lambda stacks, stk_no, stack: stack.reverse(),
    '↻': # rotate the stack clockwise
    lambda stacks, stk_no, stack: stack.push(stack.pop(), 0),
    '↺': # rotate the stack anti-clockwise
    lambda stacks, stk_no, stack: stack.push(stack.pop(0)),
    '⫰': # minimum of stack
    lambda stacks, stk_no, stack: stack.push(min(stack.items)),
    '⫯': # maximum of stack
    lambda stacks, stk_no, stack: stack.push(max(stack.items)),
    '#': # sum the stack
    sum_stack
}


class UnknownCommand(Exception):
    """An Exception that is raised on an invalid command."""

    def __init__(self, command):
        super(UnknownCommand,
              self).__init__('Unknown command: {!r}'.format(command))


class Stack:
    def __init__(self, items = None):
        if items == None:
            self.items = []
        else:
            self.items = items

    def push(self, item, index = None):
        if index == None:
            self.items.append(item)
        else:
            self.items.insert(index, item)

    def pop(self, index = None):
        if index == None:
            return self.items.pop()
        else:
            return self.items.pop(index)

    def peek(self, index = None):
        if index == None:
            return self.items[-1]
        else:
            return self.items[index]

    def reverse(self):
        self.items = self.items[::-1]

    def __len__(self):
        return len(self.items)


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
        ('string', r'"([^\\]|\\[\s\S])*?"'),
        ('number', r'-?\d+(\.\d*)?'),
        ('noop', r'[ \t\n]+'),
        ('command', r'.')
    ]
    token_regex = '|'.join(r'(?P<{}>{})'.format(*i) for i in token_specs)
    tokens = []

    for token in re.finditer(token_regex, code):
        _type = token.lastgroup
        value = token.group(_type)

        if _type == 'noop':
            pass
        elif _type == 'command':
            if value in commands:
                tokens.append(Token(_type, value))
            else:
                raise UnknownCommand(value)
        else:
            tokens.append(Token(_type, value))

    return tokens


def run(code, args):
    tokens = tokenize(code)
    stacks = [Stack()]
    stk_no = 0

    for arg in args:
        if re.match(r'-?\d+$', arg):
            stacks[stk_no].push(int(arg))
        elif re.match(r'-?\d+(\.\d*)?$', arg):
            stacks[stk_no].push(float(arg))
        else:
            stacks[stk_no].push(arg)

    for token in tokens:
        if token[0] == 'number':
            try:
                stacks[stk_no].push(int(token[1]))
            except ValueError:
                stacks[stk_no].push(float(token[1]))
        elif token[0] == 'string':
            stacks[stk_no].push(token[1][1:-1])
        elif token[0] == 'char':
            stacks[stk_no].push(token[1][1:])
        else:
            commands[token[1]](stacks, stk_no, stacks[stk_no])

    try:
        print(stacks[stk_no].pop())
    except IndexError:
        print()

def main():
    parser = argparse.ArgumentParser(
        description = 'An interpreter for the ,,, language.')
    parser.add_argument('file', help = 'program read from script file',
                        type = open)
    parser.add_argument('args', help = 'arguments for the script',
                        nargs = argparse.REMAINDER)

    arguments = parser.parse_args()
    with arguments.file as f:
        run(f.read(), arguments.args)


if __name__ == '__main__':
    main()
