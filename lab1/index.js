var lineReader = require("line-reader");
var SimpleHashTable = require("simple-hashtable");

var {
  codification,
  reservedWords,
  operatorsOrSeparators
} = require("./config.js");

const [
  ,
  ,
  inputFile = "myScripts/test.myjs",
  outputFile = "fip.txt"
] = process.argv;

const lines = [];
const symbolTableConstants = new SimpleHashTable();
const symbolTableVariables = new SimpleHashTable();
let currentPositionConstants = 0;
let currentPositionIdentifiers = 0;
const programInternalForm = [];

const main = () => {
  readAllLines(analyzeCode);
};

/**
 *  This function reads alll the lines from the input file and pushes them into an array
 * @param {function} callback function that is called after all the lines are read
 */
const readAllLines = callback => {
  lineReader.eachLine(inputFile, function(line, last) {
    lines.push(line);
    if (last) {
      callback();
    }
  });
};

/**
 * Function that starts analyzing the code from the given inputFile
 */
const analyzeCode = () => {
  try {
    lines.forEach((line, index) => {
      tokens = tokenify(line, index);
      tokens.forEach(token => {
        if (isReservedWord(token) || isOperatorOrSeparator(token)) {
          programInternalForm.push({
            tokenCode: codification[token],
            position: -1
          });
        } else if (isConstant(token)) {
          if (!symbolTableConstants.containsKey(token)) {
            symbolTableConstants.put(token, currentPositionConstants);
            currentPositionConstants++;
          }
          programInternalForm.push({
            tokenCode: 1,
            position: symbolTableConstants.get(token)
          });
        } else if (isIdentifier(token)) {
          if (!symbolTableVariables.containsKey(token)) {
            symbolTableVariables.put(token, currentPositionIdentifiers);
            currentPositionIdentifiers++;
          }
          programInternalForm.push({
            tokenCode: 0,
            position: symbolTableVariables.get(token)
          });
        }
      });
    });
  } catch (error) {
    console.log(error);
    console.log("End of execution");
    return;
  }
  console.log("Program internal form");
  console.table(programInternalForm);

  console.log("SymbolTable Variables");
  printHashTable(symbolTableVariables);
  console.log("SymbolTable Constants");
  printHashTable(symbolTableConstants);

  console.log("end of execution");
};

/**
 * Function that splits and gets all tokens from a given line
 * @param {string} line line that needs to be tokenized
 * @param {number} index  line's index on the file
 * @return {array}  array of strings which are the tokens obtained
 * @throws {object} object which contains details about unexpected tokens
 */
const tokenify = (line, index) => {
  try {
    console.log(
      line
        .split(
          // positive look behind                   // positive look ahead
          /(<=)|(>=)|(?<=[\<\>\,\;\-\+\/\*\(\)\[\] ])|(?=[\<\>\,\;\-\+\/\*\(\)\[\] ])|'"(.*?)"'|""|''/
        )
        .filter(a => a !== undefined && a !== " ")
        .map(fixTokens)
    );
    return line
      .split(
        // positive look behind                   // positive look ahead
        /(<=)|(>=)|(?<=[\<\>\,\;\-\+\/\*\(\)\[\] ])|(?=[\<\>\,\;\-\+\/\*\(\)\[\] ])|'"(.*?)"'/
      )
      .filter(a => a !== undefined && a !== " ")
      .map(fixTokens);
  } catch (error) {
    position = line.indexOf(error.token);
    console.log(
      `\x1b[31mUnexpected token at line ${index + 1}, column ${position}\x1b[0m`
    );
    throw error;
  }
};

/**
 * Function that check if the tokens are correct
 * @param {string} token - the token we want to verify if it is correct
 * @return {string} returns the token after it passed the checks
 * @throws {object} object which contains details about unexpected tokens
 */
const fixTokens = token => {
  if (
    !isReservedWord(token) &&
    !isIdentifier(token) &&
    !isConstant(token) &&
    !isOperatorOrSeparator(token)
  ) {
    throw { hasError: true, token };
  }
  return token;
};
/**
 * Function that checks if the given token is a reserved word
 * @param {string} token - the token we want to verify if it is correct
 * @returns {boolean} - true if it is correct, false otherwise
 */
const isReservedWord = token => !!reservedWords[token];

/**
 * Function that checks if the given token is a identifier
 * @param {string} token - the token we want to verify if it is correct
 * @returns {boolean} - true if it is correct, false otherwise
 */
const isIdentifier = token => /^[a-zA-Z_$][a-zA-Z_$0-9]{0,7}$/.test(token);

/**
 * Function that checks if the given token is a constant
 * @param {string} token - the token we want to verify if it is correct
 * @returns {boolean} - true if it is correct, false otherwise
 */
const isConstant = token =>
  /^[-+]?[1-9]\d*$|0|\s/.test(token) || /'.*'|".*"/.test(token);

/**
 * Function that checks if the given token is a separator or operator
 * @param {string} token - the token we want to verify if it is correct
 * @returns {boolean} - true if it is correct, false otherwise
 */
const isOperatorOrSeparator = token => !!operatorsOrSeparators[token];
/**
 *  Function that formats and prints a symbol table
 * @param {SimpleHashTable} symbolTable - the symbol table we want to print
 */
const printHashTable = symbolTable =>
  console.table(
    symbolTable.keys().map(k => ({ position: symbolTable.get(k), symbol: k }))
  );
main();
