var lineReader = require("line-reader");

/**
 *  This function parses a line of form "X = { a, b, c }" to [a,b,c]
 * @param {function} callback function that is called after all the lines are read
 * @return {array} the line parsed into an array
 */
const parseLine = line =>
  line
    .split("=")[1]
    .split(/,|{|}/)
    .map(k => k.trim())
    .filter(k => k);
/**
 *  This function reads alll the lines from the input file and pushes them into an array
 * @param {function} callback function that is called after all the lines are read
 * @param {string} inputFile file from which we read
 * @lines {array} object in which we store the lines
 */
const readAllLines = (inputFile, lines, callback) => {
  lineReader.eachLine(inputFile, function(line, last) {
    lines.push(line.trim());
    if (last) {
      callback();
    }
  });
};
module.exports = { parseLine, readAllLines };
