#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
,,, (Commata)

A language that probably hopefully does something.

Sumant Bhaskaruni
v0.2.0 (basically, don't use it)
"""

import functions
import tokenizer


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

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return (self.pop(0) for i in range(len(self)))


def run(code, args):
    tokens = tokenizer.tokenize(code)
    stacks = [Stack()]
    stk_no = 0

    for arg in args:
        stacks[stk_no].push(functions.lit_eval(arg))

    for token in tokens:
        if token[0] == 'number':
            stacks[stk_no].push(functions.lit_eval(token[1]))
        elif token[0] == 'string':
            stacks[stk_no].push(functions.lit_eval(token[1][1:-1]))
        elif token[0] == 'unclosed_string':
            stacks[stk_no].push(functions.lit_eval(token[1][1:]))
        elif token[0] == 'char':
            stacks[stk_no].push(functions.lit_eval(token[1][1:]))
        else:
            functions.commands[token[1]](stacks, stk_no, stacks[stk_no])

    try:
        print(stacks[stk_no].pop())
    except IndexError:
        print()
