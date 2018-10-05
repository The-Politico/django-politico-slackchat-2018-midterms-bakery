fips_by_postal = {
    "AK": "02",
    "AL": "01",
    "AR": "05",
    "AS": "60",
    "AZ": "04",
    "CA": "06",
    "CO": "08",
    "CT": "09",
    "DC": "11",
    "DE": "10",
    "FL": "12",
    "GA": "13",
    "GU": "66",
    "HI": "15",
    "IA": "19",
    "ID": "16",
    "IL": "17",
    "IN": "18",
    "KS": "20",
    "KY": "21",
    "LA": "22",
    "MA": "25",
    "MD": "24",
    "ME": "23",
    "MI": "26",
    "MN": "27",
    "MO": "29",
    "MS": "28",
    "MT": "30",
    "NC": "37",
    "ND": "38",
    "NE": "31",
    "NH": "33",
    "NJ": "34",
    "NM": "35",
    "NV": "32",
    "NY": "36",
    "OH": "39",
    "OK": "40",
    "OR": "41",
    "PA": "42",
    "PR": "72",
    "RI": "44",
    "SC": "45",
    "SD": "46",
    "TN": "47",
    "TX": "48",
    "UT": "49",
    "VA": "51",
    "VI": "78",
    "VT": "50",
    "WA": "53",
    "WI": "55",
    "WV": "54",
    "WY": "56",
}

slugs_by_postal = {
    "AK": "alaska",
    "AL": "alabama",
    "AR": "arkansas",
    "AS": "american-samoa",
    "AZ": "arizona",
    "CA": "california",
    "CO": "colorado",
    "CT": "connecticut",
    "DC": "district-of-columbia",
    "DE": "delaware",
    "FL": "florida",
    "GA": "georgia",
    "GU": "guam",
    "HI": "hawaii",
    "IA": "iowa",
    "ID": "indiana",
    "IL": "illinois",
    "IN": "indiana",
    "KS": "kansas",
    "KY": "kentucky",
    "LA": "louisiana",
    "MA": "massachusetts",
    "MD": "maryland",
    "ME": "maine",
    "MI": "michigan",
    "MN": "minnesota",
    "MO": "missouri",
    "MS": "mississippi",
    "MT": "montana",
    "NC": "north-carolina",
    "ND": "north-dakota",
    "NE": "nebraska",
    "NH": "new-hampshire",
    "NJ": "new-jersey",
    "NM": "new-mexico",
    "NV": "nevada",
    "NY": "new-york",
    "OH": "ohio",
    "OK": "oklahoma",
    "OR": "oregon",
    "PA": "pennsylvania",
    "PR": "puerto-rico",
    "RI": "rhode-island",
    "SC": "south-carolina",
    "SD": "south-dakota",
    "TN": "tennessee",
    "TX": "texas",
    "UT": "utah",
    "VA": "virginia",
    "VI": "virgin-islands",
    "VT": "vermont",
    "WA": "washington",
    "WI": "wisconsin",
    "WV": "west-virginia",
    "WY": "wyoming",
}

postal_by_fips = {
    fips_by_postal[postal]: postal for postal in fips_by_postal.keys()
}

postal_by_slugs = {
    slugs_by_postal[postal]: postal for postal in slugs_by_postal.keys()
}

fips_by_slugs = {
    slugs_by_postal[postal]: fips_by_postal[postal]
    for postal in slugs_by_postal.keys()
}

slugs_by_fips = {fips_by_slugs[slug]: slug for slug in fips_by_slugs.keys()}


def fips_to_postal(fips):
    return postal_by_fips[fips]


def postal_to_fips(postal):
    return fips_by_postal[postal]


def fips_to_slug(fips):
    return slugs_by_fips[fips]


def slug_to_fips(slug):
    return fips_by_slugs[slug]


def postal_to_slug(postal):
    return slugs_by_postal[postal]


def slug_to_postal(slug):
    return postal_by_slugs[slug]
