import os
from  typing import (
    List,
    Dict,
    Any
)
import pandas as pd


# load data
PROJECT_PATH: str = os.getcwd()
DATA_PATH: str = os.path.join(PROJECT_PATH, "data")

df: pd.DataFrame = pd.read_pickle(os.path.join(DATA_PATH, 'clusters.pckl'))

FEATURES_META: Dict[str, Any] = {
    'Kidhome': {'type': int, 'plot': 'bar'},
    'TotalSpends': {'type': int, 'plot': 'box'},
    'Income': {'type': int, 'plot': 'box'},
    'Meat': {'type': int, 'plot': 'box'},
    'Wines': {'type': int, 'plot': 'box'},
    'NumCatalogPurchases': {'type': int, 'plot': 'box'},
    'NPurchPerVisit': {'type': int, 'plot': 'box'},
    '%SpendOnWines': {'type': float, 'format': '{:.1%}', 'plot': 'box'},
    '%SpendOnFruits': {'type': float, 'format': '{:.1%}', 'plot': 'box'},
    '%SpendOnMeatProducts': {'type': float, 'format': '{:.1%}', 'plot': 'box'},
    '%SpendOnFishProducts': {'type': float, 'format': '{:.1%}', 'plot': 'box'},
    '%SpendOnSweetProducts': {'type': float, 'format': '{:.1%}', 'plot': 'box'},
    '%SpendOnGoldProds': {'type': float, 'format': '{:.1%}', 'plot': 'box'},
}
CATEGORIES: List[str] = ['Wines', 'Fruits', 'Meat', 'Fish', 'Sweet', 'Gold']
PALETTE: Dict[int, Any] = {
    2: dict(
        zip(
            df.groupby(["k=2"], sort=False).TotalSpends.median().sort_values().index, 
            ("red", "green")
        )
    ),
    3: dict(
        zip(
            df.groupby(["k=3"], sort=False).TotalSpends.median().sort_values().index, 
            ("red", "orange", "green")
        )
    )
}

df_stats_by_cat: pd.DataFrame = df[CATEGORIES].agg(['sum', 'mean']).T
#               Wines        Fruits           Meat          Fish         Sweet          Gold
# sum   675093.000000  58219.000000  364513.000000  83253.000000  59818.000000  97146.000000
# mean     306.164626     26.403175     165.312018     37.756463     27.128345     44.057143

df_stats_by_clst: Dict[str, pd.DataFrame] = dict()
df_stats_by_clst['k=2'] = pd.read_pickle(os.path.join(DATA_PATH, 'k_means_keq2.pckl'))
df_stats_by_clst['k=3'] = pd.read_pickle(os.path.join(DATA_PATH, 'k_means_keq3.pckl'))
