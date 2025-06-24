from json import load
from pathlib import Path
from rapidfuzz import process, fuzz
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


class DataFetcher:
    """
    A class responsible for retrieving data from CSV file and summerizing it briefly.
    """

    @staticmethod
    def load_json(path: str) -> dict:
        """
        Function responsible for reading JSON files.
        """

        with open(path, "r") as file:
            json_data = load(file)
            return json_data

    @staticmethod
    def get_data(csv_path: str, json_path: str) -> pd.DataFrame:
        """
        Function responsible for retrieving data from a CSV file using dtype information from a JSON file.
        """

        json_data = DataFetcher.load_json(json_path)
        dtypes = json_data["nypd-motor-vehicle-collisions"]["cols_dtypes"]
        use_cols = json_data["nypd-motor-vehicle-collisions"]["cols_to_read"]
        data = pd.read_csv(
            csv_path,
            dtype=dtypes,
            usecols=use_cols,
            engine="pyarrow"
        )
        return data
    
    @staticmethod
    def show_null_values_summary(data: pd.DataFrame):
        """
        Shows null values.
        """

        return data.copy().isnull().sum().sort_values(ascending=True)



class DataPreparation:
    """
    A class responsible for the data preparation.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Stores the original DataFrame as an instance variable.
        """
        self.df = data.copy()

    def clean_data(self) -> None:
        
        self.df = self.df.drop_duplicates()


    def standarize_text(self, columns: list[str]) -> None:
        """
        Standarizes text with fillna, lowercase and strip
        """

        for col in columns:
            if col in self.df.columns:
                self.df[col] = (
                    self.df[col]
                    .fillna("unknown")
                    .astype(str)
                    .str.lower()
                    .str.strip()
                    .replace(["unspecified",""], "unknown")
                )
    
    def standarize_numbers(self, columns: list[int]) -> None:
        """
        Fills NaNs with 0.
        """

        for col in columns:
            if col in self.df.columns:
                self.df[col] = (
                    self.df[col]
                    .fillna(0)
                    .astype(int)
                )


    def fill_missing_boroughs(self) -> None:
        """
        Fills missing boroughs based on available longitude and latitude.
        """
        from utils import fill_missing_boroughs
        self.df = fill_missing_boroughs(self.df)

    def count_missing_boroughs(self) -> None:
        total_rows = len(self.df)
        missing_count = self.df["BOROUGH"].isna().sum()
        missing_boroughs = missing_count / total_rows

        print(f"Missing boroughs: {round(missing_boroughs*100,2)}%")
                                
                
    def save_data(self, save_path: str) -> None:
        """
        Saves processed DataFrame to CSV file.
        """

        self.df.to_csv(save_path, index=False)


class Visualization:
    """
    A class for visuals.
    """
    
    def show_unique_observations(df: pd.DataFrame, col: str) -> None:
        """
        Creates a bar plot showing unique observations.
        """

        if col not in df.columns:
            print(f"Column {col} not found in the given DataFrame")
            return

        value_counts = df[col].value_counts(dropna=False)
        ax = value_counts.plot(kind='bar', figsize=(10, 6), color='skyblue')

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))

        plt.title(f"Value Counts in '{col}'")
        plt.xlabel(col)
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        

class StreetNormalizer:
    """
    A class responsible for normalizing street names using predefined abbreviation mappings.
    """

    def __init__(self, mapping_file: str ="street_abbreviations.json"):
        """
        Initializes street normalizer by loading mapping from a JSON file
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

def fill_missing_boroughs(df: pd.DataFrame) -> pd.DataFrame:
    # create a copy
    df = df.copy()

    # create geometry df
    geometry_df = df.dropna(subset=["LONGITUDE", "LATITUDE"]).copy()

    # create a column with original index as the original one will be replaced after sjoin
    geometry_df["ORIGINAL INDEX"] = geometry_df.index

    # create geometry column
    def create_geometry_column(geometry_df):
        geometry_df["GEOMETRY"] = geometry_df.apply(
            lambda row: Point(row["LONGITUDE"], row["LATITUDE"]), axis=1
        )
        return geometry_df
    
    geometry_df = create_geometry_column(geometry_df)

    # convert geometry_df into GeoDataFrame
    geometry_gdf = gpd.GeoDataFrame(geometry_df, geometry="GEOMETRY", crs="EPSG:4326")

    # load boroughs from shapefile
    path = Path(__file__).parent / "data" / "nybb.shp"
    boroughs_gdf = gpd.read_file(path)

    # convert boroughs to the same CRS
    boroughs_gdf = boroughs_gdf.to_crs(epsg=4326)

    # spatial join
    geometry_gdf_joined = gpd.sjoin(
        geometry_gdf,
        boroughs_gdf[["BoroName", "geometry"]],
        how = "left",
        predicate = "intersects"
    )

    # fill NaNs with "UNKNOWN"
    geometry_gdf_joined["BoroName"] = geometry_gdf_joined["BoroName"].fillna("unknown")

    # fill NaN with mapped boroughs
    df.loc[geometry_gdf_joined["ORIGINAL INDEX"], "BOROUGH"] = df.loc[
       geometry_gdf_joined["ORIGINAL INDEX"], "BOROUGH"
    ].combine_first(
        geometry_gdf_joined.set_index("ORIGINAL INDEX")["BoroName"]
    )

    return df


def load_mappings(file_name="vehicle_types.json") -> tuple[dict, dict]:
    """
    Loads raw and generalized mappings from a JSON file.
    """

    path = Path(__file__).parent / "mappings" / file_name
    with open(path, "r") as file:
        data = load(file)
        return data.get("raw_mapping", {}), data.get("generalized_mapping", {})
    

def reverse_dict_list(mapping: dict) -> dict:
    """
    Creates a reverse dictionary.
    """

    reverse_dict = {}

    for key, values in mapping.items():
        for val in values:
            reverse_dict[val] = key
    return reverse_dict


def map_vehicle_type(
        df: pd.DataFrame,
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


