from pathlib import Path

root = Path(__file__)
while root.name != "ontologie-s8":
    root = root.parent

rdf_folder = root / "RDFs"
csv_folder = root / "CSVS"
