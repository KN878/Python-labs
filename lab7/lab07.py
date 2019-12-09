### Python Programming for Software Engineers
### Assignment 7
### 'Lambda De Parser'
###   Eugene Zuev, Tim Fayz
###   Special thanks to Ivan Tkachenko

# Nikita Kalinskiy

# Task 1
# ----------------------------------------------
# Given the following:
f = lambda x, y: x * y

# 1. Rewrite to its logical equivalence using ordinary funcion definition(s)
# [code]
def f1(x, y):
    return x * y

# Task 2
# ----------------------------------------------
# Given the following:
f = lambda x: (lambda y: (lambda z: x + y + z))
# 1. How would you call it to get the result of `x + y + z`?
# [code]
x2 = 1
y2 = 1
z2 = 1
f(x2)(y2)(z2)# result = 3
# 2. Rewrite it using only one lambda expression and show how to call it
# [code]
f2 = lambda x, y, z: x + y + z
f2(1, 1, 1)

# Task 3
# ----------------------------------------------
# Given the following:
(lambda b = (lambda *c: print(c)): b("a", "b"))()

# 1. What happens here? Rewrite it so that the code can be
# understood by a normal or your mate who has no idea what the lambda is!
# Provide comments, neat formatting and a bit more meaningful var names.
# [multiline code interlaced with comments]

def args_printer(*args):
    """
    This function implements inner lambda that just print values of all arguments passed to it
    """
    print(args)


def args_printer_wrapper(printer = args_printer):
    """
    This function implements outer lambda that just passes 'a' and 'b' as arguments to args_printer
    function(inner lambda is a default argument of this function)
    """
    printer("a", "b")

args_printer_wrapper()
# Task 4 (soft)
# ----------------------------------------------
# What are the main restrictions on the lambda?
# Provide "If yes, why? If not, why not?" for each of the following:
# 1. Does lambda restrict side effects?
# 2. Does lambda restrict number of allowed statements?
# 3. Does lambda restrict assignments?
# 4. Does lambda restrict number of return values?
# 5. Does lambda restrict the use of default arguments values?
# 6. Does lambda restrict possible function signatures?

# [your enumerated answers; if possible, code is welcomed]
# 1. Lambda itself cannot cause side effects, but it can call a function in its body, which changes state of the program
# some_var = 0
# def increment_some_var_by(incr):
#   global some_var
#   some_var += incr
#
# f = lambda incr: increment_some_var_by(incr)
# f(1)
# now some_var = 1

# 2. Yes, lambda can contain only a single expression in its body
# 3. Yes, since assignment is a statement, not an expression
# 4. Yes, lambda can return only a single object(use tuple to return multiple objects)
# 5. No, the previous tasks shows that it does not
# 6. Yes, as usual function it cannot accept tuples as arguments

# Task 5
# ----------------------------------------------
# Given the following:
(lambda f = (lambda a: (lambda b: print(list(map(lambda x: x+x, a+b))))):
f((1,2,3))((4,5,6)))()

# 1. What happens here? Do the same as in Task 3 and
# enumerate order of execution using (1,2,3...) in comments
# [multiline code interlaced with comments]

# All in all, this lambda takes two iterables, concats them with each other and doubles their values after that

def printer_wrapper(first_tuple):
    """
    This function just takes a tuple and returns a function which accepts another tuple
    """
    def print_concatenated_doubled_tuples(second_tuple):
        """
        This function concatenate two tuples into list, doubles their value and prints the resulted list
        """
        print(list(map(lambda x: x + x, first_tuple + second_tuple)))
    return print_concatenated_doubled_tuples

def printer_wrapper_wrapper():
    printer_wrapper((1,2,3))((4,5,6))

printer_wrapper_wrapper()

# 1. printer_wrapper_wrapper is called first
# 2. then printer with arguments (1,2,3) is called
# 3. finally the third function(print_concatenated_doubled_tuple) is called with parameters (4,5,6)

# 2. Why does map() requires list() call?
# [written answer]
# list() allows us to create a list object from the doubled values and evaluate them at the moment since map() only
# creates a map iterator, which has a logic of lazy evaluation of its values
