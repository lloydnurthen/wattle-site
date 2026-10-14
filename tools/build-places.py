#!/usr/bin/env python3
"""Build register/places/*.json: postcode -> suburbs, for the register form's suburb list.

Source: GeoNames postal codes (https://www.geonames.org/, CC BY 4.0), as converted by
https://github.com/zauberware/postal-codes-json-xml-csv (data/AU.zip, data/NZ.zip).
Usage: python3 tools/build-places.py zipcodes.au.csv zipcodes.nz.csv
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

OUT.mkdir(parents=True, exist_ok=True)
au, nz = load(sys.argv[1]), load(sys.argv[2])
for d in "0123456789":
    write(f"au-{d}.json", {k: v for k, v in au.items() if k[0] == d})
write("nz.json", nz)
print(f"Australia: {len(au)} postcodes, {sum(map(len, au.values()))} suburbs; New Zealand: {len(nz)} postcodes")
