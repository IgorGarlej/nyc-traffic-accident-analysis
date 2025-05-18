from rapidfuzz import process, fuzz
from shapely.geometry import Point
import pandas as pd


# https://rapidfuzz.github.io/RapidFuzz/Usage/process.html

def find_similar_phrases(col, threshold=90):
    """
    Comperes unique values in a column and returns a dictionary where keys are unique values and values are similar phrases.
    """
    unique_phrases = col.unique()
    suggestions= {}

    for phrase in unique_phrases:
        matches = process.extract(phrase, unique_phrases, scorer=fuzz.token_sort_ratio, score_cutoff=threshold)

        # exlude self-matches
        similar = [match for match, score, _ in matches if match != phrase]

        if similar:
            suggestions[phrase] = similar
        
    return suggestions


# https://geopandas.org/en/stable/docs/user_guide/mergingdata.html#spatial-joins

def create_geometry_column(df):
    """
    Creates a column with geometry.
    """

    df["GEOMETRY"] = df.apply(lambda row: Point(row["LONGITUDE"], row["LATITUDE"]), axis=1 )

def normalize_street_names(street):
    """
    Normalizes common abbreviations of street.
    """
    street = street.replace(" ave", " avenue")
    street = street.replace(" st, ", " street")
    street = street.replace(" blvd, ", " boulevard")
    street = street.replace(" rd", " road")
    street = street.replace(" pkwy", " parkway")
    street = street.replace(" expy", " expressway")
    street = street.replace(" br", " bridge")
    street = street.replace(" hwy", " highway")
    street = street.replace(" hwy", " highway")
    street = street.replace(" sr", "") # state route
    street = street.replace(" s/r", "") # service route
    street = street.replace(" e ", " east ")
    street = street.replace(" w ", " west ")
    street = street.replace(" n ", " north ")
    street = street.replace(" s ", " south ")

    return street


mapping = {
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
        "unknown": ["unknown", "unkno", "unkow", "ukn", "unk", "none", "nan", "other", "moter"],
        "enclosed body": ["enclosed body - nonremovable enclosure", "enclosed body - removable enclosure"],
        "open body": ["open body"],
        "passenger": ["passa", "passe"],
        "uhaul": ["uhaul", "uhual", "u-hau"],
        "special": ["psh", "p/sh"],
        "apportioned": ["aport", "appor"],
        "15 passenger": ["15 pa"],
        "12 passenger": ["12 pa"],
        "passenger vehicle" : ["passenger vehicle"],
        "sea vehicle": ["sea", "se"],
        "armored truck": ["armored truck", "armor"],
        "police": ["polic", "nypd"],
        "beverage truck" : ["beverage truck"],
        "concrete mixer truck" : ["concrete mixer", "cement", "cemen", "(ceme", "concr"],
        "livery vehicle": ["livery vehicle", "liver"]
    }


def map_vehicle_type(df, cols, mapping):

    reverse_mapping = {}

    for correct_type, incorrect_types in mapping.items():
        for incorrect_type in incorrect_types:
            reverse_mapping[incorrect_type] = correct_type

    def replace_type(type_name):
        return reverse_mapping.get(type_name, "unknown")
    
    df_corrected_types = df.copy()

    for col in cols:
        df_corrected_types[col] = df_corrected_types[col].map(replace_type)

    return df_corrected_types