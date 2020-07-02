var lineReader = require("line-reader");
var { parseLine, readAllLines } = require("./utils");
const lines = [];
const inputFile = "./fa";
/**
 * Finite automata object structure
 * Q -> states
 * E -> alphabet
 * q0 ->
 * F ->
 * S ->
 */

const finiteAutomata = {
  Q: [],
  E: [],
  q0: "",
  F: [],
  S: []
};

const parseFinite = lines => {
  let finiteAutomata = {};
  [Q, E, q0, F, ...S] = lines;
  finiteAutomata.Q = parseLine(Q);
  finiteAutomata.E = parseLine(E);
  finiteAutomata.F = parseLine(F);
  finiteAutomata.q0 = q0
    .trim()
    .split(/q0[ ].*=| /)
    .filter(q => q)[0];
  finiteAutomata.S = S.slice(1, -1)
    .map(k =>
      k
        .split(/(\s)|,/)
        .filter(k => k)
        .map(k => k.replace(/,|\(|\)|->/, ""))
        .filter(k => k.trim())
    )
    .map(item => ({ state1: item[0], route: item[1], state2: item[2] }));

  return { ...finiteAutomata };
};

const isState = (finiteAutomata, state) => finiteAutomata.Q.includes(state);

const getTransitionsFor = (finiteAutomata, state) => {
  if (!isState(finiteAutomata, state))
    throw new Error("Can only get transitions for states");
  return finiteAutomata.S.filter(trans => trans.state1 === state);
};

const printTransitionsFor = (finiteAutomata, state) => {
  const transitions = getTransitionsFor(finiteAutomata, state);
  return `{\n${transitions
    .map(k => `(${k.state1}, ${k.route}) -> ${k.state2}`)
    .join(",\n")}\n};`;
};

const fromRegularGrammar = regularGrammar => {
  const Q = [...regularGrammar.N, "K"];
  const E = regularGrammar.E;
  const q0 = regularGrammar.S;
  const F = ["K"];

  const S = [];

  regularGrammar.P.forEach(production => {
    let state2 = "K";
    const { lhs: state1, rhs } = production;
    if (state1 === q0 && rhs[0] === "E") {
      F.push(q0);
      return;
    }
    const route = rhs[0];

    if (rhs.length === 2) {
      state2 = rhs[1];
    }
    S.push({ state1, route, state2 });
  });

  return { Q, E, q0, F, S };
};

module.exports = { fromRegularGrammar, parseFinite, printTransitionsFor };
