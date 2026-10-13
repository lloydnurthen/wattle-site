// Countries, electricity networks and retailers for the register-interest form.
//
// Australia: there's no free national postcode → network table, so the postcode gives the
// state, and the form lists that state's networks (filling it in when there's only one).
// New Zealand: the form lists every lines company. Amber's site data gives the exact network
// for Australians once they connect; for New Zealand we ask (#23, #26).
// The same file is copied to wattle-site/register/networks.js; keep them in step.

export const COUNTRIES = { AU: "Australia", NZ: "New Zealand" };

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

// New Zealand's electricity distribution businesses (lines companies), A to Z.
export const NZ_NETWORKS = ["Alpine Energy", "Aurora Energy", "Buller Electricity", "Centralines",
  "Counties Energy", "EA Networks", "Eastland Network", "Electra", "Firstlight Network",
  "Horizon Networks", "MainPower", "Marlborough Lines", "Nelson Electricity", "Network Tasman",
  "Network Waitaki", "Northpower", "Orion", "OtagoNet", "PowerNet", "Powerco", "Scanpower",
  "The Lines Company", "Top Energy", "Unison", "Vector", "Waipa Networks", "WEL Networks",
  "Wellington Electricity", "Westpower"];

export const RETAILERS = {
  AU: ["Amber Electric", "AGL", "Origin", "EnergyAustralia", "Red Energy", "Alinta Energy", "Powershop",
    "Globird", "Another retailer"],
  NZ: ["Contact Energy", "Mercury", "Genesis Energy", "Meridian", "Electric Kiwi", "Flick Electric",
    "Octopus Energy", "Powershop", "Nova Energy", "Frank Energy", "Pulse Energy", "Another retailer"],
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

/** The Australian state for a postcode, or "" (New Zealand postcodes return "NZ"). */
export function stateFor(postcode, country = "AU") {
  if (!/^\d{4}$/.test(String(postcode || ""))) return "";
  if (country === "NZ") return "NZ";
  const n = Number(postcode);
  const hit = RANGES.find(([a, b]) => n >= a && n <= b);
  return hit ? hit[2] : "";
}

/** The networks to offer for a postcode. */
export function networksFor(postcode, country = "AU") {
  if (country === "NZ") return /^\d{4}$/.test(String(postcode || "")) ? NZ_NETWORKS : [];
  return NETWORKS[stateFor(postcode)] || [];
}

export const ALL_NETWORKS = [...new Set([...Object.values(NETWORKS).flat(), ...NZ_NETWORKS])];
