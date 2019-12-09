### Python Programming for Software Engineers
### Assignment 8
### 'Happy PEPer'
###   Eugene Zuev, Tim Fayz


# Nikita Kalinskiy


# Task 1 (0 points)
# ----------------------------------------------
# Read funny PEP20 (The Zen of Python)


# 1. If you had to chose only one rule which one you would prefer?
# [rule] If the implementation is easy to explain, it may be a good idea


# Task 2-5 (10 points)
# ----------------------------------------------
# Read PEP08 (Style Guide for Python Code)


# 1. What's the reason to limit all the lines to 72-79 characters long?
# [answer]
# Limiting the required editor window width makes it possible to have several files open 
# side-by-side, and works well when using code review tools that present the two versions in
# adjacent columns.

# 1.1 Em..sorry, I forgot! What are 72 and 79 lengths exactly for?
# [answer]
# 72 for flowing long blocks of text (docstrings or comments)
# 79 for all other lines


# 2. How would you reformat this according to PEP08? 
# Well..do I really need a backslash somewhere here?
def stupid_function_written_by_someone(argument_one, argument_two, keywordarg_one = "1",  keywordarg_two = "2",
                                       **something_else):
    pass

# 2.1 Could you provide a code example where the backslash is needed?
# (do not copy paste from PEP itself, ok? - that's forbiden)
# [code]

def count_operators(**args):
    pass


operators_map = None
operands_map = None
token_value = None
token_line = None
last_def_line = None
is_def_handled = None

operators_map, operands_map,  last_def_line, is_def_handled = \
                count_operators(operators_map, operands_map, token_value,
 				token_line, last_def_line, is_def_handled)


# (From now on, stick to 79. Reformat all the rest. And please, do not make it manually! One would expect you to
# simply use IDE feature or plugin)


# 3. Is that correct according to PEP08? 
# Restructure if necessary.

class Class1:
    pass


class Class2:
    pass


def func1(args):
    pass


def func2(args):
    pass


# 4. What's wrong here?
# Restructure if necessary.
import subprocess
import sys
import os

# 4.1 Can I import modules somewhere in the middle? Is it good as for PEP08?
# [answer]
# You can, but following PEP08 'Imports are always put at the top of the file,
# just after any module comments and docstrings 
# and before module globals and constants'


# 4.2 Is it good to do this? If it isn't, why not?
from os import *
# It is okay if you import only one package in your scrpit. 
# Otherwise it can raise a naming collision between functions
# from different modules.

# 4.3 What is relative and absolute imports? Which one is preferred and why?
# [answer] Absolute imports specifies the whole path to the module
# (starting from the root of the project folder)

# Relative imports uses relative path(starting from the path of the 
# current module)

# Absolute is preferable while relative are an acceptable alternative
# to absolute imports, especially when dealing with complex package layouts
# where using absolute imports would be unnecessarily verbose


# 5. Can I use non-latin identifiers according to PEP08? Does it run btw?
имя_пользователя = "John"
user_name = "John"
# [answer]
# No, you cannot. According to PEP08: 'All identifiers in the Python
# standard library MUST use ASCII-only identifiers, 
# and SHOULD use English words wherever feasible'


# 6. What's the matter here? 
# Restructure according to PEP08.
play_on_numbers = (11229065982633 - 11229065982633 + 11229065982633*11229065982633 / (11229065982633//5) +
                   11229065982633)


# 7. What's wrong here? Fix it according to PEP08.
def counter(start, step=10, end=100) -> int:
    print(start)
    if start >= end:
        return 100
    return counter(start+step, step)


# 8. Is it well-formed comment? Reformat accroding to PEP08
'''
This comment doesn't mean anything Nick. 
But still there is some hidden, insidious trick!
Please, just make it more thick!
'''
def func():
    pass


# 9. Which is preferable?
def func(a): return a*a # 1 or
func = lambda a: a*a # 2
# [answer] #1

# 9.1 Why?
# [answer] Because it is always better to use a def statement instead
# of an assignment statement that binds
# a lambda expression directly to an identifier


# 10. Accordign to section:
# https://www.python.org/dev/peps/pep-0008/#naming-conventions

# 10.1 Which naming style would you prefer and why? 
# (eg CamelCase or lowercase or mixedCase etc)
# [answer]
# CamelCase to name classes, exception, type variables
# lowercase for everything else
# mixedCase only when it is already a prevailing style

# 10.2 Which var name of these two would you choose 
# being stuck to CamelCase as your primary naming style?
# NFSReader or NfsReader?
# [answer] NFSReader

# 10.3 Should somehow class and variable names differ?
# [answer] 
# class uses CapsCamelCase naming convention while variables - lowercase

# 10.4 Imagine we need, by some significant reason, to use var names 
# that clash with Python keywords (say, 'class' and 'else').
# What can we do according to PEP08?
def foo():
    # [create two dump vars with names resembling to 'class' and 'else']
    class_ = None
    else_ = None
    pass
