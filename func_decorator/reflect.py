# Python 3.7.4
import inspect
import io
from contextlib import redirect_stdout


def reflect(func):
    """It is not a quine since it uses inspect.getsource(func) to get the source code from the interpreter memory"""
    def dumper(*args, **kwargs):
        members_dict = dict(inspect.getmembers(func))
        print("Name:\t{}".format(func.__name__))
        print("Type:\t{}".format(members_dict['__class__']))
        print("Sign:\t{}\n".format(inspect.signature(func)))

        arg_prefix = "Args:"
        print(arg_prefix + "\tpositional" + str(args))
        print(" " * len(arg_prefix) + '\tkey=worded' + str(kwargs) + "\n")

        doc_prefix = "Doc:"
        doc_strings = members_dict['__doc__'].split("\n")
        print(doc_prefix + "\t" + doc_strings[0])
        for i in range(1, len(doc_strings)):
            print(" " * len(doc_prefix) + doc_strings[i])

        print("Complx:\t{}".format("{'print': " + str(inspect.getsource(func).count('print')) + "}\n"))

        source_prefix = "Source:"
        source_strings = inspect.getsource(func).split('\n')
        print(source_prefix + '\t' + source_strings[0])
        for i in range(1, len(source_strings)):
            print(" " * len(source_prefix) + '\t' + source_strings[i])

        captured_out = io.StringIO()
        with redirect_stdout(captured_out):
            func(*args, **kwargs)
        output_prefix = "Output:"
        func_out_strings = captured_out.getvalue().split('\n')
        if len(func_out_strings) != 0:
            print(output_prefix + '\t' + func_out_strings[0])
            for i in range(1, len(func_out_strings)):
                print(" " * len(output_prefix) + '\t' + func_out_strings[i])
        else:
            print(output_prefix + '\tNone')

    return dumper


# if __name__ == "__main__":
    # We cannot directly use decorator to itself since it is not defined at the moment of apply to the function itself
    # workaround
    # reflect(reflect)(None)
