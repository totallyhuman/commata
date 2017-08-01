#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import math
import re

def lit_eval(x):
    if re.match(r'-?\d+(\.\d*)?', str(x)):
        return float(x)

    return ast.literal_eval(repr(x))


def is_prime(n):
    if n == 2:
        return 1
    if n == 3:
        return 1
    if n % 2 == 0:
        return 0
    if n % 3 == 0:
        return 0

    i = 5
    w = 2

    while i * i <= n:
        if n % i == 0:
            return 0

        i += w
        w = 6 - w

    return 1


def product_stack(stacks, stk_no, stack):
    if isinstance(stack.peek(), str):
        result = ''
        for _ in range(len(stack)):
            result *= int(stack.pop())
    else:
        result = 0
        for _ in range(len(stack)):
            result *= lit_eval(stack.pop())


def primes(n):
    result = set()
    for i in range(1, int(n ** 0.5) + 1):
        div, mod = divmod(n, i)
        if mod == 0:
            result |= {i, div}
    return sorted(result)


def sum_stack(stacks, stk_no, stack):
    if isinstance(stack.peek(), str):
        result = ''
        for _ in range(len(stack)):
            result += str(stack.pop())
    else:
        result = 0
        for _ in range(len(stack)):
            result += lit_eval(stack.pop())

    stack.push(result)

def to_base(n, base):
    if n == 0:
        return 0

    digits = []

    while n:
        digits.append(int(n % base))
        n /= base

    return sum(digits)

commands = {
    '+': # addition or concatenation
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) + stack.pop()),
    '-': # subtraction
    lambda stacks, stk_no, stack: stack.push(lit_eval(stack.pop(-2)) - lit_eval(stack.pop())),
    '×': # multiplication or string multiplication
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) * stack.pop()),
    '÷': # division
    lambda stacks, stk_no, stack: stack.push(lit_eval(stack.pop(-2)) / lit_eval(stack.pop())),
    '/': # integer division
    lambda stacks, stk_no, stack: stack.push(lit_eval(stack.pop(-2)) // lit_eval(stack.pop())),
    '%': # modulo or string formatting
    lambda stacks, stk_no, stack: stack.push(stack.pop(-2) % stack.pop()),
    '*': # exponentiation
    lambda stacks, stk_no, stack: stack.push(lit_eval(stack.pop(-2)) ** lit_eval(stack.pop())),
    '√': # square root
    lambda stacks, stk_no, stack: stack.push(math.sqrt(lit_eval(stack.pop()))),
    '_': # negate
    lambda stacks, stk_no, stack: stack.push(0 - lit_eval(stack.pop())),
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
    lambda stacks, stk_no, stack: stack.push(chr(int(stack.pop()))),
    'o': # convert character to its ASCII number
    lambda stacks, stk_no, stack: stack.push(ord(stack.pop())),
    'b': # conver number to base
    lambda stacks, stk_no, stack: stack.push(to_base(stack.pop(-2), stack.pop())),
    'B': # convert integer to binary
    lambda stacks, stk_no, stack: stack.push(bin(int(stack.pop()))[2:]),
    '🀱': # nth character of string
    lambda stacks, stk_no, stack: stack.push(str(stack.pop(-2))[int(stack.pop())]),
    '⊢': # slice start of string
    lambda stacks, stk_no, stack: stack.push(str(stack.pop(-2))[int(stack.pop()):]),
    '⊣': # slice end of string
    lambda stacks, stk_no, stack: stack.push(str(stack.pop(-2))[:int(stack.pop())]),
    '⟛': # slice every nth character of string
    lambda stacks, stk_no, stack: stack.push(str(stack.pop(-2))[::int(stack.pop())]),
    '⍷': # count instances of x in y
    lambda stacks, stk_no, stack: stack.push(str(stack.pop(-2)).count(str(stack.pop()))),
    '&': # bitwise AND
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2)) & int(stack.pop())),
    '|': # bitwise OR
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2)) | int(stack.pop())),
    '^': # bitwise XOR
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2)) ^ int(stack.pop())),
    '~': # bitwise NOT
    lambda stacks, stk_no, stack: stack.push(~ int(stack.pop())),
    '«': # bit left shift
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2)) << int(stack.pop())),
    '»': # bit right shift
    lambda stacks, stk_no, stack: stack.push(int(stack.pop(-2)) >> int(stack.pop())),
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
    'a': # absolute value
    lambda stacks, stk_no, stack: stack.push(abs(stack.pop())),
    'p': # primality test
    lambda stacks, stk_no, stack: stack.push(is_prime(lit_eval(stack.pop()))),
    'P': # prime factorization
    lambda stacks, stk_no, stack: [stack.push(i) for i in primes(stack.pop())],
    'œ': # parity test, 1 if odd, 0 if even
    lambda stacks, stk_no, stack: stack.push(lit_eval(stack.pop()) % 2),
    '•': # move nth item to the top
    lambda stacks, stk_no, stack: stack.push(stack.pop(int(stack.pop()))),
    '⇆': # switch last two items
    lambda stacks, stk_no, stack: stack.push(stack.pop(-1)),
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
    'Σ': # sum the stack
    sum_stack,
    '⨳': # product of the stack
    product_stack
}
