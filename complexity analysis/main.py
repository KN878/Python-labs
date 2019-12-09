import sys
import tokenize
import keyword
import ast
from math import log2
from io import BytesIO


def get_tokens():
    """
    Method extracts tokens for input file
    :return: list of tokens
    """
    reader = BytesIO(source_code.encode('utf-8')).readline

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


def count_functions_args():
    """
    Counts number of arguments in all function declarations and calls
    :return: int
    """
    count = 0
    tree = ast.parse(source_code)
    print(tree)
    ast.dump(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            count += len(node.args.args)
        if isinstance(node, ast.Call):
            count += len(node.args)
    return count


def analyze():
    """
    Method analyzes source code using Halstead’s complexity
    :return:
    """
    operators_map = {}
    operands_map = {}
    last_def_line = -1
    is_def_handled = True
    # used to detect indices
    prev_token = {'type': None, 'value': None}
    tokens = get_tokens()
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
            operators_map, operands_map,  last_def_line, is_def_handled = \
                count_operators(operators_map, operands_map, token_value, token_line, last_def_line, is_def_handled)

        prev_token['type'] = token_type
        prev_token['value'] = token_value

    operands_map['args'] = count_functions_args() if 'args' not in operands_map else operands_map['args'] + count_functions_args()
    print_operators(operators_map)
    print_operands(operands_map)
    print_program_complexity(operators_map, operands_map)


def print_program_complexity(operators_map, operands_map):
    print("\n[program]")

    vocabulary = get_program_vocabulary(operators_map, operands_map)
    length = get_program_length(operators_map, operands_map)
    calc_length = get_calculated_length(operators_map, operands_map)
    volume = get_program_volume(vocabulary, length)
    difficulty = get_program_difficulty(operators_map, operands_map)
    effort = get_effort(volume, difficulty)

    print("vocabulary: " + str(vocabulary))
    print("length: " + str(length))
    print("calc_length: " + str(calc_length))
    print("volume: " + str(volume))
    print("difficulty: " + str(difficulty))
    print("effort: " + str(effort))


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
    return n1*log2(n1) + n2*log2(n2)


def get_program_volume(vocabulary, length):
    return length * log2(vocabulary)


def get_program_difficulty(operators_map, operands_map):
    n1 = len(operators_map.keys())
    n2 = len(operands_map.keys())
    operands_length = 0
    for value in operands_map.values():
        operands_length += value
    return n1/2 * operands_length/n2


def get_effort(volume, difficulty):
    return volume * difficulty


def print_operators(operators_map):
    print("[operators]")

    total_count = 0
    for op, count in operators_map.items():
        print(op + ": " + str(count))
        total_count += count
    print("N1: " + str(total_count))


def print_operands(operands_map):
    print("\n[operands]")

    total_count = 0
    for op, count in operands_map.items():
        print(op + ": " + str(count))
        total_count += count
    print("N2: " + str(total_count))


if __name__ == "__main__":
    source_code = sys.stdin.read()
    analyze()
