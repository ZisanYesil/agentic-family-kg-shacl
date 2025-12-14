from rdflib import Graph
from pyshacl import validate

def run_validation(data_path, shapes_path):
    data_graph = Graph()
    data_graph.parse(data_path)

    shapes_graph = Graph()
    shapes_graph.parse(shapes_path, format="turtle")

    conforms, report_graph, report_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        debug=False
    )

    return conforms, report_text