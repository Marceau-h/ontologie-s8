from scripts import ascsv, csv_to_onto, langues_soeur
from tqdm.auto import tqdm


def main():
    pbar = tqdm(total=3)
    pbar.set_description("lancement des scripts : ascsv")
    ascsv.all_csvs()
    pbar.update(1)
    pbar.set_description("lancement des scripts : csv_to_onto")
    csv_to_onto.main()
    pbar.update(1)
    pbar.set_description("lancement des scripts : langues_soeur")
    langues_soeur.main()
    pbar.update(1)
    pbar.set_description("fin des scripts")


if __name__ == "__main__":
    main()
