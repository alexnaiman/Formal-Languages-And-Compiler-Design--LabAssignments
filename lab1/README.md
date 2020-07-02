# Lab 1


### Requirements (the exact problem statement)

> 			Laboratory Work no. 1

>Statement: Considering a small programming language (that we shall call mini-langauge), you have to write a scanner (lexical analyzer). The assignment can be divided in two parts:

> 1. Minilanguage Specification

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


	... example from course
