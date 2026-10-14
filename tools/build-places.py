#!/usr/bin/env python3
"""Build register/places/*.json: postcode -> suburbs, for the register form's suburb list.

Sources:
- Australia: GeoNames postal codes (https://www.geonames.org/, CC BY 4.0), as converted by
  https://github.com/zauberware/postal-codes-json-xml-csv (data/AU.zip).
- New Zealand: GeoNames gives only one place per postcode, so suburbs come from Open NZ
  Postcodes' street_postcodes (https://github.com/s01ipsist/open_nz_postcodes, CC0): every
  road with its postcode and LINZ suburb. A suburb is listed for a postcode when at least two
  of its roads have that postcode (one stray road isn't enough). GeoNames fills in postcodes
  with no roads (PO boxes, rural).
Usage: python3 tools/build-places.py zipcodes.au.csv zipcodes.nz.csv path/to/open_nz_postcodes/street_postcodes
Australia is split by the postcode's first digit (au-0.json ... au-9.json); New Zealand is one file.
The credit line is on the register page (CC BY 4.0 needs it).
"""
import csv, json, sys
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "register" / "places"

def load(path):
    places = defaultdict(set)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            code, place = row["zipcode"].strip().zfill(4), row["place"].strip()
            if len(code) == 4 and code.isdigit() and place:
                places[code].add(place)
    return {k: sorted(v) for k, v in sorted(places.items())}

def write(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

# New Zealand town -> lines company (electricity distribution business), for towns that sit
# wholly in one network. Postcodes whose roads are mostly in one of these towns get their lines
# company filled in on the form, with "Not right? Choose another" next to it. Anything not
# here (rural areas, Nelson city, which is split, and the like) asks the person.
# Best knowledge, Oct 2026; correct it when someone says it's wrong.
TOWN_LINES = {}
for network, towns in {
    "Vector": "Auckland, Whangaparaoa, Orewa, Silverdale, Waiheke Island, Kumeu, Takanini",
    "Counties Energy": "Pukekohe, Waiuku, Tuakau",
    "Northpower": "Whangarei, Dargaville, Ruakaka, Waipu, Mangawhai, Hikurangi, Maungaturoto",
    "Top Energy": "Kerikeri, Kaitaia, Kaikohe, Kawakawa, Russell, Awanui, Moerewa, Okaihau, Kaeo, Mangonui",
    "WEL Networks": "Hamilton, Huntly, Ngaruawahia, Raglan, Te Kauwhata",
    "Waipa Networks": "Cambridge, Te Awamutu",
    "The Lines Company": "Te Kuiti, Otorohanga, Taumarunui, Piopio",
    "Unison": "Rotorua, Taupo, Turangi, Napier, Hastings, Havelock North, Clive",
    "Horizon Networks": "Whakatane, Opotiki, Kawerau, Edgecumbe, Murupara, Taneatua, Matata",
    "Firstlight Network": "Gisborne, Wairoa, Tolaga Bay, Ruatoria",
    "Centralines": "Waipukurau, Takapau, Otane, Porangahau",
    "Scanpower": "Dannevirke, Woodville",
    "Powerco": ("Tauranga, Papamoa, Mount Maunganui, Te Puke, Katikati, Omokoroa, Waihi Beach, Morrinsville, "
                "Matamata, Te Aroha, Thames, Paeroa, Waihi, Whitianga, Coromandel, Whangamata, Ngatea, Putaruru, "
                "Tirau, Tokoroa, New Plymouth, Stratford, Hawera, Inglewood, Waitara, Eltham, Opunake, Patea, "
                "Palmerston North, Feilding, Ashhurst, Whanganui, Marton, Bulls, Pahiatua, Eketahuna, Masterton, "
                "Carterton, Greytown, Featherston, Martinborough"),
    "Electra": "Paraparaumu, Waikanae, Otaki, Levin, Foxton, Shannon",
    "Wellington Electricity": "Wellington, Lower Hutt, Upper Hutt, Porirua",
    "Network Tasman": "Richmond, Motueka, Takaka, Wakefield, Brightwater, Mapua, Murchison, Collingwood",
    "Marlborough Lines": "Blenheim, Picton, Renwick, Havelock, Seddon",
    "Westpower": "Greymouth, Hokitika, Reefton, Runanga, Ross",
    "Buller Electricity": "Westport, Karamea, Cape Foulwind",
    "Orion": ("Christchurch, Lyttelton, Akaroa, Little River, Diamond Harbour, Governors Bay, Rolleston, "
              "Lincoln, Prebbleton, Darfield, Leeston"),
    "MainPower": "Rangiora, Kaiapoi, Woodend, Oxford, Amberley, Hanmer Springs, Kaikoura, Culverden, Cheviot",
    "EA Networks": "Ashburton, Methven, Rakaia",
    "Alpine Energy": "Timaru, Temuka, Geraldine, Pleasant Point, Fairlie, Twizel, Lake Tekapo, Waimate",
    "Network Waitaki": "Oamaru, Kurow, Duntroon, Hampden, Moeraki",
    "Aurora Energy": ("Dunedin, Mosgiel, Port Chalmers, Waikouaiti, Queenstown, Arrowtown, Wanaka, Lake Hawea, "
                      "Cromwell, Alexandra, Roxburgh"),
    "OtagoNet": "Balclutha, Milton, Lawrence, Owaka, Clinton, Kaitangata, Middlemarch",
    "PowerNet": ("Invercargill, Bluff, Gore, Winton, Te Anau, Riverton/Aparima, Otautau, Mataura, Lumsden, "
                 "Tuatapere, Wyndham, Edendale"),
}.items():
    for town in towns.split(","):
        TOWN_LINES[town.strip()] = network


def load_nz_lines(folder):
    """postcode -> lines company, only where 80%+ of the postcode's roads are in towns of one network."""
    roads = defaultdict(lambda: defaultdict(int))
    for path in sorted(Path(folder).glob("*.csv")):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                code = (row.get("postcode") or "").strip().zfill(4)
                if len(code) != 4 or not code.isdigit():
                    continue
                town = (row.get("city") or "").split(",")[0].strip()
                roads[code][TOWN_LINES.get(town, "?")] += 1
    out = {}
    for code, by in roads.items():
        total = sum(by.values())
        best = max((n, k) for k, n in by.items() if k != "?") if any(k != "?" for k in by) else (0, None)
        if best[1] and best[0] / total >= 0.8:
            out[code] = best[1]
    return dict(sorted(out.items()))


def load_nz_streets(folder):
    counts = defaultdict(lambda: defaultdict(int))
    for path in sorted(Path(folder).glob("*.csv")):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                code = (row.get("postcode") or "").strip().zfill(4)
                if len(code) != 4 or not code.isdigit() or code == "0000":
                    continue
                for place in (row.get("locality") or "").split(","):
                    if place.strip():
                        counts[code][place.strip()] += 1
    out = {}
    for code, places in counts.items():
        keep = [p for p, n in places.items() if n >= 2] or [max(places, key=places.get)]
        out[code] = set(keep)
    return out

OUT.mkdir(parents=True, exist_ok=True)
au, nz = load(sys.argv[1]), load(sys.argv[2])
if len(sys.argv) > 3:
    streets = load_nz_streets(sys.argv[3])
    for code, places in streets.items():
        nz[code] = sorted(places | set(nz.get(code, [])) if len(places) < 3 else places)
    nz = dict(sorted(nz.items()))
    lines = load_nz_lines(sys.argv[3])
    write("nz-lines.json", lines)
    print(f"New Zealand lines company known for {len(lines)} postcodes")
for d in "0123456789":
    write(f"au-{d}.json", {k: v for k, v in au.items() if k[0] == d})
write("nz.json", nz)
print(f"Australia: {len(au)} postcodes, {sum(map(len, au.values()))} suburbs; "
      f"New Zealand: {len(nz)} postcodes, {sum(map(len, nz.values()))} suburbs")
