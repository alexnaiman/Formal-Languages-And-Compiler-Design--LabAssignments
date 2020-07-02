# Alphabet:

* Uppercase and lowercase letters of the  English alphabet (A-Z and a-z);
* Underscore character '_';
* Decimal digits(0-9);


# Lexic

a) Special symbols:

- operators: `+ - * / % < <== === > >== !==`
- separators: `{} () ; space \n \n\r \t \r`
- reserved words: `read write if else while begin end int string array`
		
b) Identifiers:

	non_zero_digit = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9".
	zero_digit = "0".
	digit = zero_digit | non_zero_digit.
	alpha_character = "a" | "A" | "b" | "B" | "c" | "C" | "d" | "D" | "e" | "E" | "f" | "F" | "g" | "G" | "h" | "H" | "i" | "I" | "j" | "J" | "k" | "K" | "l" | "L" | "m" | "M" | "n" | "N" | "o" | "O" | "p" | "P" | "q" | "Q" | "r" | "R" | "s" | "S" | "t" | "T" | "u" | "U" | "v" | "V" | "w" | "W" | "x" | "X" | "y" | "Y" | "z" | "Z".
	underscore = "_".
	non_digit = underscore | alpha_character.
	identifier = non_digit{non_digit | digit}.

c) Constants:

		non_zero_natural_number = non_zero_digit {digit}.
		natural_number = non_zero_natural_number | zero_digit.
		
		number = ["-"] natural_number.
		string = "'" {non_digit | digit} "'".

# Syntax:

	program = "begin" {declaration} {statement} "end".
	declaration = variable_declaration | array_declaration.
	statement = assignment | input | output | conditional | loop.

	input = "read" "(" identifier ")" ";".
	output = "write" "(" expression_member ")" ";".
	
	assignment = identifier "=" expression ";".
	
	conditional = "if" "(" condition ")" "{" {statement} "}" ["else" "{" {statement} "}"] ";".
	loop = "while" "(" condition ")" "{" {statement} "}" ";".
	condition = expression relation expression.
	
	
	
	variable_declaration = type identifier ";".
	array_declaration = "array" type identifier "[" non_zero_natural_number "] ";".
	
	type = "int" | "string".
	expression = expression_member_variable {expression_operator expression_member_variable}.
	expression_operator = "+" | "-" | "*" | "/" | "%".
	expression_member = identifier | number | string.
	expression_member_variable = ["("] expression_member {expression_operator expression_member} [")"].
	relation = "<" | "<=" | ">" | ">=" | "==" | "!=".


# Tokentype: 	code

    "identifier": 0,
    "constant": 1,
    "read": 2,
    "write": 3,
    "if": 4,
    "else": 5,
    "while": 6,
    "begin": 7,
    "end": 8,
    "int": 9,
    "array": 10,
    "string": 11,
    "{": 12,
    "}": 13,
    "(": 14,
    ")": 15,
    ";": 16,
    " ": 17,
    "[": 18,
    "]": 19,
    "\t": 20,
    "\n\r": 21,
    "\n": 22,
    "\r": 23,
    "+": 24,
    "-": 25,
    "*": 26,
    "/": 27,
    "%": 28,
    "===": 29,
    ">==": 30,
    "<==": 31,
    "!==": 32,
    "=": 33,
    ">": 34,
    "<": 35