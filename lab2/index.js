var {
  parseGrammar,
  fromFiniteAutomata,
  showProductionsFor,
  isRegular
} = require("./regularGrammar");
var { parseFinite, fromRegularGrammar } = require("./finiteAutomata");
var { parseLine, readAllLines } = require("./utils");

const regularGrammarLines = [];
const finiteAutomataLines = [];
let finiteAutomata = {};
let grammar = {};
//  Grammar usage
//   We read the grammar from file 'ra'
readAllLines("rg", regularGrammarLines, () => {
  grammar = parseGrammar(regularGrammarLines);
  console.log(grammar);
  try {
    showProductionsFor(grammar, "A");
  } catch (e) {
    console.log(e);
  }
});

readAllLines("fa", finiteAutomataLines, () => {
  finiteAutomata = parseFinite(finiteAutomataLines);
  // rg -> fa
  if (isRegular(grammar)) {
    console.log("the grammar is regular");
    const finiteAutomata2 = fromRegularGrammar(grammar);
    console.log(finiteAutomata2);
  } else {
    console.log("the grammar is not regular");
  }
  // fa ->rg
  grammar2 = fromFiniteAutomata(finiteAutomata);
  console.log(grammar2);
});

// TODO: finish main + isRegular
