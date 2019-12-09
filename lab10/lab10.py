### Python Programming for Software Engineers
### Assignment 10
### '(Anniversary) Inverse of Assignment 10'
###   Eugene Zuev, Tim Fayz

# Here is your story: 
# It is 2005. Recently, you've got your dream job offer from one of the
# best "Big Five" tech company. More than that, you've been immediately
# accepted as a Lead Developer! Isn't it cool..huh? BUT! Here is the
# trick.. Your manager (as it turns out after a month of normal
# operation) is a real pro butt! The story doesn't tell us if he was a
# Lead Developer too. What we know, however, is that he is most certainly
# the one who had been doing "mission critical tasks" at the very
# beggining of the company. He [as our course suggests] loves Python more
# than his wife and always keep in touch with the latest news stories.
# [btw...the reason he gave up his original job is a decision to stop
# h***ing his own brain and let others do that instead. Maybe he tired in
# general or that's a priority change. Nobody knows now...] So now, on
# the same cool Reddit channel he once heard there is an upcoming PEP 343
# that introduces a "with" statement. "What's THAT, man!?" -- he
# wondered. The old pro immediately realizes whatever it is he wants it
# to be integrated as a "new great technology" [but yet keeping his own
# hands clean]. So the choice WHO will teach others to use this statement
# (and adopt it into an existing code base) fell on YOU. [That may sound
# strange] but now he wants you to prepare a set of tasks to be sure that
# the aforementioned PEP 343 was read, consumed and understood by all
# department developers. As an example -- how these all should look like
# -- the old pro referenced back to well-known assignments 7 till 9.
# Moreover, he decided to entitle most of the tasks to mix his own
# intentions. As it turns out (again) he is a sly one. Our pro butt wants
# a "special edition" of your working where all the answers are given in
# advance! [most probably to "save" his time of doing it by hands; which
# is a bad idea anyway...] As you may guess, he set up a deadline ['cause
# you know...he is a manager] that you are supposed to meet! It's Nov 21,
# 10:35AM [just in case you have forgotten.] He absolutely can't keep his
# patience of waiting for your tasks! And the ultimate moment where he
# will proudly spread them over the department uttering "This is how we
# stay on cutting-edge!" 
# End of the story. 
# You can begin now...


# Introduction (an abstract)
# ----------------------------------------------
# [what and why "with" is]
# PEP 343 introduces a 'with' statement to make it possible to factor out
# standard uses of try/finally statements that were used previously to ensure
# that clean-up code is executed.
# The 'with' statement is a new control-flow structure like:
#   'with expression [as variable]:
#       with-block'
# , where the expression evaluated and results in an object with __enter__()
# and __exit()__ methods(context management protocol).

# [code example(s); don't copy paste from PEP!]
# 1) Simple file open and write operations
filename = "tmp.txt"
with open(filename, "w+") as f:
    f.write("hello")


# 2) More complicated, but still simple file writer object
class MessageWriter(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, 'w+')
        return self.file

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            self.file.close()


with MessageWriter('my_file.txt') as xfile:
    xfile.write('hello world')

# Task 1 (demonstrates the benefits of using with)
# ----------------------------------------------
# Task: implement file writer 1) without using 'with' and 2) using 'with' statement

# Answers:
# 1) without using with statement
file = open('file.txt', 'w+')
try:
    file.write('hello world')
finally:
    file.close()

# 2) using with statement
with open('file.txt', 'w+') as file:
    file.write('hello world !')

# Task 2 (demonstrates how to use several nested with's)
# ----------------------------------------------
# Task: You have a file - 'code.txt'. You should read a code from it, execute the code
# and write the result in 'result.txt'

# Answer:
import io
from contextlib import redirect_stdout

with open('code.txt', 'r') as code:
    with open('result.txt', 'w+') as result:
        captured_out = io.StringIO()
        with redirect_stdout(captured_out):
            exec(code.read())
        result.write(captured_out.getvalue())


# Task 3 (demonstrates how to create your own context manager)
# ----------------------------------------------
# Task: Create your own file writer class 'MessageWriter' that implements
# context manager functionality and writes a string 'hello world' to 'my_file.txt'

# Answer:
class MessageWriter(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, 'w+')
        return self.file

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            self.file.close()


with MessageWriter('my_file.txt') as xfile:
    xfile.write('hello world')

# Task 4 (demonstrates exception handling)
# ----------------------------------------------
# Task: write a code that opens a file 'no_file.txt' for reading
# using 'with' statement and printing its context. If there is no such file,
# the code should catch the exception and print
# 'Provide an existing file'

# Answer:
try:
    with open('no_file.txt', 'r') as file:
        print(file.read())
except FileNotFoundError:
    print("Provide an existing file")

# Task 5 (your own)
# ----------------------------------------------
# Task: Create a Mandelbrot set image using real and image 'c' parts ranges,
# rpoints and ipoints, infinity border, and max_iterations, that are
# written in 'mandelbrot.txt'. Values are separated by commas and
# first 2 values are real part min and max values and last 2 - complex part values.

import numpy as np
import matplotlib.pyplot as plt


def mandelbrot():
    with open('mandelbrot.txt') as ranges:
        values = ranges.read().split(',')
    rmin, rmax, imin, imax = float(values[0]), float(values[1]), float(values[2]), float(values[3])
    rpoints = int(values[4])
    ipoints = int(values[5])
    infinity_border = int(values[6])
    max_iterations = int(values[7])
    image = np.zeros((rpoints, ipoints))
    r, i = np.mgrid[rmin:rmax:(rpoints * 1j), imin:imax:(ipoints * 1j)]
    c = r + 1j * i
    z = np.zeros_like(c)
    for k in range(max_iterations):
        z = z ** 2 + c
        mask = (np.abs(z) > infinity_border) & (image == 0)
        image[mask] = k
        z[mask] = np.nan
    plt.imshow(-image.T, cmap='flag')
    plt.show()


mandelbrot()
