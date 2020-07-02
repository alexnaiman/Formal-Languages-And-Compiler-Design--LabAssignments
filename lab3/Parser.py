from Grammar import Grammar
from ParseTable import ParseTable


class Parser:
    def __init__(self, pif, codification_table):
        self.grammar = Grammar()
        self.pif = pif
        self.codification_table = codification_table
        self.first = dict()
        self.follow = dict()
        self.rules = []
        self.productions = dict()
        self.alpha = []
        self.beta = []
        self.pi = []
        self.generate_first()
        self.generate_follow()
        self.parse_table = ParseTable()
        self.create_parse_table()

    def generate_first(self):
        for non_terminal in self.grammar.N:
            self.first[non_terminal] = self.first_of(non_terminal)

    def generate_follow(self):
        for non_terminal in self.grammar.N:
            self.follow[non_terminal] = self.follow_of(
                non_terminal, non_terminal)

    def first_of(self, non_terminal):
        if non_terminal in self.first.keys():
            return self.first[non_terminal]
        temp = set()
        terminals = set(self.grammar.E)
        productions = self.grammar.get_productions_for_symbol_parser(
            non_terminal)
        for production in productions:
            rule = production[1]
            first = rule.split(" ")[0].strip()
            if first != non_terminal:
                if first == "*":
                    temp.add("*")
                elif first in terminals:
                    temp.add(first)
                else:
                    for f in self.first_of(first):
                        temp.add(f)
        return temp

    def follow_of(self, non_terminal, initial_non_terminal):
        if non_terminal in self.follow.keys():
            return self.follow[non_terminal]
        temp = set()
        terminals = set(self.grammar.E)
        productions = self.grammar.get_productions_containing_symbol_parser(
            non_terminal)
        if non_terminal == self.grammar.S:
            temp.add("$")
        for production in productions:
            start = production[0]
            rule = [var.strip() for var in production[1].split(" ")]
            rule_conflict = [non_terminal]
            # rule_conflict.append(non_terminal)
            for r in rule:
                rule_conflict.append(r)
            if non_terminal in rule and rule_conflict not in self.rules:
                self.rules.append(rule_conflict)
                index = rule.index(non_terminal)
                for operation in self.follow_operation(non_terminal, temp, terminals, start, rule, index,
                                                       initial_non_terminal):
                    temp.add(operation)
                sub_list = rule[index + 1:]
                if non_terminal in sub_list:
                    for op in self.follow_operation(non_terminal, temp, terminals, start, rule,
                                                    index + 1 +
                                                    sub_list.index(
                                                        non_terminal),
                                                    initial_non_terminal):
                        temp.add(op)
                self.rules.pop()
        return temp

    def follow_operation(self, non_terminal, temp, terminals, start, rule, index, initial_non_terminal):
        if index == len(rule) - 1:
            if start == non_terminal:
                return temp
            if initial_non_terminal != start:
                for follow in self.follow_of(start, initial_non_terminal):
                    temp.add(follow)
        else:
            next = rule[index + 1]
            if next in terminals:
                temp.add(next)
            else:
                if initial_non_terminal != next:
                    temp_first = set()
                    for first in self.first[next]:
                        temp_first.add(first)
                    if "*" in temp_first:
                        for operation in self.follow_of(next, initial_non_terminal):
                            temp.add(operation)
                        temp_first.remove("*")
                    for first in temp_first:
                        temp.add(first)
        return temp

    def numbering_productions(self):
        index = 1
        for production in self.grammar.P:
            self.productions[(production[0], production[1])] = index
            index += 1

    def create_parse_table(self):
        self.numbering_productions()
        symbols = self.grammar.E
        symbols.append("$")
        self.parse_table.put(("$", "$"), (["acc"], -1))
        for terminal in self.grammar.E:
            if terminal != "$":
                self.parse_table.put((terminal, terminal), (["pop"], -1))
        for production_key, production_value in self.productions.items():
            row_symbol = production_key[0]
            rule = [var.strip() for var in production_key[1].split(" ")]
            parse_table_value = (rule, production_value)
            for column_symbol in symbols:
                parse_table_key = (row_symbol, column_symbol)
                if rule[0] == column_symbol and column_symbol != "*":
                    self.parse_table.put(parse_table_key, parse_table_value)
                elif rule[0] in self.grammar.N and column_symbol in self.first[rule[0]]:
                    if not self.parse_table.contains_key(parse_table_key):
                        self.parse_table.put(
                            parse_table_key, parse_table_value)
                else:
                    if rule[0] == "*":
                        for b in self.follow[row_symbol]:
                            self.parse_table.put(
                                (row_symbol, b), parse_table_value)
                    else:
                        firsts = set()
                        for symbol in rule:
                            if symbol in self.grammar.N:
                                for s in self.first[symbol]:
                                    firsts.add(s)
                        if "*" in firsts:
                            for b in self.first[row_symbol]:
                                if b == "*":
                                    b = "$"
                                parse_table_key = (row_symbol, b)
                                if not self.parse_table.contains_key(parse_table_key):
                                    self.parse_table.put(
                                        parse_table_key, parse_table_value)

    def parse_sequence(self, symbols):
        self.init_stacks(symbols)
        go = True
        result = True
        while go:
            beta_head = self.peek_stack(self.beta)
            alpha_head = self.peek_stack(self.alpha)
            heads = (beta_head, alpha_head)
            parse_table_entry = self.parse_table.get(heads)
            if parse_table_entry[1] != -1:
                self.beta.pop()
                for symbol in parse_table_entry[0][::-1]:
                    if symbol != "*":
                        self.beta.append(symbol)
                self.pi.append(parse_table_entry[1])
            else:
                if parse_table_entry[0] == ["pop"]:
                    self.beta.pop()
                    self.alpha.pop()
                elif parse_table_entry[0] == ["acc"]:
                    return result
                else:
                    return not result

    def parse_pif(self):
        print(self.scan_source(self.pif))
        return self.parse_sequence(self.scan_source(self.pif))

    def init_stacks(self, symbols):
        self.alpha.clear()
        self.alpha.append("$")
        for symbol in symbols[::-1]:
            self.alpha.append(symbol)

        self.beta.clear()
        self.beta.append("$")
        self.beta.append(self.grammar.S)

        self.pi.clear()
        self.pi.append("*")

    @staticmethod
    def peek_stack(stack):
        if not stack:
            return None
        return stack[-1]

    @staticmethod
    def scan_source(pif):
        print(str(x[0]) for x in pif)
        return [str(x[0]) for x in pif]
