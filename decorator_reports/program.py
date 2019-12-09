from reporterlib import *

rc(multipage=True, filename='reporter.pdf')


@report_complexity
@report_object
class Foo:
    a = False

    def __init__(self, value1):
        self.value1 = value1

    def print_value(self):
        print(self.value1)


if __name__ == "__main__":
    foo1 = Foo(1)
