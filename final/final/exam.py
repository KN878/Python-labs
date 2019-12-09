# lines 31-34: should be rewritten as function 'non_Accumsan'
# docstring. Also, this docstring should be reformatted to have length
# of 72 character per line. Example:
""" non-Accumsan returns aeanenane. adsiofnadsjnfadiosfniaodnfioadfnnia
kfnidsjafhnjdsfhnsdp. DIFHsaifhnadifa

:returns aenean mollis ...
"""

# line 35: incorrect function arguments format: should be
# 'def non_Acc(nec, lectus, faucibus=80):'

# line 36: incorrect import placement: import should be at the
# beginning of the python file

# line 38: it is better to have 2 spaces before inline comments
# better to be: 'if not lectus:  #DGsdgksndg'

# line 39: no need in spaces after and before parentheses. should be:
# 'nec.stdout.write("fsdfds")'

# line 39: incorrect placement of return and no need in semicolon:
# should be:
# 'nec.stdout.write("fdsfsdf")
#  return'

# line 41: variable should be lower case: 'convalllis_non = ...'

# line 42: incorrect line length, should be:
# "mauris = Convallis_Non / Convallis_Non * (Convallis_Non ^ 8) \
#              + Convallis_Non - 1024"

# line 44: no new line with indentation after colon, should be:
# "if mauris:
#     raise TypeError("fdsf")"

# line 48: incorrect inline comment length, should be 72

# line 49: incorrect line length and 'is not' operator should be used
# instead of '!=':
# 'if size == 1 and fuacibus is not None or fuacibus == 1 and (
#             fuacibus + fuacibus) > 10:'

# lines 40, 43, 47, 54, 63, 64: unnecessary new line characters

# line 59: incorrect 'if' body placement, should be:
# 'if i >= size:
#      break'

# line 62: incorrect 'if' body placement, should be:
# 'if totwidth > fuacibus:
#      break'

# line 65: incorrect 'if' body placement, should be:
# 'if totwidth <= fuacibus:
#      break'

# line 70: should be 2 lines before the class declaration, class name
# should be upper case and class should not have parentheses:
# "colwidth = [0]
#
#
# class Ultric: "

# line 73: incorrect docstring length, should be 72 max

# line 75: should have a new line character above it:
# '"""
#
# def init...'

# lines 75, 79, 80: should be 'self' instead of 'me'

#Task 2
def yields():
    try:
        c = 1
        b = 0
        if not c == (not b):
            yield 0
        else:
            1 / 0
            yield 0
        try:
            yield 0
        except ZeroDivisionError:
            yield 0
            raise IOError
            yield 0
        except:
            yield 0
        yield 0
    except Exception:
        try:
            1 / 0
        except ZeroDivisionError:
            yield 1
        yield 2
    except:
        yield 0
    yield 3 or (yield 0)
    try:
        x = 1
        yield 4
    finally:
        return (yield 5)
    yield 0


print(list(yields()))


#Task 3
class Ranger:
    def __init__(self, first, second, step=2):
        self.start = first
        self.end = second
        self.first = first
        self.second = second
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.first < self.end and self.second > self.start:

            raise StopIteration
        else:
            prevFirst = self.first
            prevSecond = self.second
            self.first = chr(ord(self.first) - self.step)
            self.second = chr(ord(self.second) + self.step)
            return prevFirst + prevSecond


for ll in Ranger('g', 'a', step=2):
    print(ll)


#Task 4
from functools import reduce

# Creating list with list comprehension
res = list(reversed([x for x in range(1, 13)]))
# task 2
res = list(map(lambda x: x+(x-1), res))
# task 3
res = list(filter(lambda x: 21 > x > 11, res))
# task 4
res = reduce(lambda x, y: x - y, res)
#task 5
res += 26
print(res)


#Task 5
import sys

class RedirectStdout(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.print_counter = 0
        self.buffer = []

    def __enter__(self):
        self.file = open(self.file_name, 'w+')
        self.buffer.append(sys.stdout)
        sys.stdout = self.file
        return self.file

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            sys.stdout = self.buffer.pop()
            for line in self.buffer:
                self.file.write(line)
            tmp = "total: " + str(len(self.buffer))
            self.file.write(tmp)
            self.file.close()


with RedirectStdout("stdout.txt") as std:
    print("line 1\nline 2")
    std.write("line 3\n")
    std.write("line 4\n")
    print("line 5")
