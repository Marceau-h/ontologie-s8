import pandas as pd


def trieur(csv, colonne):
    df = pd.read_csv(csv).fillna("")
    sorted_df = df.sort_values(by=[colonne], ascending=True)
    sorted_df.to_csv(csv, index=False)

def all_csvs():
    for csv, colonne in (
            ("../CSVS/langues_ad.csv", "Langue"),
            ("../CSVS/langues_dk.csv", "Langue"),
            ("../CSVS/langues_mh.csv", "Langue"),
            ("../CSVS/famille.csv", "Label"),
            ("../CSVS/pays.csv", "Label"),
            ("../CSVS/region.csv", "Label"),
    ):
        trieur(csv, colonne)

if __name__ == "__main__":
    all_csvs()
