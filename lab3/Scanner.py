import re
from collections import defaultdict
from typing import Tuple, List

from LexicalException import LexicalException

tokens_list = ["identifier", "constant", "[", "]", "{", "}", "(", ")", ":", ";",
               "+", "-", "/", "*", "<", ">", "<=", ">=", "==", "=", "!=", "if", "else", "for", "while", "print", "input",
               "and", "in", "int", "string", "boolean", "array", "var"]


def generate_codification_table():
    return {k: v for v, k in enumerate(tokens_list)}


class Scanner:
    def __init__(self, codification_table: dict, input_file: str, output_file):
        self.codification_table = codification_table
        self.input_file = input_file
        self.output_file = output_file
        self.program_internal_form: List[Tuple[int, Tuple[int, int]]] = []
        self.identifiers_symbol_table = defaultdict(list)
        self.constants_symbol_table = defaultdict(list)
        self.OPERATORS = ["+", "-", "/", "*", "<", ">", "="]
        self.COMPOUND_OPERATORS = ["<=", ">=", "==", "!="]
        self.KEYWORDS = ["identifier", "constant", "if", "else", "for", "while", "print", "True", "False", "input",
                         "and", "in", "int", "string", "boolean", "array", "var"]
        self.SEPARATORS = ["[", "]", "]", "(", ")", "{", "}", ":", ";"]
        self.IDENTIFIER = "identifier"
        self.CONSTANT = "constant"
        self.INTEGER_REGEX = "^0$|[-+]?[1-9]\d*$"
        self.FLOAT_REGEX = "(^0$|[-+]?[1-9]\d*).[0-9]\d*$"
        self.STRING_REGEX = '"\w*"'

    @staticmethod
    def detect(line: str) -> List[str]:
        tokens = [x for x in re.split(
            '([^\w."])', line) if x != '' and x != ' ']
        return tokens

    def is_keyword(self, inp):
        return inp in self.KEYWORDS

    def is_operator(self, inp):
        return inp in self.OPERATORS

    def is_separator(self, inp):
        return inp in self.SEPARATORS

    # codification ,symbol table, pif

    @staticmethod
    def is_identifier(inp):
        if len(inp) > 8 or (inp[0].isupper() or inp[0].isdigit()):
            return False
        if not all(c.isalpha() or c.isdigit() for c in inp):
            return False
        return True

    def is_number_constant(self, inp):
        return any([bool(re.match(self.INTEGER_REGEX, inp)), bool(re.match(self.FLOAT_REGEX, inp))])

    def is_constant(self, inp):
        try:
            fl = float(inp)
            b = bool(re.match(self.INTEGER_REGEX, inp))
            c = bool(re.match(self.FLOAT_REGEX, inp))
            return any([bool(re.match(self.INTEGER_REGEX, inp)), bool(re.match(self.FLOAT_REGEX, inp))])
        except ValueError:
            return bool(re.match(self.STRING_REGEX, inp))

    @staticmethod
    def h(inp: str):
        return sum(map(ord, inp))

    def get_position(self, symbol_table, param: str) -> Tuple[int, int]:
        if param not in symbol_table[self.h(param)]:
            symbol_table[self.h(param)].append(param)
        return self.h(param), symbol_table[self.h(param)].index(param)

    def write_to_file(self):
        with open(self.output_file, "w") as f:
            f.write("CODIFICATION TABLE\n")
            f.write('\n'.join('{}: {}'.format(
                self.codification_table[x], x) for x in self.codification_table))
            f.write('\nIDENTIFIERS SYMBOL TABLE\n')
            f.write('\n'.join('{}: {}'.format(x, ' -> '.join(self.identifiers_symbol_table[x])) for x in
                              self.identifiers_symbol_table))
            f.write('\nCONSTANTS SYMBOL TABLE\n')
            f.write('\n'.join('{}: {}'.format(x, ' -> '.join(self.constants_symbol_table[x])) for x in
                              self.constants_symbol_table))
            f.write("\nPROGRAM INTERNAL FORM\n")
            f.write('\n'.join('{}: {}'.format(x[0], x[1])
                              for x in self.program_internal_form))

    def run(self):
        with open(self.input_file, 'r') as f:
            for index, line in enumerate(f.readlines()):
                tokens = Scanner.detect(line.strip())
                i = 0
                column = 0
                while i < len(tokens):
                    if self.is_keyword(tokens[i]) or self.is_operator(tokens[i]) or self.is_separator(tokens[i]):
                        if 0 < i < len(tokens) and tokens[i] == "-" and self.is_operator(tokens[i - 1]):
                            if self.is_number_constant(tokens[i + 1]):
                                to_be_added = tokens[i] + tokens[i + 1]
                                position = self.get_position(
                                    self.constants_symbol_table, to_be_added)
                                self.program_internal_form.append(
                                    (self.codification_table[self.CONSTANT], position))
                                i += 1
                                column += 2
                            else:
                                raise LexicalException(
                                    f"Unexpected token at {index}, {column}: {tokens[i]}")
                        else:
                            if i < len(tokens) - 1 and tokens[i] + tokens[i + 1] in self.COMPOUND_OPERATORS:
                                to_be_added = tokens[i] + tokens[i + 1]
                                i += 1
                            else:
                                to_be_added = tokens[i]
                            self.program_internal_form.append(
                                (self.codification_table[to_be_added], (-1, -1)))
                    elif self.is_identifier(tokens[i]):
                        position = self.get_position(
                            self.identifiers_symbol_table, tokens[i])
                        self.program_internal_form.append(
                            (self.codification_table[self.IDENTIFIER], position))
                    elif self.is_constant(tokens[i]):
                        position = self.get_position(
                            self.constants_symbol_table, tokens[i])
                        self.program_internal_form.append(
                            (self.codification_table[self.CONSTANT], position))
                    else:
                        raise LexicalException(
                            f"Unexpected token at {index}, {column}: {tokens[i]}")

                    column += len(tokens[i]) + 1
                    i += 1
            self.write_to_file()
            return self.program_internal_form
