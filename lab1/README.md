# Lab 1


### Requirements (the exact problem statement)

> 			Laboratory Work no. 1

Statement: Considering a small programming language (that we shall call mini-langauge), you have to write a scanner (lexical analyzer). The assignment can be divided in two parts:

1. Minilanguage Specification

	The minilanguage should be a restricted form of a known programming language, and should contain the following:
- 2 simple data types and a user-defined type
- statements:
	- assignment
	- input/output
	- conditional
	- loop
- some conditions will be imposed on the way the identifiers and constants can be formed.

2. Scanner implementation

	The scanner input will be a text file containind the source program, and will produce as output the following:
	- PIF - Program Internal Form
	- ST  - Symbol Table
In addition, the program should be able to determine the lexical errors, specifying the location, and, if possible, the type of the error.

The scanner assignment will be diferentiated based on:
	1. Identifiers:
		a. length at most 8 characters
		b. arbitrary length, no more than 250 characters
	2. Symbol Table:
		a. unique for identifiers and constants
		b. separate tables for indentifiers, respectively 
		   constants
	3. Symbol Table Organization:
		a. lexicographically sorted table
		b. lexicographically binary tree
		c. hashing table

Documenting the scanner program is COMPULSORY!


IMPORTANT:
	  Each week delay will be penalized with one point, and delays more than 2 weeks are NOT ACCEPTED!
	  Laboratory work is taken into consideration at the final mark, and acceptance at the final exam is conditioned by the delivery of all laboratory work.


Example:
Language Specification:
 1 .Language Definition:
  1.1 Alphabet:
  1.1.a. Upper (A-Z) and lower case letters (a-z) of the English alphabet
      b. Underline character '_';
      c. Decimal digits (0-9);
  Lexic:
      a.Special symbols, representing:
	 - operators + - * / := < <= = >=
	 - separators [ ] { }  : ; space
	 - reserved words:
	    	array  char  const do else  if int  of program read 
		then var while write
      b.identifiers
	   -a sequence of letters and  digits, such that the first charater is a letter; the rule is:
	     identifier ::= letter | letter{letter}{digit}
	     letter ::= "A" | "B" | . ..| "Z"
	     digit ::= "0" | "1" |...| "9"
      c.constants
	 1.integer - rule:
	      noconst:=+no|-no|no
	      no:=digit{no}
	 2.character
	     character:='letter'|'digit'
	 3.string
	      constchar:="string"
	      string:=char{string}
	      char:=letter|digit
 2.2 Syntax:
	The words - predefined tokens are specified between " and ":	
a) Sintactical rules:
    program ::= "VAR" decllist ";" cmpdstmt "."
   decllist ::= declaration | declaration ";" decllist
declaration ::= IDENTIFIER ":" type
      type1 ::= "BOOLEAN" | "CHAR" | "INTEGER" | "REAL"
  arraydecl ::= "ARRAY" "[" nr "]" "OF" type1
      type  ::= type1|arraydecl
   cmpdstmt ::= "BEGIN" stmtlist "END"
   stmtlist ::= stmt | stmt ";" stmtlist
       stmt ::= simplstmt | structstmt
  simplstmt ::= assignstmt | iostmt
 assignstmt ::= IDENTIFIER ":=" expression
 expression ::= expression "+" term | term
       term ::= term "*" factor | factor
     factor ::= "(" expression ")" | IDENTIFIER
     iostmt ::= "READ" | "WRITE" "(" IDENTIFIER ")"
 structstmt ::= cmpdstmt | ifstmt | whilestmt
     ifstmt ::= "IF" condition "THEN" stmt ["ELSE" stmt]
  whilestmt ::= "WHILE" condition "DO" stmt
  condition ::= expression RELATION expression
b) lexical rules:
 IDENTIFIER ::= letter | letter{letter}{digit}
     letter ::= "A" | "B" | . ..| "Z"
      digit ::= "0" | "1" |...| "9"
   RELATION ::= "<" | "<=" | "=" | "<>" | ">=" | ">"

The tokens are codified according to the following table:
- identifiers	- code 0
- constants	- code  1
- reserved words: each word has its own code
- operators: each operator has its own code
- separators: each separator has its own code
Codification:
-------------------------
| Token type	|   code |
-------------------------
| identifier	|    0  |
-------------------------
| constant	|    1  |
-------------------------
| program       |    2  |
-------------------------
|  array	|    3  |
-------------------------
|    of		|    4  |
-------------------------
|    var	|    5  |
-------------------------
|  integer      |    6  |
-------------------------
|  real  	|    7  |
-------------------------
| boolean       |    8  |
-------------------------
| begin 	|    9  |
-------------------------
| end		|   10  |
-------------------------
|read		|   11  |
-------------------------
|write 		|   12  |
-------------------------
| for		|   13  |
-------------------------
| to		|   14  |
-------------------------
| do 		|   15  |
-------------------------
| if		|   16  |
-------------------------
| then		|   17  |
-------------------------
|  else  	|   18  |
-------------------------
| and		|   19  |
-------------------------
|  or		|   20  |
-------------------------
|  not		|   21  |
-------------------------
| :		|   22  |
-------------------------
| ;		|   23  |
-------------------------
| ,     	|   24  |
-------------------------
| .		|   25  |
-------------------------
| +		|   26  |
-------------------------
| * 		|   27  |
-------------------------
| (		|   28  |
-------------------------
| )		|   29  |
-------------------------
| [		|   30  |
-------------------------
| ]     	|   31  |
-------------------------
| -		|   32  |
-------------------------
| <     	|   33  |
-------------------------
| >		|   34  |
-------------------------
| =		|   35  |
-------------------------
| := 		|   36  |
-------------------------

... (documentation for the scanner application)
