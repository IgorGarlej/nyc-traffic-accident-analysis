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

