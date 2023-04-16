import pandas as pd

from scripts.path import *


def trieur(csv, colonne):
    df = pd.read_csv(csv).fillna("")
    sorted_df = df.sort_values(by=[colonne], ascending=True)
    sorted_df.to_csv(csv, index=False)


def all_csvs():
    for csv, colonne in (
            (csv_folder / "langues_ad.csv", "Langue"),
            (csv_folder / "langues_dk.csv", "Langue"),
            (csv_folder / "langues_mh.csv", "Langue"),
            (csv_folder / "famille.csv", "Label"),
            (csv_folder / "pays.csv", "Label"),
            (csv_folder / "region.csv", "Label"),
    ):
        trieur(csv, colonne)


if __name__ == "__main__":
    all_csvs()
