// Postcode → state, and the electricity networks in each state.
//
// There's no free national postcode → network table we can use, so the form narrows
// the choice to the state's networks and fills it in when the state has only one.
// Amber's site data gives the exact network once someone connects (#23).
// Copied from lloydnurthen/wattle interest/src/networks.js; keep them in step.

export const NETWORKS = {
  NSW: ["Ausgrid", "Endeavour Energy", "Essential Energy"],
  ACT: ["Evoenergy"],
  VIC: ["CitiPower", "Powercor", "Jemena", "United Energy", "AusNet Services"],
  QLD: ["Energex", "Ergon Energy"],
  SA: ["SA Power Networks"],
  WA: ["Western Power", "Horizon Power"],
  TAS: ["TasNetworks"],
  NT: ["Power and Water"],
};

const RANGES = [
  // [from, to, state] — Australia Post ranges; earlier rows win.
  [200, 299, "ACT"], [2600, 2618, "ACT"], [2900, 2920, "ACT"],
  [800, 999, "NT"],
  [1000, 2599, "NSW"], [2619, 2899, "NSW"], [2921, 2999, "NSW"],
  [3000, 3999, "VIC"], [8000, 8999, "VIC"],
  [4000, 4999, "QLD"], [9000, 9999, "QLD"],
  [5000, 5999, "SA"],
  [6000, 6999, "WA"],
  [7000, 7999, "TAS"],
];

export function stateFor(postcode) {
  if (!/^\d{4}$/.test(String(postcode || ""))) return "";
  const n = Number(postcode);
  const hit = RANGES.find(([a, b]) => n >= a && n <= b);
  return hit ? hit[2] : "";
}

export function networksFor(postcode) {
  return NETWORKS[stateFor(postcode)] || [];
}

export const ALL_NETWORKS = [...new Set(Object.values(NETWORKS).flat())];
