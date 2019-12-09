# Python 3.7.4 64bit
import dis
import sys
import marshal
import py_compile
import os
import operator


def check_file_format(filename, file_format):
    if not str(filename).endswith(file_format):
        sys.exit("Ti che pes, {} eto ne {} file".format(filename, file_format))


def dump(code):
    filename = "tmp.py"
    with open(filename, "w+") as f:
        f.write(code)
    f.close()
    py_compile.compile(filename, cfile="out.pyc")
    os.remove(filename)


def compile_files(args):
    for i in range(len(args)):
        if i % 2 == 1:
            continue
        if args[i] == '-py':
            check_file_format(args[i + 1], '.py')
            py_compile.compile(args[i + 1], cfile='file.pyc')
        elif args[i] == "-s":
            dump(args[i + 1])
        else:
            sys.exit('Cannot compile .pyc file')


def print_py(filename):
    check_file_format(filename, '.py')
    bytecode = dis.Bytecode(open(filename).read())
    for instr in bytecode:
        print("{} {}".format(instr.opname, instr.argrepr))


def get_pyc_bytecode(filename):
    header_size = 8
    if sys.version_info >= (3, 7):
        header_size = 16
    elif sys.version_info >= (3, 3):
        header_size = 12
    with open(filename, 'rb') as file:
        file.read(header_size)
        return dis.Bytecode(marshal.loads(file.read()))


def print_pyc(filename):
    check_file_format(filename, '.pyc')
    bytecode = get_pyc_bytecode(filename)
    for instr in bytecode:
        print("{} {}".format(instr.opname, instr.argrepr))


def print_str(code_string):
    compiled = compile(code_string, '<string>', 'exec')
    bytecode = dis.Bytecode(compiled)
    for instr in bytecode:
        print("{} {}".format(instr.opname, instr.argrepr))


def print_bytecode(args):
    for i in range(len(args)):
        if i % 2 == 1:
            continue
        if args[i] == '-py':
            print_py(args[i + 1])
        elif args[i] == '-pyc':
            print_pyc(args[i + 1])
        elif args[i] == "-s":
            print_str(args[i + 1])


def count_instructions_by_files(bytecode, file, filenames, instructions_map):
    for instr in bytecode:
        if instr.opname in instructions_map:
            instructions_map[instr.opname][file] += 1
        else:
            instructions_map[instr.opname] = {file: 1}
            for f in filenames:
                if file != f and f not in instructions_map[instr.opname]:
                    instructions_map[instr.opname][f] = 0
    return instructions_map


def get_instructions_occurrence(instr_map):
    instr_max_occurrences = {}
    for instr, values in instr_map.items():
        instr_max_occurrences[instr] = max(values.items(), key=operator.itemgetter(1))[1]
    return dict(sorted(instr_max_occurrences.items(), key=lambda item: item[1], reverse=True))



def compare_files_bytecode(args):
    instructions_by_files_map = {}

    filenames = []
    for i in range(int(len(args) / 2)):
        filenames.append(args[i * 2 + 1])

    for i in range(len(args)):
        if i % 2 == 1:
            continue
        bytecode = None
        if args[i] == '-py':
            check_file_format(args[i + 1], '.py')
            bytecode = dis.Bytecode(open(args[i + 1]).read())
        elif args[i] == '-pyc':
            check_file_format(args[i + 1], '.pyc')
            bytecode = get_pyc_bytecode(args[i + 1])
        elif args[i] == "-s":
            compiled = compile(args[i + 1], '<string>', 'exec')
            bytecode = dis.Bytecode(compiled)
        instructions_by_files_map = count_instructions_by_files(bytecode, args[i + 1], filenames, instructions_by_files_map)
    sorted_instr = get_instructions_occurrence(instructions_by_files_map)

    table_header = "{:<13}" + "|{:<13}" * int(len(args) / 2)
    filenames[:] = (file[:13] for file in filenames)
    print(table_header.format('INSTRUCTION', *filenames))
    for instr in sorted_instr.keys():
        files_map = instructions_by_files_map[instr]
        print(table_header.format(instr, *files_map.values()))


if sys.argv[1] == "print":
    print_bytecode(sys.argv[2:])
elif sys.argv[1] == "compile":
    compile_files(sys.argv[2:])
elif sys.argv[1] == "compare":
    compare_files_bytecode(sys.argv[2:])
else:
    print("No such action. Use on of these: 'print' , 'compile', 'compare'")
