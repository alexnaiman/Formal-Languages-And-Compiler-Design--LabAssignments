class Grammar:
    def __init__(self):
        self.read_grammar("grammar-seminar")
        # self.read_grammar("my_grammar")

    def __str__(self):
        return 'N = {' + ', '.join(self.N) + '}\n' \
               + 'E = {' + ', '.join(self.E) + '}\n' \
               + 'P = {' + ', '.join([' -> '.join(prod) for prod in self.P]) + '}\n' \
               + 'S = ' + str(self.S) + '\n'

    def is_terminal(self, element):
        return element in self.E

    def is_non_terminal(self, element):
        return element in self.N

    def get_terminals(self):
        return 'E = {' + ', '.join(self.E) + '}\n'

    def get_non_terminals(self):
        return 'N = {' + ', '.join(self.N) + '}\n'

    def get_productions(self):
        return 'P = {' + ',\n '.join([' -> '.join(prod) for prod in self.P]) + '}'

    def get_productions_for_symbol(self, non_terminal):
        rules = []
        if non_terminal in self.E:
            raise Exception('Cannot show productions for terminals')
        elif non_terminal not in self.N:
            raise Exception(
                'Can show productions only for valid non-terminals')
        for rule in self.P:
            lhs, rhs = rule
            if lhs == non_terminal:
                rules.append(rule)
        return '{' + ', '.join([' -> '.join(rule) for rule in rules]) + '}\n'

    def get_productions_for_symbol_parser(self, non_terminal):
        rules = []
        if non_terminal in self.E:
            raise Exception('Cannot show productions for terminals')
        elif non_terminal not in self.N:
            raise Exception(
                'Can show productions only for valid non-terminals')
        for rule in self.P:
            lhs, rhs = rule
            if lhs == non_terminal:
                rules.append(rule)
        return rules

    def get_productions_containing_symbol_parser(self, non_terminal):
        rules = []
        if non_terminal in self.E:
            raise Exception('Cannot show productions for terminals')
        elif non_terminal not in self.N:
            raise Exception(
                'Can show productions only for valid non-terminals')
        for rule in self.P:
            lhs, rhs = rule
            symbols = [var.strip() for var in rhs.split(" ")]
            if non_terminal in symbols:
                rules.append(rule)
        return rules

    @staticmethod
    def parse_rules(line):
        rules = []
        for rule in line:
            lhs, rhs = rule.strip().split("->")
            for value in rhs.split('|'):
                rules.append((lhs.strip(), value.strip()))
        return rules

    def read_grammar(self, file_name):
        with open(file_name, "r") as f:
            self.N = [s.strip() for s in f.readline().split(" ")]
            self.E = [s.strip() for s in f.readline().split(" ")]
            self.S = f.readline().strip()
            self.P = Grammar.parse_rules([s.strip() for s in f.readlines()])
