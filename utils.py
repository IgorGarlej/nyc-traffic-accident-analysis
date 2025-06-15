from json import load
from pathlib import Path
from rapidfuzz import process, fuzz
from shapely.geometry import Point
import pandas as pd
from matplotlib.ticker import FuncFormatter


def load_json(path: str) -> dict:
    """Function responsible for reading JSON files"""
    with open(path, "r") as file:
        json_data = load(file)
        return json_data
    

def load_mapping(file_name: str) -> dict:
    """Function responsible for loading json mappings from other mappings directory"""
    path = Path(__file__).parent / "mappings" / file_name
    with open(path, "r") as file:
        json_data = load(file)
        return json_data
    
    
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

def create_geometry_column(df: pd.DataFrame):
    """
    Creates a column with geometry.
    """

    df["GEOMETRY"] = df.apply(lambda row: Point(row["LONGITUDE"], row["LATITUDE"]), axis=1 )


class StreetNormalizer:
    """
    A class responsible for normalizing street names using predefined abbreviation mappings.
    """

    def __init__(self, mapping_file: str ="street_abbreviations.json"):
        """
        Initializes street normalizer by load mapping from a JSON file
        """
        
        self.abbreviations = self._load_mapping(mapping_file)
    
    def _load_mapping(self, file_name: str) -> dict:
        """
        Loads the mapping from the mapping directory.
        """

        path = Path(__file__).parent / "mappings" / file_name
        with open(path, "r") as file:
            json_data = load(file).get("street_abbreviations", {})
            return json_data
        
    def normalize_string(self, street_name: str) -> str:
        """
        Normalizes a single string
        """

        for abbrev, full_name in self.abbreviations.items():
            street_name = street_name.replace(abbrev, full_name)
        return street_name
    
    def normalize_series(self, series: pd.Series) -> pd.Series:
        """
        Normalizes all street in the Pandas Series
        """

        return series.apply(self.normalize_string)
    
    def normalize_df_cols(self,df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """
        Normalizes multiple columns
        """
        df = df.copy()
        for col in columns:
            df[col] = self.normalize_series(df[col])
        return df
    



def normalize_street_names(street: str) -> str:
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

def reverse_dict_list(dict: dict) -> dict:
    """
    Creates a reverse dictionary.
    """

    reverse_dict = {}

    for key, values in dict.items():
        for val in values:
            reverse_dict[val] = key
    return reverse_dict


def map_vehicle_type(df: pd.DataFrame,
        cols: list,
        generalized: bool = False,
        raw_mapping: dict = None,
        generalized_mapping: dict = None
) -> pd.DataFrame:
    """
    Cleans raw typos and categorizes vehicle types. 
    Optionally generalizes vehicle types into broader category.
    """
    if raw_mapping is None:
        raise ValueError("Raw mapping is required")
    if generalized and generalized_mapping is None:
        raise ValueError("Generalized mapping is required if 'generalized=True'.")

    reverse_raw_mapping = reverse_dict_list(raw_mapping)

    reverse_generalized_mapping = None

    if generalized:
        reverse_generalized_mapping = reverse_dict_list(generalized_mapping)

    def map_type(type_name):
        mapped_type = reverse_raw_mapping.get(type_name, "unknown")

        if generalized:
            generalized_type = reverse_generalized_mapping.get(mapped_type, "unknown")
            return generalized_type
        
        return mapped_type
   
    df_result = df.copy()

    for col in cols:

        df_result[col] = df_result[col].map(map_type)

    return df_result


def apply_thousand_separator(ax):
    """
    Applies coma as a thousand separator.
    """

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))

    

if __name__ == "__main__":

    data = {
        'street_address': ['123 Main st', '456 Oak ave', '789 First blvd'],
        'mailing_address': ['111 Park dr', '222 Second st', '333 Third ave']
    }

    df = pd.DataFrame(data)
    normalizer = StreetNormalizer()
    result = normalizer.normalize_df_cols(df, ["street_address", "mailing_address"])
    print(result)
    

    

