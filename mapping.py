raw_mapping = {
        "bus": ["bu", "bs", "omnibus"],
        "van": ["vang", "vn", "van t", "van (", "van/t", "refrigerated van", "van camper"],
        "taxi": ["taxi"],
        "bike": ["bicycle", "bicyc"],
        "e-bike": ["ebike", "e bik", "e-bik", "e/bik", "e- bi", "e - b"],
        "scooter": ["scoot", "scoo", "scooter", "motorscooter"],
        "motorcycle": ["motor", "motorcycle", "motorbike"],
        "suv": ["station wagon/sport utility vehicle", "sport utility / station wagon"],
        "school bus": ["schoo"],
        "e-scooter": ["e sco", "e-sco"],
        "moped": ["mopd", "mopad"],
        "garbage or refuse" : ["garbage or refuse"],
        "tractor truck": ["tractor truck diesel", "tractor truck gasoline", "convertible", "semi", "semi-", "trail"],
        "truck": ["trk", "tk", "tr", "ltr", "trl", "trlr", "trc", "track", "tract", "trac", "trac.", "tow truck / wrecker", "chassis cab", "cab", "cb"],
        "pickup truck" : ["pickup-truck", "pick-up truck"],
        "pickup": ["pick", "pick-", "picku", "pkup"],
        "box truck": ["boxtr", "box t", "box"],
        "lift boom truck": ["lift boom", "boom", "lift"],
        "tanker": ["tanker", "tanke", "oil t", "fuel"],
        "tank": ["tank"],
        "flatbed": ["flat", "flatb", "flat/", "flat bed", "flat rack" , "stake or rack", "livestock rack", "glass rack"],
        "dump truck": ["dump", "dumps", "dumpt"],
        "delivery": ["deliv", "delv", "delvi", "del", "fedex"],
        "ambulance": ["ambu", "amabu", "amb", "am", "mb", "ambul", "e amb"],
        "fire truck": ["fire", "firet"],
        "forklift": ["fork", "forkl", "fork-"],
        "utility": ["util", "utili", "ulili", "ut"],
        "limo": ["limou"],
        "motor home": ["motorized home", "motor home"],
        "rv": ["r/v"],
        "tow truck": ["towtr", "tow-t", "tow t", "tow"],
        "crane": ["crane"],
        "sedan": ["2 dr sedan", "4 dr sedan", "4ds", "4dsd", "4d"],
        "construction": ["const", "cont"],
        "postal": ["usps", "usps2", "uspos", "posta", "posto", "mail"],
        "federal": ["fdny", "fd ny", "feder"],
        "nyc agency": ["nyc a", "nys a", "ns am", "nyc d", "nyc f", "nyc m", "nyc b"],
        "special purpose": ["spc", "sp", "g spc", "spc p", "spec", "pc"],
        "commercial": ["comme", "comm", "commm", "com", "com.", "comb", "co", "cm", "comer"],
        "omnibus": ["omni", "omnib"],
        "ladder": ["ladde", "loade"],
        "chevy": ["chevy", "chevo", "heavy"],
        "mark": ["mark", "marke"],
        "skateboard": ["skate", "state"],
        "horse": ["horse", "hrse"],
        "suburban": ["subn", "subn/", "sub"],
        "ems": ["ems a", "ems b"],
        "caterpillar": ["cater", "cate", "cat.", "cat p" ],
        "dot": ["dot t", "dot r"],
        "winnebago": ["wineb", "winne"],
        "trailer": ["trl", "trlr", "ltrl", "ltr"],
        "unknown": ["unknown", "unkno", "unkow", "ukn", "unk", "none", "nan"],
        "other": ["other", "moter"],
        "enclosed body": ["enclosed body - nonremovable enclosure", "enclosed body - removable enclosure"],
        "open body": ["open body"],
        "uhaul": ["uhaul", "uhual", "u-hau"],
        "special": ["psh", "p/sh"],
        "apportioned": ["aport", "appor"],
        "15 passenger": ["15 pa"],
        "12 passenger": ["12 pa"],
        "passenger vehicle" : ["passenger vehicle","passa", "passe", "passenger"],
        "sea vehicle": ["sea", "se"],
        "armored truck": ["armored truck", "armor"],
        "police": ["polic", "nypd"],
        "beverage truck" : ["beverage truck"],
        "concrete mixer truck" : ["concrete mixer", "cement", "cemen", "(ceme", "concr"],
        "livery vehicle": ["livery vehicle", "liver"]
    }

generalized_mapping = {
    "car": [
        "sedan", "suburban", "passenger", "passenger vehicle", 
        "mark", "chevy", "limo"
    ],
    "motorcycle": [
        "motorcycle", "moped", "bike", "e-bike", "scooter", "e-scooter"
    ],
    "van": [
        "van", "delivery", "postal", "uhaul"
    ],
    "taxi / livery": [
        "taxi", "livery vehicle"
    ],
    "bus": [
        "bus", "school bus", "omnibus"
    ],
    "truck": [
        "box truck", "flatbed", "dump truck", 
        "tractor truck", "truck", "tow truck", "tanker", "tank", "crane", 
        "lift boom truck", "garbage or refuse", "beverage truck", "concrete mixer truck",
        "armored truck"
    ],
    "pickup": [
        "pickup", "pickup truck"
    ],
    "suv": [
        "suv"
    ],
    "rv / motorhome": [
        "motor home", "rv", "winnebago"
    ],
    "construction / industrial": [
        "forklift", "caterpillar", "construction"
    ],
    "emergency / government": [
        "fire truck", "police", "federal", "nyc agency", "dot", "utility", "ems", "ambulance"
    ],
    "commercial / special purpose": [
        "commercial", "special purpose", "special", "apportioned", 
        "15 passenger", "12 passenger", "enclosed body", "open body"
    ],
    "unknown": [
        "unknown"
    ],
    "other": [
        "other","sea vehicle", "horse", "skateboard"
    ]
}