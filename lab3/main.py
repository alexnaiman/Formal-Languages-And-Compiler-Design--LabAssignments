from Grammar import Grammar
from Parser import Parser
from Scanner import Scanner, generate_codification_table
from functools import reduce


def parse_sequence(parser):
    user_input = input()
    sequence = user_input.strip().split(" ")
    result = parser.parse_sequence(sequence)
    if result is True:
        print("Sequence: \"", user_input, "\" is accepted. Parsing tree is: ")
        print_derivations_strings(parser)
    else:
        print("Sequence: \"", user_input, "\" is not accepted")


def print_derivations_strings(parser):
    productions_number = parser.pi
    my_productions = []
    for number in productions_number[1:]:
        for key, value in parser.productions.items():
            if value == number:
                my_productions.append(key)

    my_productions = list(reversed(my_productions))
    first, rhs = my_productions.pop()

    s = first + ' -> ' + rhs + " -> "
    print(s)
    derivation = rhs.split()
    while len(my_productions) > 0:
        lhs, rhs = my_productions.pop()
        position = next(i for i, v in enumerate(
            derivation) if lhs == v)
        derivation = derivation[:position] + \
            rhs.split() + derivation[position + 1:]
        s = " -> " + reduce(lambda x, y: x + " " + y,
                            filter(lambda x: x != "*", derivation))
        print(s, end=" ")
    print('*')


def parse_pif(parser):
    result = parser.parse_pif()
    if result is True:
        print("PIF parsed successfully. Parsing tree is: ")
        print_derivations_strings(parser)

    else:
        print("PIF is not accepted")


if __name__ == '__main__':

    while True:
        try:
            print('1. Grammar menu\n2. Parser menu\n0. Exit')
            option = input('Choose option: ')
            if int(option) == 1:
                grammar = Grammar()
                while True:
                    try:
                        print('1. Display set of non-terminals\n'
                              '2. Display set of terminals\n'
                              '3. Display set of productions\n'
                              '4. Display the productions of a given non-terminal\n'
                              '5. Display starting symbol\n'
                              '6.Go back')
                        option = input('Choose option: ')
                        if int(option) == 1:
                            print(grammar.get_non_terminals())
                        elif int(option) == 2:
                            print(grammar.get_terminals())
                        elif int(option) == 3:
                            print(grammar.get_productions())
                        elif int(option) == 4:
                            symbol = input('enter symbol: ')
                            print(grammar.get_productions_for_symbol(symbol))
                        elif int(option) == 5:
                            print(grammar.S)
                        elif int(option) == 6:
                            break
                    except Exception as e:
                        print(e)
            elif int(option) == 2:
                scanner = Scanner(generate_codification_table(),
                                  "nipy_example", "output")
                parser = Parser(scanner.run(), generate_codification_table())
                while True:
                    try:
                        print('1. Display FIRST set\n'
                              '2. Display FOLLOW set\n'
                              '3. Create parse table\n'
                              '4. Parse sequence\n'
                              '5. Parse PIF\n'
                              '6.Go back')
                        option = input('Choose option: ')
                        if int(option) == 1:
                            print(parser.first)
                        elif int(option) == 2:
                            print(parser.follow)
                        elif int(option) == 3:
                            print(parser.parse_table)
                        elif int(option) == 4:
                            parse_sequence(parser)
                        elif int(option) == 5:
                            parse_pif(parser)
                    except Exception as e:
                        print(e)
            elif int(option) == 0:
                exit(0)
            else:
                raise Exception("invalid option!")
        except Exception as e:
            print(e)
