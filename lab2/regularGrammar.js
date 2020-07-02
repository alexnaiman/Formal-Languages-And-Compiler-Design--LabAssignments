var { parseLine, readAllLines } = require("./utils");

// const regularGrammar = {
//   N: [],
//   E: [],
//   S: "",
//   P: []
// };

const parseGrammar = lines => {
  let regularGrammar = {};
  const [N, E, S, ...P] = lines;

  regularGrammar.N = parseLine(N);
  regularGrammar.E = parseLine(E);
  regularGrammar.S = S.trim()
    .split(/q0[ ].*=| /)
    .filter(q => q)[0];
  regularGrammar.P = P.slice(1, -1)
    .map(k =>
      k
        .split(/(\s)|,/)
        .filter(k => k)
        .map(k => k.replace(/,|\(|\)|->|\|/, ""))
        .filter(k => k.trim())
    )
    .map(([lhs, ...rhs]) => rhs.map(k => ({ lhs, rhs: k })))
    .reduce((a, b) => [...a, ...b]);
  return regularGrammar;
};

const fromFiniteAutomata = finiteAutomata => {
  const N = finiteAutomata.Q;
  const E = finiteAutomata.E;
  const S = finiteAutomata.q0;
  const P = [];

  if (finiteAutomata.F.indexOf(finiteAutomata.q0) > -1) {
    P.push({ lhs: finiteAutomata.q0, rhs: "E" });
  }

  finiteAutomata.S.forEach(transition => {
    const { state1, route, state2 } = transition;
    P.push({ lhs: state1, rhs: route + state2 });
    // console.log(state1);
    if (finiteAutomata.F.indexOf(state2) > -1) {
      P.push({ lhs: state1, rhs: route });
    }
  });
  return { N, E, P, S };
};

const isTerminal = (regularGrammar, terminal) =>
  regularGrammar.E.indexOf(terminal) > -1;

const isNonTerminal = (regularGrammar, nonTerminal) =>
  regularGrammar.N.indexOf(nonTerminal) > -1;

const getProductionsFor = (regularGrammar, nonTerminal) => {
  if (!isNonTerminal(regularGrammar, nonTerminal)) {
    throw new Error("Can only show productions for non-terminals");
  }
  return regularGrammar.P.filter(prod => prod.lhs === nonTerminal);
};

const showProductionsFor = (regularGrammar, nonTerminal) => {
  productions = getProductionsFor(regularGrammar, nonTerminal);
  console.log(productions.map(k => `${k.lhs} -> ${k.rhs}`).join(", "));
};

const isRegular = regularGrammar => {
  const usedInRhs = {};
  const notAllowedInRhs = [];

  const intermediate = regularGrammar.P.every(rule => {
    const { lhs, rhs } = rule;
    let hasTerminal = false;
    let hasNonTerminal = false;
    if (rhs.length > 2) return false;
    // console.log;
    for (let i = 0; i < rhs.split("").length; i++) {
      if (isNonTerminal(regularGrammar, rhs[i])) {
        usedInRhs[rhs[i]] = true;
        hasNonTerminal = true;
      } else if (isTerminal(regularGrammar, rhs[i])) {
        if (hasNonTerminal) {
          return false;
        }
        hasTerminal = true;
      }
      if (rhs[i] === "E") {
        notAllowedInRhs.push(lhs);
      }
    }
    if (hasNonTerminal && !hasTerminal) return false;
    return true;
  });
  console.log(intermediate);

  const intermediate2 = notAllowedInRhs.every(k => !usedInRhs[k]);

  return intermediate && intermediate2;
};

module.exports = {
  fromFiniteAutomata,
  parseGrammar,
  isTerminal,
  isNonTerminal,
  isRegular,
  showProductionsFor
};
