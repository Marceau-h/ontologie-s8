from rdflib.graph import Graph, Literal
from rdflib.namespace import Namespace, OWL, RDF, RDFS, XSD

import pandas as pd

from scripts.ascsv import all_csvs
from scripts.path import *


def main():


    graph = Graph()

    rdf_ = graph.parse(rdf_folder / "languesV1.ttl")

    famille_de_langue = pd.read_csv(csv_folder / "famille.csv")
    pays = pd.read_csv(csv_folder / "pays.csv")
    region = pd.read_csv(csv_folder / "region.csv")

    untitled_ontology = Namespace("http://www.semanticweb.org/marceau/ontologies/2023/2/untitled-ontology-5#")
    dbpedia = Namespace("http://dbpedia.org/resource/")
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

    graph.bind("untitled-ontology-5", untitled_ontology)
    graph.bind("dbpedia", dbpedia)
    graph.bind("owl", owl)
    graph.bind("rdf", rdf)
    graph.bind("rdfs", rdfs)
    graph.bind("xsd", xsd)

    def parse_multiple_values(row, column):
        values = row[column].split(",")
        values = [v.strip() for v in values]
        values = [v for v in values if v and v != ""]
        return values

    def parse_int(value):
        return int(value) if value else 0

    def create_class(graph, label, parent=None):
        class_uri = untitled_ontology[label]
        graph.add((class_uri, RDF.type, OWL.Class))
        graph.add((class_uri, RDFS.label, Literal(label)))
        if parent:
            parent_uri = untitled_ontology[parent]
            graph.add((class_uri, RDFS.subClassOf, parent_uri))
        return class_uri

    def create_property(graph, label, domain, range, parent=None):
        if not label:
            return None
        property_uri = untitled_ontology[label]
        graph.add((property_uri, RDF.type, OWL.ObjectProperty))
        graph.add((property_uri, RDFS.label, Literal(label)))
        domain_uri = untitled_ontology[domain]
        graph.add((property_uri, RDFS.domain, domain_uri))
        range_uri = untitled_ontology[range]
        graph.add((property_uri, RDFS.range, range_uri))
        if parent:
            parent_uri = untitled_ontology[parent]
            graph.add((property_uri, RDFS.subPropertyOf, parent_uri))
        return property_uri

    def create_instance(graph, label, class_uri):
        instance_uri = untitled_ontology[label]
        graph.add((instance_uri, RDF.type, class_uri))
        graph.add((instance_uri, RDFS.label, Literal(label)))
        return instance_uri

    def create_datatype_property(graph, label, domain, range, parent=None):
        property_uri = untitled_ontology[label]
        graph.add((property_uri, RDF.type, OWL.DatatypeProperty))
        graph.add((property_uri, RDFS.label, Literal(label)))
        domain_uri = untitled_ontology[domain]
        graph.add((property_uri, RDFS.domain, domain_uri))
        range_uri = XSD[range]
        graph.add((property_uri, RDFS.range, range_uri))
        if parent:
            parent_uri = untitled_ontology[parent]
            graph.add((property_uri, RDFS.subPropertyOf, parent_uri))
        return property_uri

    classes = {
        "Langue": create_class(graph, "Langue"),
        "Pays": create_class(graph, "Pays"),
        "Région": create_class(graph, "Région"),
        "Continent": create_class(graph, "Continent"),
        "Famille_de_langue": create_class(graph, "Famille_de_langue"),
        "Organisation": create_class(graph, "Organisation"),
        "Propriété": create_class(graph, "Propriété"),
        "Alphabet": create_class(graph, "Alphabet"),
        "Indo_europeenne": create_class(graph, "Indo_europeenne", "Famille_de_langue"),
    }

    properties = {
        "a_langue_mere": create_property(graph, "estLangueFille", "Langue", "Langue"),
        "a_propriété": create_property(graph, "aPropriété", "Langue", "Propriété"),
        "a_organisation": create_property(graph, "estLangueOrganisation", "Langue", "Organisation"),
        "a_famille": create_property(graph, "estDansLaFamille", "Langue", "Famille_de_langue"),
        "a_alphabet": create_property(graph, "aAlphabet", "Langue", "Alphabet"),
        "a_pays": create_property(graph, "estLangue", "Langue", "Pays"),
        "a_pays_origine": create_property(graph, "aPaysOrigine", "Langue", "Pays"),
        "a_region": create_property(graph, "aRégion", "Pays", "Région"),
        "a_continent": create_property(graph, "aContinent", "Région", "Continent"),
        "a_region_mere": create_property(graph, "aRégionMère", "Région", "Région"),

        "a_locuteurs": create_datatype_property(graph, "aLocuteurs", "Langue", "int"),
        "a_locuteurs_natifs": create_datatype_property(graph, "aLocuteursNatifs", "Langue", "int", "aLocuteurs"),
        "a_locuteurs_secondaires": create_datatype_property(graph, "aLocuteursSecondaires", "Langue", "int",
                                                            "aLocuteurs"),
        "a_code_iso": create_datatype_property(graph, "aCodeISO", "Langue", "string"),
    }

    instances = {
        "langues": {},
        "pays": {},
        "regions": {},
        "continents": {},
        "familles": {},
        "organisations": {},
        "propriétés": {},
        "alphabets": {},
    }

    df = pd.read_csv(csv_folder / "famille.csv").fillna("")
    for index, row in df.iterrows():
        label = row["Label"]
        origine = row["Langue_origine"]
        proprietes = row["Propriété"].split(",")
        proprietes = [p.strip() for p in proprietes]
        proprietes = [p for p in proprietes if p]

        famille_uri = create_instance(graph, label, classes["Famille_de_langue"])
        instances["familles"][label] = famille_uri

        if origine:
            origine_uri = create_instance(graph, origine, classes["Langue"])
            graph.add((famille_uri, properties["a_langue_mere"], origine_uri))

        for p in proprietes:
            p_uri = create_instance(graph, p, classes["Propriété"])
            graph.add((famille_uri, properties["a_propriété"], p_uri))

    df = pd.read_csv(csv_folder / "pays.csv").fillna("")
    for index, row in df.iterrows():
        label = row["Label"]
        region = row["Région"]

        pays_uri = create_instance(graph, label, classes["Pays"])
        instances["pays"][label] = pays_uri

        if region:
            region_uri = create_instance(graph, region, classes["Région"])
            graph.add((pays_uri, properties["a_region"], region_uri))

    df = pd.read_csv(csv_folder / "region.csv").fillna("")
    for index, row in df.iterrows():
        label = row["Label"]
        continent = row["Continent"]
        region_mere = row["Région"]

        region_uri = create_instance(graph, label, classes["Région"])
        instances["regions"][label] = region_uri

        if continent:
            continent_uri = create_instance(graph, continent, classes["Continent"])
            graph.add((region_uri, properties["a_continent"], continent_uri))

        if region_mere:
            region_mere_uri = create_instance(graph, region_mere, classes["Région"])
            graph.add((region_uri, properties["a_region_mere"], region_mere_uri))

    def parse_lang_csv(path):
        df = pd.read_csv(path).fillna("")
        for index, row in df.iterrows():
            label = row["Langue"]
            pays = parse_multiple_values(row, "Pays")
            alphabet = parse_multiple_values(row, "Alphabet")
            locuteurs_natifs = parse_int(row["Locuteurs_n"])
            locuteurs_secondaires = parse_int(row["Locuteurs_s"])
            famille = parse_multiple_values(row, "Famille")
            proprietes = parse_multiple_values(row, "Propriété")
            organisations = parse_multiple_values(row, "Organisations")
            code_iso = parse_multiple_values(row, "ISO_639-3")
            pays_origine = parse_multiple_values(row, "Pays_origine")
            langue_mere = parse_multiple_values(row, "Langue_origine")

            langue_uri = create_instance(graph, label, classes["Langue"])
            instances["langues"][label] = langue_uri

            for a in alphabet:
                a_uri = create_instance(graph, a, classes["Alphabet"])
                graph.add((langue_uri, properties["a_alphabet"], a_uri))

            for f in famille:
                if f == "Créole":
                    f_uri = create_instance(graph, f, classes["Famille_de_langue"])
                else:
                    f_uri = create_instance(graph, f, classes["Indo_europeenne"])

                graph.add((langue_uri, properties["a_famille"], f_uri))

            if locuteurs_natifs:
                graph.add((langue_uri, properties["a_locuteurs_natifs"], Literal(locuteurs_natifs)))

            if locuteurs_secondaires:
                graph.add((langue_uri, properties["a_locuteurs_secondaires"], Literal(locuteurs_secondaires)))

            for c in code_iso:
                graph.add((langue_uri, properties["a_code_iso"], Literal(c)))

            for p in proprietes:
                p_uri = create_instance(graph, p, classes["Propriété"])
                graph.add((langue_uri, properties["a_propriété"], p_uri))

            for o in organisations:
                o_uri = create_instance(graph, o, classes["Organisation"])
                graph.add((langue_uri, properties["a_organisation"], o_uri))

            for p in pays:
                p_uri = create_instance(graph, p, classes["Pays"])
                graph.add((langue_uri, properties["a_pays"], p_uri))

            for p in pays_origine:
                p_uri = instances["pays"][p]
                graph.add((langue_uri, properties["a_pays_origine"], p_uri))

            for l in langue_mere:
                l_uri = create_instance(graph, l, classes["Langue"])
                graph.add((langue_uri, properties["a_langue_mere"], l_uri))

    for path in (csv_folder / "langues_ad.csv", csv_folder / "langues_dk.csv", csv_folder / "langues_mh.csv"):
        parse_lang_csv(path)

    graph.serialize(destination=rdf_folder / "pre-langues.ttl", format='turtle')
    graph.serialize(destination=rdf_folder / "pre-langues.rdf", format="xml")


if __name__ == "__main__":
    all_csvs()
    main()
    main()
