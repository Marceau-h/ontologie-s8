from rdflib.graph import Graph, Literal
from rdflib.namespace import Namespace, OWL, RDF, RDFS

from scripts.path import *


def main():
    graph = Graph()
    rdf = graph.parse(rdf_folder / "pre-langues.ttl")

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

    aLangueSoeur = create_property(graph, "estSoeur", "Langue", "Langue")

    langues = graph.subjects(RDF.type, untitled_ontology["Langue"])

    langues_list = list(langues)

    langues_dict = {}

    for langue in langues_list:
        langue_mere = graph.objects(langue, untitled_ontology["estLangueFille"])
        for l in langue_mere:
            if l not in langues_dict:
                langues_dict[l] = []
            langues_dict[l].append(langue)

    for k, v in langues_dict.items():
        for i in v:
            for j in v:
                if i != j:
                    graph.add((i, aLangueSoeur, j))
                    graph.add((j, aLangueSoeur, i))

    graph.serialize(destination=rdf_folder / "langues.ttl", format='turtle')
    graph.serialize(destination=rdf_folder / "langues.rdf", format="xml")

    graph.serialize(destination=root / "langues.ttl", format='turtle')


if __name__ == "__main__":
    main()
