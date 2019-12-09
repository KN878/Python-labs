# Python 3.7.4
import inspect
import io
import tokenize
import keyword
import ast
import os
from contextlib import redirect_stdout
from math import log2
from functools import wraps
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from fpdf import FPDF
from PyPDF2 import PdfFileMerger, PdfFileReader

filename1 = 'report.pdf'
papersize_map = {'a4': [8.27, 11.69], 'a3': [16.53, 11.69]}
papersize1 = 'a4'
multipage1 = False
aggregated_pdf = None


def rc(multipage=False, filename='report.pdf', papersize='a4'):
    global multipage1
    multipage1 = multipage
    global filename1
    filename1 = filename
    global papersize1
    papersize1 = papersize
    if multipage1 and os.path.exists(filename1):
        os.remove(filename1)


def report_object(name=True, type=True, sign=True, arg=True, docstrings=True, source=True, output=True):
    def real_decorator(entity):
        @wraps(entity)
        def reporter(*args, **kwargs):
            pdf = FPDF(format=papersize1.upper())
            members_dict = dict(inspect.getmembers(entity))
            title = '\"' + entity.__name__ + '\"' + " object report\n"
            set_object_report_title(pdf, title)

            if name:
                name_str = "Name:\t{}\n".format(entity.__name__)
                write_object_report_body(pdf, name_str)

            if type:
                type_str = "Type:\t{}\n".format(members_dict['__class__'])
                write_object_report_body(pdf, type_str)

            if sign:
                sign_str = "Sign:\t{}\n".format(inspect.signature(entity))
                write_object_report_body(pdf, sign_str)

            if arg:
                arg_str = "Args:\tPositional: " + str(args) + "\n" + " " * len("Args: ") + '\tkey=worded' + str(kwargs) + "\n"
                write_object_report_body(pdf, arg_str)

            if docstrings:
                doc_str = ""
                if members_dict['__doc__']:
                    doc_strings = members_dict['__doc__'].split("\n")
                    doc_str = "Doc:\t" + doc_strings[0] + '\n'
                    for i in range(1, len(doc_strings)):
                        doc_str += " " * len("Doc:") + '\t' + doc_strings[i] + '\n'

                write_object_report_body(pdf, doc_str)

            if source:
                source_strings = inspect.getsource(entity).split('\n')
                source_str = "Source:\t" + source_strings[0] + '\n'
                for i in range(1, len(source_strings)):
                    source_str += " " * len("Source:") + '\t' + source_strings[i] + '\n'

                write_object_report_body(pdf, source_str)

            if output:
                captured_out = io.StringIO()
                with redirect_stdout(captured_out):
                    entity(*args, **kwargs)
                output_str = "Output:\t"
                func_out_strings = captured_out.getvalue().split('\n')
                if len(func_out_strings) != 0:
                    output_str += func_out_strings[0] + '\n'
                    for i in range(1, len(func_out_strings)):
                        output_str += " " * len("Output:") + '\t' + func_out_strings[i] + '\n'
                else:
                    output_str += 'None'

                write_object_report_body(pdf, output_str)

            pdf.output(entity.__name__ + "_object.pdf", 'F')
            if multipage1:
                merger = PdfFileMerger()
                if os.path.exists(filename1):
                    merger.append(PdfFileReader(filename1))
                merger.append(PdfFileReader(entity.__name__ + "_object.pdf"))
                merger.write(filename1)
                os.remove(entity.__name__ + "_object.pdf")

            return entity(*args, **kwargs)
        return reporter
    return real_decorator


def report_complexity(operators=True, operands=True, complexity=True, uwsc=True, loc=True):
    def real_decorator(entity):
        @wraps(entity)
        def reporter(*args, **kwargs):
            operators_map, operands_map = analyze(inspect.getsource(entity))
            with PdfPages(entity.__name__ + '_complexity.pdf') as pdf:
                if operators:
                    print_map_to_figure(pdf, operators_map, 'Operators')

                if operands:
                    print_map_to_figure(pdf, operands_map, 'Operands')

                if complexity:
                    program_complexity = get_program_complexity(operators_map, operands_map)

                    if inspect.getsource(entity).startswith('class'):  # metrics about class
                        if uwsc:
                            program_complexity = get_uwsc(program_complexity, operators_map, entity)
                        if loc:
                            program_complexity = get_loc(program_complexity, entity)

                    print_map_to_figure(pdf, program_complexity, 'Complexity')

            if multipage1:
                merger = PdfFileMerger()
                if os.path.exists(filename1):
                    merger.append(PdfFileReader(filename1))
                merger.append(PdfFileReader(entity.__name__ + "_complexity.pdf"))
                merger.write(filename1)
                os.remove(entity.__name__ + "_complexity.pdf")

            return entity(*args, **kwargs)
        return reporter
    return real_decorator


def get_uwsc(program_complexity, operators_map, entity_class):
    """
    Calculates Unweighted Class Size
    :param program_complexity: dict
    :param operators_map: dict
    :param entity_class: class
    :return: dict
    """
    uwsc = 0
    uwsc += operators_map['def']
    attributes = inspect.getmembers(entity_class, lambda a: not (inspect.isroutine(a)))
    for a in attributes:
        if not (a[0].startswith('__') and a[0].endswith('__')):
            uwsc += 1
    if uwsc != 0:
        program_complexity['uwsc'] = uwsc
    return program_complexity


def get_loc(program_complexity, entity_class):
    loc = len(list(filter(lambda line: line != '\n', inspect.getsourcelines(entity_class)[0])))  # remove lines with only \n
    if loc / 1000 >= 1:
        kloc = loc / 1000
        program_complexity['KLOC'] = kloc + loc % float(kloc*1000)
    else:
        program_complexity['LOC'] = loc
    return program_complexity


def print_map_to_figure(pdf, map, title):
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2., 1.01 * height,
                    '%f' % float(height),
                    ha='center', va='bottom')

    plt.figure(figsize=(papersize_map[papersize1][0], papersize_map[papersize1][1]), dpi=100)
    plt.title(title)
    rects1 = plt.bar(range(len(map)), list(map.values()), align='center')
    autolabel(rects1)
    plt.xticks(range(len(map)), list(map.keys()), rotation=75)
    pdf.savefig()
    plt.close()


def set_object_report_title(pdf, title):
    width = len(title) + 5
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_x((210 - width) / 2)
    pdf.cell(width, 10, title, 'C')
    pdf.ln(10)


def write_object_report_body(pdf, text):
    pdf.set_font('Times', '', 12)
    # Output justified text
    pdf.multi_cell(0, 5, text)
    pdf.ln()


def text_to_figure(text):
    figure = plt.figure()
    figure.text(.1, .1, text, fontfamily="monospace")
    return figure


def stat_object(func):
    """It is not a quine since it uses inspect.getsource(func) to get the source code from the interpreter memory"""

    @wraps(func)
    def dumper(*args, **kwargs):
        members_dict = dict(inspect.getmembers(func))
        reflect_map = {'Name': func.__name__, 'Type': members_dict['__class__'], 'Sign': inspect.signature(func)}

        reflect_map['Args'] = {'positional': str(args), 'key=worded': str(kwargs)}

        if members_dict['__doc__']:
            reflect_map['Doc'] = members_dict['__doc__']

        reflect_map['Source'] = inspect.getsource(func)

        captured_out = io.StringIO()
        with redirect_stdout(captured_out):
            func(*args, **kwargs)
        reflect_map['Output'] = captured_out.getvalue()

        print(reflect_map)
        return func(*args, **kwargs)

    return dumper


def stat_complexity(func):
    """
    Method analyzes source code using Halstead’s complexity
    :return:
    """

    @wraps(func)
    def dumper(*args, **kwargs):
        source_code = inspect.getsource(func)
        operators_map, operands_map = analyze(source_code)
        print_operators(operators_map)
        print_operands(operands_map)
        print(get_program_complexity(operators_map, operands_map))
        return func(*args, **kwargs)

    return dumper


def analyze(source_code):
    operators_map = {}
    operands_map = {}
    last_def_line = -1
    is_def_handled = True
    # used to detect indices
    prev_token = {'type': None, 'value': None}
    tokens = get_tokens(source_code)
    for token_type, token_value, _, _, token_line in tokens:
        # detecting literals and docstrings
        if token_type == tokenize.NUMBER:
            operands_map['literals'] = 1 if 'literals' not in operands_map else operands_map['literals'] + 1
        elif token_type == tokenize.STRING:
            if token_value.startswith("\"\"\""):
                operands_map['docstrings'] = 1 if 'docstrings' not in operands_map else operands_map['docstrings'] + 1
            else:
                operands_map['literals'] = 1 if 'literals' not in operands_map else operands_map['literals'] + 1
        # detecting inline comments
        elif token_value.startswith("#"):
            operands_map['inlinedocs'] = 1 if 'inlinedocs' not in operands_map else operands_map['inlinedocs'] + 1
        # detect indices by checking previous token under being an identifier but not a keyword
        elif token_value == '[' and prev_token['type'] == tokenize.NAME and not keyword.iskeyword(prev_token['value']):
            operands_map['args'] = 1 if 'args' not in operands_map else operands_map['args'] + 1
        # counting an operator
        else:
            operators_map, operands_map, last_def_line, is_def_handled = \
                count_operators(operators_map, operands_map, token_value, token_line, last_def_line, is_def_handled)

        prev_token['type'] = token_type
        prev_token['value'] = token_value

    operands_map['args'] = count_functions_args(source_code) if 'args' not in operands_map else operands_map[
                                                                                                    'args'] + count_functions_args(
        source_code)
    return operators_map, operands_map


def get_tokens(source_code):
    """
    Method extracts tokens for input file
    :return: list of tokens
    """
    reader = io.BytesIO(source_code.encode('utf-8')).readline

    return tokenize.tokenize(reader)


def count_operators(operators_map, operands_map, op, line, last_def_line, is_def_handled):
    """
    Method counts all operators
    :param operators_map: dict
    :param operands_map: dict
    :param op: str
    :param line: int
    :param last_def_line: int
    :param is_def_handled: bool
    :return: dict, dict, int, bool
    """
    if op == 'if':
        operators_map['if'] = 1 if 'if' not in operators_map else operators_map['if'] + 1
    elif op == 'else':
        operators_map['else'] = 1 if 'else' not in operators_map else operators_map['else'] + 1
    elif op == 'elif':
        operators_map['elif'] = 1 if 'elif' not in operators_map else operators_map['elif'] + 1
    elif op == 'try':
        operators_map['try'] = 1 if 'try' not in operators_map else operators_map['try'] + 1
    elif op == 'for':
        operators_map['for'] = 1 if 'for' not in operators_map else operators_map['for'] + 1
    elif op == 'with':
        operators_map['with'] = 1 if 'with' not in operators_map else operators_map['with'] + 1
    elif op == 'return':
        operators_map['return'] = 1 if 'return' not in operators_map else operators_map['return'] + 1
    elif op == 'def':
        operators_map['def'] = 1 if 'def' not in operators_map else operators_map['def'] + 1
        operands_map['entities'] = 1 if 'entities' not in operands_map else operands_map['entities'] + 1
        last_def_line = line
        is_def_handled = False
    elif op == 'import':
        operators_map['import'] = 1 if 'import' not in operators_map else operators_map['import'] + 1
    elif op == 'except':
        operators_map['except'] = 1 if 'except' not in operators_map else operators_map['except'] + 1
    elif op == '=':
        operators_map['assign'] = 1 if 'assign' not in operators_map else operators_map['assign'] + 1
        operands_map['entities'] = 1 if 'entities' not in operands_map else operands_map['entities'] + 1
    elif op == '+' or op == '-' or op == '*' or op == '/':
        operators_map['arithmetic'] = 1 if 'arithmetic' not in operators_map else operators_map['arithmetic'] + 1
    elif op == '==' or op == '!=' or op == 'and' or op == 'not':
        operators_map['logic'] = 1 if 'logic' not in operators_map else operators_map['logic'] + 1
    elif op == '(':
        # detecting a call when it is not on the same string as func def
        if line != last_def_line:
            operators_map['call'] = 1 if 'call' not in operators_map else operators_map['call'] + 1
        # detecting a call when it is on the same string as func def
        # but func def '(' operator has already appeared
        elif is_def_handled:
            operators_map['call'] = 1 if 'call' not in operators_map else operators_map['call'] + 1
        # detecting a func def '(' operator
        else:
            is_def_handled = True
    elif op == 'class':
        operands_map['entities'] = 1 if 'entities' not in operands_map else operands_map['entities'] + 1

    return operators_map, operands_map, last_def_line, is_def_handled


def count_functions_args(source_code):
    """
    Counts number of arguments in all function declarations and calls
    :return: int
    """
    count = 0
    tree = ast.parse(source_code)
    ast.dump(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            count += len(node.args.args)
        if isinstance(node, ast.Call):
            count += len(node.args)
    return count


def get_program_complexity(operators_map, operands_map):
    program = {}
    program['vocabulary'] = get_program_vocabulary(operators_map, operands_map)
    program['length'] = get_program_length(operators_map, operands_map)
    program['calc_length'] = get_calculated_length(operators_map, operands_map)
    program['volume'] = get_program_volume(program['vocabulary'], program['length'])
    program['difficulty'] = get_program_difficulty(operators_map, operands_map)
    program['effort'] = get_effort(program['volume'], program['difficulty'])

    return program


def get_program_vocabulary(operators_map, operands_map):
    return len(operators_map.keys()) + len(operands_map.keys())


def get_program_length(operators_map, operands_map):
    length = 0
    for value in operators_map.values():
        length += value
    for value in operands_map.values():
        length += value
    return length


def get_calculated_length(operators_map, operands_map):
    n1 = len(operators_map.keys())
    n2 = len(operands_map.keys())
    return n1 * log2(n1) + n2 * log2(n2)


def get_program_volume(vocabulary, length):
    return length * log2(vocabulary)


def get_program_difficulty(operators_map, operands_map):
    n1 = len(operators_map.keys())
    n2 = len(operands_map.keys())
    operands_length = 0
    for value in operands_map.values():
        operands_length += value
    return n1 / 2 * operands_length / n2


def get_effort(volume, difficulty):
    return volume * difficulty


def print_operators(operators_map):
    total_count = 0
    for _, count in operators_map.items():
        total_count += count
    operators_map['N1'] = total_count
    print(operators_map)


def print_operands(operands_map):
    total_count = 0
    for _, count in operands_map.items():
        total_count += count
    operands_map["N2"] = total_count
    print(operands_map)
